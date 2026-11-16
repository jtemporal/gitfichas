#!/usr/bin/env python3
"""
Card Generator Module
=====================

Builds standalone GitFichas cards on a fixed 16:9 canvas, ready for print and video.

Each card contains the title block, the diagram, the card number and the signature.
The diagram is still a Mermaid block diagram, but with a stacked layout: one row per
command part with its note to the right, so the card never gets wider as the command
gets longer and the text size is the same on every card.

Pipeline for one card:
    1. Build Mermaid syntax from the post front matter.
    2. Render it with Mermaid CLI.
    3. Post-process the SVG: left-align tokens and notes, redraw the arrows from the end
       of each word to the start of its note, then place the diagram on the canvas
       together with the title, number and signature.
    4. Replace every piece of text with outlines, shaped with HarfBuzz. The final SVG
       has no fonts and no foreignObject, so it looks the same in every browser,
       in design tools and in print.
    5. Optionally export a 1920x1080 PNG with headless Chrome.

Mermaid measures text while laying out the diagram, so Borel and Chilanka must be
installed on the machine (see install_fonts).
"""

import copy
import glob
import json
import os
import platform
import re
import shutil
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

SVG_NS = "http://www.w3.org/2000/svg"
XHTML_NS = "http://www.w3.org/1999/xhtml"
XLINK_NS = "http://www.w3.org/1999/xlink"
ET.register_namespace("", SVG_NS)
ET.register_namespace("xhtml", XHTML_NS)
ET.register_namespace("xlink", XLINK_NS)

# Canvas, in SVG user units. 1120x630 is 16:9 and scales to 1920x1080.
CANVAS_W, CANVAS_H = 1120, 630
PNG_W, PNG_H = 1920, 1080
MARGIN = 44

# Area the diagram may use. It is centered here and never scaled up.
ZONE_X, ZONE_Y, ZONE_W, ZONE_H = 70, 162, 980, 406

# Text sizes in px. Mermaid applies a classDef to a node and again to its label,
# so relative units (em) compound. Absolute sizes keep the measured box and the
# rendered text in agreement.
COMMAND_SIZE = 36
NOTE_SIZE = 23
CONCEPT_SIZE = 29
COMMAND_LINE_HEIGHT = 1.2
NOTE_LINE_HEIGHT = 1.35
CONCEPT_LINE_HEIGHT = 1.4
TITLE_SIZE = 66
TITLE_SPACING = 5
TITLE_MAX_W = 900
SMALL_SIZE = 28
FOOTER_SIZE = 28

# Arrows
ARROW_GAP = 16        # space between text and arrow, on both ends
ARROW_HEAD = 6        # the marker extends past the end of the path
MIN_ARROW = 70        # length of the shortest arrow on a card
TOKEN_DY = 6          # Borel sits a little high in its line box

NUMBER_COLOR = "#5f5f5f"
AUTHOR_COLOR = "#7a357d"

# (title color, subtitle color) by card number modulo 6, same as mermaid-graphs.html
COLOR_SCHEMES = {
    1: ("#5096d0", "#006a98"),
    2: ("#1f584d", "#273535"),
    3: ("#7592e2", "#333c7d"),
    4: ("#e290b9", "#ad4784"),
    5: ("#d581e1", "#424699"),
    0: ("#689582", "#152b29"),
}

FONT_FILES = {
    "Borel": "Borel-Regular.ttf",
    "Chilanka": "Chilanka-Regular.ttf",
    "Londrina Solid": "LondrinaSolid-Regular.ttf",
    "Shadows Into Light Two": "ShadowsIntoLightTwo-Regular.ttf",
}
# Fonts the browser has to have while Mermaid measures labels.
MEASURED_FONTS = ["Borel", "Chilanka"]


class CardError(Exception):
    """Raised when a card cannot be generated."""


# ---------------------------------------------------------------------------
# Fonts
# ---------------------------------------------------------------------------

