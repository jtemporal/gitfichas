## Jekyll Development
- Always start the jekyll server with `bundle exec jekyll serve` no extra flags.

## Contributing Guidelines for GitFichas
When working on this GitFichas (Git Study Cards) project, follow these guidelines:

### New Mermaid Posts
- **Always run SVG generation** after creating or modifying posts with mermaid diagrams
- Use the command: `python3 scripts/generate_images_only.py`
- For specific posts: `python3 scripts/generate_images_only.py "filename.md"`
- Use `--force` flag to regenerate existing images: `python3 scripts/generate_images_only.py --force`
- Use `--verbose` flag for detailed debugging output when troubleshooting
- **Offer to run the script** when helping users create new mermaid posts
- Commit both the post changes AND the generated SVG files
- Generated SVG files are stored in `assets/img/mermaid/` directory

### Post Templates
Follow the templates from CONTRIBUTING.md exactly:

#### Command Cards Must Include:
- `layout: post` (mandatory)
- `title` (mandatory)
- `command` (mandatory) - the actual git command
- `descriptors` (mandatory) - descriptions for command parts
- `number` (mandatory) - card number with quotes for leading zeros
- `author` (mandatory) - GitHub username with @
- `mermaid: true` (mandatory)
- `use_static_image: true` (mandatory for new posts)
- `permalink` (mandatory) - `/projects/{number}` for PT, `/en/{number}` for EN
- `lang` (mandatory) - either "pt" or "en"
- `pv` and `nt` (mandatory) - previous/next card navigation
- `{% include mermaid-graphs.html %}` at the end

#### Concept Cards Must Include:
- `layout: post` (mandatory)
- `title` (mandatory)
- `concept: true` (mandatory)
- `parts` (mandatory) - concept descriptions
- Same metadata as command cards (number, author, mermaid, etc.)

### Development Workflow
1. **Setup**: Recommend running `bash scripts/setup.sh` for new environments
   - This installs Node.js dependencies, Python packages, system libraries for headless Chrome, and Mermaid CLI
   - Auto-configures the entire development environment
2. **Create/Edit Posts**: Follow templates exactly
3. **Generate SVGs**: Always run `python3 scripts/generate_images_only.py`
4. **Test Locally**: Use `bundle exec jekyll serve` (no extra flags)
5. **Commit**: Include both post and generated SVG files

### Project Structure
- Posts with mermaid diagrams generate SVG files in `assets/img/mermaid/`
- Portuguese posts: `{number}.svg` (e.g., `053.svg`)
- English posts: `{number}-en.svg` (e.g., `053-en.svg`)
- Theme configuration: `gitfichas-mermaid-theme.json`
- CSS files: `assets/css/mermaid.css`, `assets/css/embedded-svg.css`, `assets/css/embedded-fonts.css`

### Troubleshooting
- If SVG generation fails, ensure system dependencies are installed via `bash scripts/setup.sh`
- For browser launch errors, check that headless Chrome libraries are installed
- Missing fonts issue: run `python3 scripts/generate_embedded_fonts.py` first
- Use `--verbose` flag for detailed debugging information

### Card Numbering
- Use sequential numbering with leading zeros in quotes: `"053"`
- Check existing posts to find the next available number
- Update previous/next navigation links appropriately

### Languages
- Support PT (Portuguese) and EN (English) only
- Use `lang: "pt"` for Portuguese cards in `_posts/`
- Use `lang: "en"` for English cards in `en/_posts/`
- Include `translated` field linking to other language version when available

### Code Quality
- **Remove all trailing whitespaces** from files before committing
- Ensure consistent formatting and clean code standards
