# Mermaid to Static SVG Converter

Converts the Mermaid diagrams in the posts to static 16:9 SVG cards for the site, print and video.

## Prerequisites

- Python 3.7+
- Node.js 14+
- Jekyll (for local testing)

## Quick Start

```bash
bash scripts/setup.sh
```

## Manual Setup

If you can't run the setup script:

1. Install dependencies:
```bash
pip install -r requirements.txt
npm install -g @mermaid-js/mermaid-cli
```

2. On Linux, install Chrome dependencies:
```bash
sudo apt install -y libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libasound2
```

3. Install the card fonts:
```bash
python3 scripts/generate_cards.py --install-fonts
```

## How It Works

1. Add flag to post front matter:

```yaml
---
mermaid: true
use_static_image: true  # ← Add this line
---
```

2. Generate static images:

```bash
python3 scripts/generate_cards.py "053.md"
```

3. Test locally:

```bash
bundle exec jekyll serve
```

## Usage

```bash
# Generate images for all posts
python3 scripts/generate_cards.py

# Generate for specific posts
python3 scripts/generate_cards.py "053.md"

# Force regeneration of all images
python3 scripts/generate_cards.py --force

# Force regeneration of specific post
python3 scripts/generate_cards.py "053.md" --force

# Verbose output
python3 scripts/generate_cards.py --verbose
```

## The cards

`scripts/generate_cards.py` builds one self-contained card per Mermaid post in `assets/img/cards/`.
The site shows these cards through `_includes/mermaid-graphs.html`, which also builds the image alt text
from the post front matter (command, notes and info).

Every card:

- uses the same 16:9 canvas (1120x630 units, exported as 1920x1080 PNG) and the same text size
- includes the title block, the diagram, the card number and the signature
- uses a stacked layout for commands: one row per part with its note to the right, so long
  commands get taller instead of wider (up to 6 parts fit without shrinking)
- embeds only the glyphs it uses, so each SVG is around 40 to 100 KB

```bash
# Once per machine: Mermaid needs Borel and Chilanka installed to measure text
python3 scripts/generate_cards.py --install-fonts

# All cards that don't exist yet
python3 scripts/generate_cards.py

# One card in every language, regenerated
python3 scripts/generate_cards.py 028 --force

# One language, with a 1920x1080 PNG next to each SVG
python3 scripts/generate_cards.py 028 --lang pt --png
```

How it works:

1. `scripts/card_generator.py` writes Mermaid `block-beta` syntax from the front matter.
2. Mermaid CLI renders it.
3. The SVG is post-processed: tokens and notes are left-aligned, arrows are redrawn from the end
   of each word to the start of its note, and the diagram is centered on the canvas.
4. Title, pretitle, subtitle, number and signature are drawn as outlines from the fonts in
   `assets/fonts/`, using the same six color schemes as the site.

Notes:

- PNG export uses headless Chrome. Set `CHROME_PATH` if it is not found automatically.
- Set `PUPPETEER_CONFIG` (or add `puppeteer-config.json` to the project root) to pass a Puppeteer
  config to Mermaid CLI, for example to use `--no-sandbox` in CI.
- Sizes, spacing and the canvas are constants at the top of `scripts/card_generator.py`.

## Project Structure

```
gitfichas/
├── _posts/              # Markdown posts with mermaid diagrams
├── assets/img/cards/    # Generated 16:9 SVG cards
├── assets/fonts/        # Fonts used to build the cards
├── scripts/             # Setup and generation scripts
└── requirements.txt     # Python dependencies
```

## Example

**Input** (`_posts/2022-01-02-028.md`):
```yaml
---
pretitle: Usando
title: rebase
subtitle: pra corrigir um branch
command: git rebase --onto origem anterior branch
descriptors:
  - command: Comando para reaplicar commits
  - part1: Flag para indicar\na nova origem
  - part2: Branch ou commit\nque deve ser a origem
  - part3: Origem incorreta\ndo branch
  - part4: Branch que precisa\nde correção
number: "028"
author: "@jtemporal"
mermaid: true
use_static_image: true
lang: "pt"
---
```

**Output**: `assets/img/cards/028.svg` (`028-en.svg` and `028-es.svg` for the translations)

## Maintenance

Remove all generated images:
```bash
rm -rf assets/img/cards/*.svg
```

Regenerate everything:
```bash
python3 scripts/generate_cards.py --force
```

## Troubleshooting

**Browser launch fails:** Run `scripts/setup.sh` to install Chrome dependencies

**Missing fonts:** Run `python3 scripts/generate_cards.py --install-fonts`

**Image not showing:** Verify `use_static_image: true` is in front matter and SVG exists in `assets/img/cards/`

**Debug mode:** Use `--verbose` flag for detailed output

## License

MIT License - Feel free to adapt for your own Jekyll sites!