def user_font_dir() -> Path:
    """Directory where per-user fonts live on this OS."""
    system = platform.system()
    if system == "Darwin":
        return Path.home() / "Library" / "Fonts"
    if system == "Windows":
        return Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / "Microsoft" / "Windows" / "Fonts"
    return Path.home() / ".local" / "share" / "fonts"


def fonts_installed() -> List[str]:
    """Return the measured fonts that are missing from this machine."""
    missing = []
    listing = None
    if shutil.which("fc-list"):
        result = subprocess.run(["fc-list", ":", "family"], capture_output=True, text=True)
        if result.returncode == 0:
            listing = result.stdout.lower()
    for family in MEASURED_FONTS:
        if listing is not None and family.lower() in listing:
            continue
        candidates = [user_font_dir() / FONT_FILES[family], Path.home() / ".fonts" / FONT_FILES[family]]
        if any(c.exists() for c in candidates):
            continue
        missing.append(family)
    return missing


def install_fonts(fonts_dir: Path) -> Path:
    """Copy the card fonts into the user font directory."""
    target = user_font_dir()
    target.mkdir(parents=True, exist_ok=True)
    for filename in FONT_FILES.values():
        shutil.copy2(fonts_dir / filename, target / filename)
    if shutil.which("fc-cache"):
        subprocess.run(["fc-cache", "-f"], capture_output=True)
    return target


class FontBook:
    """Loads the card fonts and turns text into outlines."""

    def __init__(self, fonts_dir: Path):
        self.fonts_dir = fonts_dir
        self._fonts: Dict[str, TTFont] = {}
        self._shapers: Dict[str, "hb.Font"] = {}

    def path(self, family: str) -> Path:
        font_path = self.fonts_dir / FONT_FILES[family]
        if not font_path.exists():
            raise CardError(f"Font file not found: {font_path}")
        return font_path

    def font(self, family: str) -> TTFont:
        if family not in self._fonts:
            self._fonts[family] = TTFont(str(self.path(family)))
        return self._fonts[family]

    def shaper(self, family: str) -> "hb.Font":
        if family not in self._shapers:
            face = hb.Face(hb.Blob.from_file_path(str(self.path(family))))
            self._shapers[family] = hb.Font(face)
        return self._shapers[family]

    def metrics(self, family: str, size: float) -> Tuple[float, float]:
        """Return (ascent, descent) in px, the way browsers size a line box."""
        font = self.font(family)
        scale = size / font["head"].unitsPerEm
        return font["hhea"].ascent * scale, -font["hhea"].descent * scale

    def outline(self, family: str, text: str, size: float, spacing: float = 0) -> Tuple[str, float]:
        """Return (SVG path data, width) for text set at the given size.

        The text is shaped with HarfBuzz, so Borel's joined letters and kerning come out
        the same as in a browser. The baseline is y=0 and the text starts at x=0.
        """
        font = self.font(family)
        glyphs = font.getGlyphSet()
        order = font.getGlyphOrder()
        scale = size / font["head"].unitsPerEm

        buffer = hb.Buffer()
        buffer.add_str(text)
        buffer.guess_segment_properties()
        hb.shape(self.shaper(family), buffer)

        x = 0.0
        commands = []
        for info, position in zip(buffer.glyph_infos or [], buffer.glyph_positions or []):
            name = order[info.codepoint]
            pen = SVGPathPen(glyphs, ntos=lambda v: f"{v:.2f}".rstrip("0").rstrip("."))
            offset = (scale, 0, 0, -scale, x + position.x_offset * scale, -position.y_offset * scale)
            glyphs[name].draw(TransformPen(pen, offset))
            data = pen.getCommands()
            if data:
                commands.append(data)
            x += position.x_advance * scale + spacing
        width = x - spacing if commands or text else 0.0
        return " ".join(commands), max(width, 0.0)

    def width(self, family: str, text: str, size: float, spacing: float = 0) -> float:
        return self.outline(family, text, size, spacing)[1]

    def shape(self, family: str, text: str) -> Tuple[List[Tuple[int, int, int]], int]:
        """Shape text and return ([(glyph id, x, y)], advance), all in font units."""
        buffer = hb.Buffer()
        buffer.add_str(text)
        buffer.guess_segment_properties()
        hb.shape(self.shaper(family), buffer)
        x = 0
        run = []
        for info, position in zip(buffer.glyph_infos or [], buffer.glyph_positions or []):
            run.append((info.codepoint, x + position.x_offset, position.y_offset))
            x += position.x_advance
        return run, x

    def glyph_outline(self, family: str, glyph_id: int) -> str:
        """SVG path data for one glyph in font units (y axis pointing up)."""
        font = self.font(family)
        glyphs = font.getGlyphSet()
        pen = SVGPathPen(glyphs, ntos=lambda v: str(int(round(v))))
        glyphs[font.getGlyphOrder()[glyph_id]].draw(pen)
        return pen.getCommands()

    def units_per_em(self, family: str) -> int:
        return self.font(family)["head"].unitsPerEm


