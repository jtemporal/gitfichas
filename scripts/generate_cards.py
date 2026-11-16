#!/usr/bin/env python3
"""
GitFichas Card Generator (16:9, print and video ready)
======================================================

Generates one standalone card per Mermaid post in assets/img/cards/. Every card uses
the same 16:9 canvas and the same text size, and includes the title, the diagram,
the card number and the signature.

The site shows these cards through _includes/mermaid-graphs.html for every post with
use_static_image: true. The posts themselves are never modified.

Usage:
    python3 scripts/generate_cards.py [filter] [options]

Examples:
    python3 scripts/generate_cards.py --install-fonts   # once per machine
    python3 scripts/generate_cards.py                   # all cards that don't exist yet
    python3 scripts/generate_cards.py 028 --force       # regenerate card 028 in every language
    python3 scripts/generate_cards.py 028 --lang pt --png
"""

import argparse
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, Optional

import yaml

script_dir = Path(__file__).parent
if str(script_dir) not in sys.path:
    sys.path.insert(0, str(script_dir))

from card_generator import CardBuilder, CardError, fonts_installed, install_fonts
from config_manager import ConfigManager
from utils import Logger


def read_front_matter(file_path: Path) -> Dict[str, Any]:
    content = file_path.read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?\n)---\s*\n", content, re.DOTALL)
    if not match:
        return {}
    try:
        return yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError:
        return {}


def puppeteer_config(root_dir: Path) -> Optional[Path]:
    """Optional Puppeteer config for Mermaid CLI (for example to pass --no-sandbox in CI)."""
    if os.environ.get("PUPPETEER_CONFIG"):
        return Path(os.environ["PUPPETEER_CONFIG"])
    default = root_dir / "puppeteer-config.json"
    return default if default.exists() else None


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate standalone 16:9 GitFichas cards")
    parser.add_argument("filter", nargs="?", help="Only posts whose filename contains this text, for example 028")
    parser.add_argument("--lang", choices=["pt", "en", "es"], help="Only one language")
    parser.add_argument("--force", "-f", action="store_true", help="Regenerate cards that already exist")
    parser.add_argument("--png", action="store_true", help="Also export a 1920x1080 PNG next to each SVG")
    parser.add_argument("--output", help="Output directory (default: assets/img/cards)")
    parser.add_argument("--install-fonts", action="store_true", help="Install the card fonts for this user and exit")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    args = parser.parse_args()

    config = ConfigManager(".")
    logger = Logger(args.verbose)

    if args.install_fonts:
        target = install_fonts(config.fonts_dir)
        logger.success(f"Fonts installed in {target}")
        return 0

    missing = fonts_installed()
    if missing:
        logger.failure(f"Fonts not installed: {', '.join(missing)}")
        print("  Mermaid needs them to measure text. Run: python3 scripts/generate_cards.py --install-fonts")
        return 1

    config.validate_theme_file()
    if args.output:
        config.cards_dir = Path(args.output)
    builder = CardBuilder(config.fonts_dir, config.theme_path, puppeteer_config(config.root_dir))

    generated = skipped = failed = 0
    for posts_dir in config.posts_dirs:
        if not posts_dir.exists():
            continue
        for file_path in sorted(posts_dir.glob("*.md")):
            if args.filter and args.filter not in file_path.name:
                continue
            front_matter = read_front_matter(file_path)
            if not front_matter.get("mermaid"):
                continue
            if args.lang and str(front_matter.get("lang", "pt")) != args.lang:
                continue

            svg_path = config.get_card_path(front_matter, file_path)
            png_path = svg_path.with_suffix(".png")
            needs_svg = args.force or not svg_path.exists()
            needs_png = args.png and (needs_svg or not png_path.exists())
            if not needs_svg and not needs_png:
                logger.info(f"  Skipping {file_path}: card already exists")
                skipped += 1
                continue

            try:
                builder.warnings.clear()
                if needs_svg:
                    builder.write_svg(front_matter, svg_path)
                if needs_png:
                    builder.write_png(svg_path, png_path)
                logger.success(f"{svg_path}" + (" (+ png)" if needs_png else ""))
                for warning in builder.warnings:
                    logger.warning(f"{svg_path.name}: {warning}")
                generated += 1
            except CardError as error:
                logger.failure(f"{file_path}: {error}")
                failed += 1

    print("\n=== Summary ===")
    print(f"Cards generated: {generated}")
    print(f"Skipped: {skipped}")
    print(f"Failed: {failed}")
    if generated:
        print(f"\n✅ Cards are in: {config.cards_dir}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
