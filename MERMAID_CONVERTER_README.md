# Mermaid to Static SVG Converter

Converts dynamic Mermaid diagrams to static SVG images for better performance and accessibility.

## Quick Start

```bash
bash scripts/setup.sh
```

## How It Works

1. **Add flag to post front matter:**
   ```yaml
   ---
   mermaid: true
   use_static_image: true  # ← Add this line
   ---
   ```

2. **Generate static images:**
   ```bash
   python3 scripts/generate_images_only.py "053.md"
   ```

3. **Test locally:**
   ```bash
   bundle exec jekyll serve
   ```

## Usage

```bash
# Generate images for all posts
python3 scripts/generate_images_only.py

# Generate for specific posts
python3 scripts/generate_images_only.py "053.md"

# Force regeneration of all cards
python3 scripts/generate_images_only.py --force

# Force regeneration of a specic card
python3 scripts/generate_images_only.py "053.md" --force

# Verbose output
python3 scripts/generate_images_only.py --verbose
```

## Setup Requirements

The setup script handles everything automatically, but manual setup requires:

- Node.js and npm
- Python dependencies: `pip install -r requirements.txt`
- Mermaid CLI: `npm install -g @mermaid-js/mermaid-cli`
- System libraries for headless Chrome (auto-installed by setup script)

## Troubleshooting

**Browser launch fails:** Run `scripts/setup.sh` to install Chrome dependencies

**Missing fonts:** Run `python3 scripts/generate_embedded_fonts.py`

**Image not showing:** Verify `use_static_image: true` is in front matter and SVG exists in `assets/img/mermaid/`

**Debug mode:** Use `--verbose` flag for detailed output

MIT License - Feel free to adapt for your own Jekyll sites!