# ---------------------------------------------------------------------------
# Mermaid syntax
# ---------------------------------------------------------------------------

def clean_text(text: Any) -> str:
    """Normalize front matter text for a Mermaid label."""
    if text is None:
        return ""
    value = str(text).strip()
    value = value.replace("\\n", "<br/>").replace("\n", "<br/>")
    value = re.sub(r"<br\s*/?>", "<br/>", value)
    value = re.sub(r"\s*<br/>\s*", "<br/>", value)
    return value.replace('"', "#quot;")


def label_lines(label: str) -> List[str]:
    """The lines of a Mermaid label as they appear on the card."""
    lines = label.replace("#quot;", '"').split("<br/>")
    return [" ".join(line.split()) for line in lines]


def descriptor_map(front_matter: Dict[str, Any]) -> Dict[str, Any]:
    merged: Dict[str, Any] = {}
    for item in front_matter.get("descriptors") or []:
        if isinstance(item, dict):
            merged.update(item)
    return merged


def command_rows(front_matter: Dict[str, Any]) -> List[Tuple[str, str]]:
    """Split a command into (token, note) rows.

    "git" and the subcommand share one row because one descriptor covers both.
    """
    parts = str(front_matter.get("command", "")).split()
    descriptors = descriptor_map(front_matter)
    if len(parts) < 2:
        return [(" ".join(parts), clean_text(descriptors.get("command")))]
    rows = [(" ".join(parts[:2]), clean_text(descriptors.get("command")))]
    for index, part in enumerate(parts[2:], start=1):
        rows.append((part, clean_text(descriptors.get(f"part{index}"))))
    return rows


def card_info(front_matter: Dict[str, Any]) -> str:
    """The extra note of a card. Some posts keep it inside descriptors."""
    return clean_text(front_matter.get("info") or descriptor_map(front_matter).get("info"))


def concept_parts(front_matter: Dict[str, Any]) -> List[str]:
    parts = []
    for item in front_matter.get("parts") or []:
        if isinstance(item, dict):
            parts.extend(clean_text(value) for value in item.values())
    return [part for part in parts if part]


def _styling(command_ids: List[str], note_ids: List[str], concept_ids: List[str]) -> List[str]:
    lines = [
        "classDef transparent fill:#fff,stroke:#fff;",
        f"class {','.join(command_ids + note_ids + concept_ids)} transparent",
    ]
    if command_ids:
        lines.append(f"classDef commandFont font-family:Borel,font-size:{COMMAND_SIZE}px,line-height:{COMMAND_LINE_HEIGHT};")
        lines.append(f"class {','.join(command_ids)} commandFont")
    if note_ids:
        lines.append(f"classDef textFont font-family:Chilanka,font-size:{NOTE_SIZE}px,line-height:{NOTE_LINE_HEIGHT};")
        lines.append(f"class {','.join(note_ids)} textFont")
    if concept_ids:
        lines.append(f"classDef conceptFont font-family:Chilanka,font-size:{CONCEPT_SIZE}px,line-height:{CONCEPT_LINE_HEIGHT};")
        lines.append(f"class {','.join(concept_ids)} conceptFont")
    return lines


def command_syntax(front_matter: Dict[str, Any]) -> str:
    """Stacked layout: one row per part, token on the left, note on the right."""
    lines = ["block-beta", "columns 7"]
    command_ids, note_ids, arrows = [], [], []
    for index, (token, note) in enumerate(command_rows(front_matter)):
        command_ids.append(f"c{index}")
        token_label = clean_text(token)
        if note:
            lines.append(f'  c{index}("{token_label}"):3 space n{index}["{note}"]:3')
            note_ids.append(f"n{index}")
            arrows.append(f"  c{index} --> n{index}")
        else:
            lines.append(f'  c{index}("{token_label}"):3 space:4')
    info = card_info(front_matter)
    if info:
        lines.append(f'  info["{info}"]:7')
        note_ids.append("info")
    return "\n".join(lines + arrows + _styling(command_ids, note_ids, []))


def concept_syntax(front_matter: Dict[str, Any]) -> str:
    """Concept cards: the parts stacked and centered."""
    lines = ["block-beta", "columns 1"]
    concept_ids, note_ids = [], []
    for index, part in enumerate(concept_parts(front_matter)):
        lines.append(f'  p{index}["{part}"]')
        concept_ids.append(f"p{index}")
    info = card_info(front_matter)
    if info:
        lines.append(f'  info["{info}"]')
        note_ids.append("info")
    return "\n".join(lines + _styling([], note_ids, concept_ids))


def card_syntax(front_matter: Dict[str, Any]) -> Optional[str]:
    if front_matter.get("command"):
        return command_syntax(front_matter)
    if front_matter.get("concept") and concept_parts(front_matter):
        return concept_syntax(front_matter)
    return None


# ---------------------------------------------------------------------------
# SVG post-processing
# ---------------------------------------------------------------------------

def _translate(transform: str) -> Tuple[float, float]:
    match = re.search(r"translate\(\s*([-\d.eE]+)[ ,]*([-\d.eE]+)?\s*\)", transform or "")
    if not match:
        return 0.0, 0.0
    return float(match.group(1)), float(match.group(2) or 0)


def _tag(name: str) -> str:
    return f"{{{SVG_NS}}}{name}"


class _Node:
    """A Mermaid block node: its group, box and measured label."""

    def __init__(self, key: str, group: ET.Element):
        self.key = key
        self.group = group
        rect = group.find(_tag("rect"))
        self.label = group.find(_tag("g"))
        self.foreign = self.label.find(_tag("foreignObject")) if self.label is not None else None
        if rect is None or self.foreign is None:
            raise CardError(f"Unexpected Mermaid output for node '{key}'")
        self.cx, self.cy = _translate(group.get("transform"))
        self.box_w = float(rect.get("width"))
        self.box_h = float(rect.get("height"))
        self.label_w = float(self.foreign.get("width"))
        self.label_h = float(self.foreign.get("height"))
        self.left = self.cx - self.label_w / 2
        self.right = self.cx + self.label_w / 2

    @property
    def top(self) -> float:
        return self.cy - self.box_h / 2

    @property
    def bottom(self) -> float:
        return self.cy + self.box_h / 2

    def align_left(self, x: float, dy: float = 0) -> None:
        """Put the label's left edge at x (diagram coordinates)."""
        self.cx = x + self.box_w / 2
        self.group.set("transform", f"translate({self.cx:.3f}, {self.cy:.3f})")
        self.label.set("transform", f"translate({-self.box_w / 2:.3f}, {-self.label_h / 2 + dy:.3f})")
        div = self.foreign.find(f"{{{XHTML_NS}}}div")
        if div is not None:
            div.set("style", (div.get("style") or "") + " text-align: left;")
        self.left, self.right = x, x + self.label_w

    def center_at(self, x: float) -> None:
        self.cx = x
        self.group.set("transform", f"translate({self.cx:.3f}, {self.cy:.3f})")
        self.left, self.right = x - self.label_w / 2, x + self.label_w / 2

    def label_origin(self) -> Tuple[float, float]:
        """Top left corner of the label, relative to the node."""
        return _translate(self.label.get("transform"))

    def replace_label(self, outlines: ET.Element) -> None:
        """Swap the HTML label for outlined text.

        Mermaid styles the direct children of a node (the "transparent" class paints them
        white), so the outlines go one level deeper and set their own fill and stroke.
        """
        self.group.remove(self.label)
        wrapper = ET.SubElement(self.group, _tag("g"))
        wrapper.append(outlines)


def _collect_nodes(svg: ET.Element) -> Dict[str, _Node]:
    nodes = {}
    for group in svg.iter(_tag("g")):
        match = re.search(r"-(c\d+|n\d+|p\d+|info)$", group.get("id") or "")
        if match and "node" in (group.get("class") or ""):
            nodes[match.group(1)] = _Node(match.group(1), group)
    if not nodes:
        raise CardError("No diagram nodes found in the Mermaid output")
    return nodes


def realign(svg: ET.Element) -> Tuple[Tuple[float, float, float, float], Dict[str, _Node]]:
    """Tidy the diagram in place. Returns its bounding box (x, y, width, height) and its nodes.

    Command cards: tokens and notes are left-aligned in their columns, the note column
    sits a fixed distance after the longest token, and every arrow runs from the end of
    its word to the start of its note at the height of the row's center.
    """
    nodes = _collect_nodes(svg)
    tokens = [n for k, n in nodes.items() if k.startswith("c")]
    notes = [n for k, n in nodes.items() if k.startswith("n")]
    info = nodes.get("info")

    if tokens:
        token_x = min(n.cx - n.box_w / 2 for n in tokens)
        for node in tokens:
            node.align_left(token_x, TOKEN_DY)
        longest = max(n.right for n in tokens)
        note_x = longest + ARROW_GAP + MIN_ARROW + ARROW_HEAD + ARROW_GAP
        for node in notes:
            node.align_left(note_x)
        for path in svg.iter(_tag("path")):
            match = re.search(r"-(c\d+)-(n\d+)$", path.get("id") or "")
            if match:
                start, end = nodes[match.group(1)], nodes[match.group(2)]
                path.set("d", f"M{start.right + ARROW_GAP:.3f},{start.cy:.3f}"
                              f"L{end.left - ARROW_GAP - ARROW_HEAD:.3f},{end.cy:.3f}")
        if info is not None:
            rows = tokens + notes
            info.center_at((min(n.left for n in rows) + max(n.right for n in rows)) / 2)

    everything = list(nodes.values())
    left = min(n.left for n in everything)
    right = max(n.right for n in everything)
    top = min(n.top for n in everything)
    bottom = max(n.bottom for n in everything)
    return (left, top, right - left, bottom - top), nodes


# ---------------------------------------------------------------------------
# Card builder
# ---------------------------------------------------------------------------

class CardBuilder:
    """Builds a card SVG (and optionally a PNG) from post front matter."""

    def __init__(self, fonts_dir: Path, theme_path: Path, puppeteer_config: Optional[Path] = None):
        self.fonts = FontBook(fonts_dir)
        self.fonts_dir = fonts_dir
        self.theme_path = theme_path
        self.puppeteer_config = puppeteer_config
        self.warnings: List[str] = []
        self._glyph_defs: Dict[str, str] = {}

    # -- Mermaid -----------------------------------------------------------

    def _mermaid_command(self, source: Path, output: Path) -> List[str]:
        runner = ["mmdc"] if shutil.which("mmdc") else ["npx", "@mermaid-js/mermaid-cli"]
        command = runner + ["-i", str(source), "-o", str(output), "-b", "white", "-e", "svg",
                            "--configFile", str(self.theme_path)]
        if self.puppeteer_config:
            command += ["-p", str(self.puppeteer_config)]
        return command

    def render_diagram(self, syntax: str) -> ET.Element:
        with tempfile.TemporaryDirectory() as tmp:
            source, output = Path(tmp) / "card.mmd", Path(tmp) / "card.svg"
            source.write_text(syntax, encoding="utf-8")
            result = subprocess.run(self._mermaid_command(source, output), capture_output=True, text=True)
            if result.returncode != 0 or not output.exists():
                raise CardError(f"Mermaid CLI failed: {(result.stderr or result.stdout).strip()[-400:]}")
            return ET.parse(str(output)).getroot()

    def _check_measurement(self, front_matter: Dict[str, Any], diagram: ET.Element) -> None:
        """Fail when Mermaid measured the command with a fallback font."""
        if not front_matter.get("command"):
            return
        nodes = _collect_nodes(diagram)
        for index, (token, _) in enumerate(command_rows(front_matter)):
            node = nodes.get(f"c{index}")
            expected = self.fonts.width("Borel", token, COMMAND_SIZE)
            if node is None or expected <= 0:
                continue
            if abs(node.label_w - expected) / expected > 0.15:
                raise CardError(
                    f"'{token}' measured {node.label_w:.0f}px but should be about {expected:.0f}px. "
                    "Borel is probably not installed. Run: python3 scripts/generate_cards.py --install-fonts")

    # -- Text as outlines ----------------------------------------------------

    def _outline(self, parent: ET.Element, family: str, text: str, size: float, x: float, baseline: float,
                 fill: str, anchor: str = "start", spacing: float = 0, **attrs: str) -> float:
        """Draw text as a path. Returns its width."""
        data, width = self.fonts.outline(family, text, size, spacing)
        if anchor == "middle":
            x -= width / 2
        elif anchor == "end":
            x -= width
        if data:
            path = ET.SubElement(parent, _tag("path"), d=data, fill=fill,
                                 transform=f"translate({x:.2f}, {baseline:.2f})")
            for key, value in attrs.items():
                path.set(key.replace("_", "-"), value)
        return width

    def _title_block(self, root: ET.Element, front_matter: Dict[str, Any], title_color: str, sub_color: str) -> None:
        """Title in the middle, pretitle hanging off its left edge, subtitle off its right edge."""
        title = str(front_matter.get("title") or "").strip().upper()
        pretitle = str(front_matter.get("pretitle") or "").strip()
        subtitle = str(front_matter.get("subtitle") or "").strip()

        size, spacing = TITLE_SIZE, TITLE_SPACING
        width = self.fonts.width("Londrina Solid", title, size, spacing)
        if width > TITLE_MAX_W:
            factor = TITLE_MAX_W / width
            size, spacing, width = size * factor, spacing * factor, TITLE_MAX_W
        center = CANVAS_W / 2
        left, right = center - width / 2, center + width / 2

        group = ET.SubElement(root, _tag("g"), {"class": "card-title"})
        if pretitle:
            pre_w = self.fonts.width("Shadows Into Light Two", pretitle, SMALL_SIZE)
            x = max(MARGIN, min(left, CANVAS_W - MARGIN - pre_w))
            self._outline(group, "Shadows Into Light Two", pretitle, SMALL_SIZE, x, 50, sub_color)
        self._outline(group, "Londrina Solid", title, size, left, 116, title_color, spacing=spacing,
                      stroke=sub_color, stroke_width="2", stroke_linejoin="round")
        if subtitle:
            sub_w = self.fonts.width("Shadows Into Light Two", subtitle, SMALL_SIZE)
            x = min(CANVAS_W - MARGIN, max(right, MARGIN + sub_w))
            self._outline(group, "Shadows Into Light Two", subtitle, SMALL_SIZE, x, 150, sub_color, anchor="end")

    # -- Composition -------------------------------------------------------

    def build_svg(self, front_matter: Dict[str, Any]) -> ET.ElementTree:
        syntax = card_syntax(front_matter)
        if not syntax:
            raise CardError("Post has no command or concept parts to draw")

        diagram = self.render_diagram(syntax)
        self._check_measurement(front_matter, diagram)
        self._glyph_defs = {}
        (box_x, box_y, box_w, box_h), nodes = realign(diagram)
        self._outline_labels(front_matter, nodes)
        scale = min(1.0, ZONE_W / box_w, ZONE_H / box_h)
        if scale < 0.995:
            self.warnings.append(f"diagram scaled to {scale:.0%} to fit the canvas")

        number = str(front_matter.get("number", "")).strip()
        try:
            scheme = int(number) % 6
        except ValueError:
            scheme = 4
        title_color, sub_color = COLOR_SCHEMES[scheme]

        root = ET.Element(_tag("svg"), {
            "viewBox": f"0 0 {CANVAS_W} {CANVAS_H}", "width": str(CANVAS_W), "height": str(CANVAS_H),
            "role": "img",
        })
        label = " ".join(str(front_matter.get(key) or "").strip() for key in ("pretitle", "title", "subtitle"))
        ET.SubElement(root, _tag("title")).text = f"#{number} {' '.join(label.split())}".strip()
        ET.SubElement(root, _tag("rect"), width=str(CANVAS_W), height=str(CANVAS_H), fill="#ffffff")

        defs = ET.SubElement(root, _tag("defs"))
        for ref, data in self._glyph_defs.items():
            if data:
                ET.SubElement(defs, _tag("path"), id=ref, d=data)

        self._title_block(root, front_matter, title_color, sub_color)

        inner = copy.deepcopy(diagram)
        for attribute in ("style", "width", "height"):
            inner.attrib.pop(attribute, None)
        pad = 6
        view_w, view_h = box_w + 2 * pad, box_h + 2 * pad
        draw_w, draw_h = view_w * scale, view_h * scale
        inner.set("viewBox", f"{box_x - pad:.3f} {box_y - pad:.3f} {view_w:.3f} {view_h:.3f}")
        inner.set("x", f"{ZONE_X + (ZONE_W - draw_w) / 2:.3f}")
        inner.set("y", f"{ZONE_Y + (ZONE_H - draw_h) / 2:.3f}")
        inner.set("width", f"{draw_w:.3f}")
        inner.set("height", f"{draw_h:.3f}")
        inner.set("overflow", "visible")
        root.append(inner)

        footer = ET.SubElement(root, _tag("g"), {"class": "card-footer"})
        baseline = CANVAS_H - 30
        if number:
            self._outline(footer, "Shadows Into Light Two", f"#{number}", FOOTER_SIZE, MARGIN, baseline, NUMBER_COLOR)
        author = str(front_matter.get("author") or "").strip()
        if author:
            self._outline(footer, "Shadows Into Light Two", author, FOOTER_SIZE, CANVAS_W - MARGIN, baseline,
                          AUTHOR_COLOR, anchor="end")
        return ET.ElementTree(root)

    def _outline_labels(self, front_matter: Dict[str, Any], nodes: Dict[str, "_Node"]) -> None:
        """Replace Mermaid's HTML labels with outlined text in the same position.

        HTML inside foreignObject and embedded web fonts are the two things browsers
        disagree on in an SVG. Outlines look the same everywhere.
        """
        labels: Dict[str, str] = {}
        if front_matter.get("command"):
            for index, (token, note) in enumerate(command_rows(front_matter)):
                labels[f"c{index}"] = clean_text(token)
                labels[f"n{index}"] = note
        else:
            for index, part in enumerate(concept_parts(front_matter)):
                labels[f"p{index}"] = part
        labels["info"] = card_info(front_matter)

        for key, node in nodes.items():
            if key.startswith("c"):
                family, size, line_height, centered = "Borel", COMMAND_SIZE, COMMAND_LINE_HEIGHT, False
            elif key.startswith("p"):
                family, size, line_height, centered = "Chilanka", CONCEPT_SIZE, CONCEPT_LINE_HEIGHT, True
            else:
                family, size, line_height, centered = "Chilanka", NOTE_SIZE, NOTE_LINE_HEIGHT, key == "info"

            ascent, descent = self.fonts.metrics(family, size)
            line_px = size * line_height
            scale = size / self.fonts.units_per_em(family)
            origin_x, origin_y = node.label_origin()
            group = ET.Element(_tag("g"), {"class": "card-text", "fill": "#000000", "stroke": "none"})
            for row, line in enumerate(label_lines(labels.get(key, ""))):
                run, advance = self.fonts.shape(family, line)
                x = origin_x + (node.label_w - advance * scale) / 2 if centered else origin_x
                baseline = origin_y + row * line_px + (line_px - ascent - descent) / 2 + ascent
                # One group per line in font units; each glyph is drawn once in <defs> and reused.
                line_group = ET.SubElement(
                    group, _tag("g"), transform=f"translate({x:.2f}, {baseline:.2f}) scale({scale:.5f}, {-scale:.5f})")
                for glyph_id, glyph_x, glyph_y in run:
                    ref = self._glyph_ref(family, glyph_id)
                    if ref is None:
                        continue
                    use = ET.SubElement(line_group, _tag("use"), {f"{{{XLINK_NS}}}href": f"#{ref}"})
                    if glyph_x:
                        use.set("x", str(glyph_x))
                    if glyph_y:
                        use.set("y", str(glyph_y))
            node.replace_label(group)

    def _glyph_ref(self, family: str, glyph_id: int) -> Optional[str]:
        """Id of the shared outline for a glyph, or None when the glyph is blank (a space)."""
        ref = f"{family[0].lower()}{glyph_id}"
        if ref not in self._glyph_defs:
            self._glyph_defs[ref] = self.fonts.glyph_outline(family, glyph_id)
        return ref if self._glyph_defs[ref] else None

    def write_svg(self, front_matter: Dict[str, Any], output: Path) -> None:
        tree = self.build_svg(front_matter)
        output.parent.mkdir(parents=True, exist_ok=True)
        tree.write(str(output), encoding="utf-8", xml_declaration=True)

    # -- PNG export --------------------------------------------------------

    def find_chrome(self) -> Optional[str]:
        for variable in ("CHROME_PATH", "PUPPETEER_EXECUTABLE_PATH"):
            if os.environ.get(variable):
                return os.environ[variable]
        if self.puppeteer_config and self.puppeteer_config.exists():
            try:
                configured = json.loads(self.puppeteer_config.read_text()).get("executablePath")
                if configured:
                    return configured
            except (ValueError, OSError):
                pass
        for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome"):
            if shutil.which(name):
                return shutil.which(name)
        candidates = [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "/Applications/Chromium.app/Contents/MacOS/Chromium",
        ]
        cache = Path.home() / ".cache" / "puppeteer"
        candidates += sorted(glob.glob(str(cache / "chrome" / "*" / "chrome-*" / "chrome")), reverse=True)
        candidates += sorted(glob.glob(str(cache / "chrome" / "*" / "chrome-*" / "*.app" / "Contents" / "MacOS" / "*")),
                             reverse=True)
        for candidate in candidates:
            if Path(candidate).exists():
                return candidate
        return None

    def write_png(self, svg_path: Path, png_path: Path) -> None:
        """Rasterize a card to 1920x1080 with headless Chrome."""
        chrome = self.find_chrome()
        if not chrome:
            raise CardError("Chrome not found for PNG export. Set CHROME_PATH to a Chrome or Chromium binary.")
        with tempfile.TemporaryDirectory() as tmp:
            sized = Path(tmp) / "card.svg"
            content = svg_path.read_text(encoding="utf-8")
            content = content.replace(f'width="{CANVAS_W}" height="{CANVAS_H}"', f'width="{PNG_W}" height="{PNG_H}"', 1)
            sized.write_text(content, encoding="utf-8")
            command = [chrome, "--headless=new", "--hide-scrollbars", "--force-device-scale-factor=1",
                       "--virtual-time-budget=2000", f"--window-size={PNG_W},{PNG_H}",
                       f"--screenshot={png_path}", sized.as_uri()]
            if hasattr(os, "geteuid") and os.geteuid() == 0:
                command.insert(1, "--no-sandbox")
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode != 0 or not png_path.exists():
                raise CardError(f"Chrome could not export the PNG: {result.stderr.strip()[-300:]}")
