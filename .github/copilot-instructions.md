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
- `pretitle` (optional) - for additional context before the title
- `title` (mandatory) - main card title
- `subtitle` (optional) - descriptive subtitle, can be blank
- `command` (mandatory) - the actual git command
- `descriptors` (mandatory) - descriptions for command parts
  - `command`: description of the main git command
  - `part1`, `part2`, etc.: descriptions for each command part
- `number` (mandatory) - card number with quotes for leading zeros
- `author` (mandatory) - GitHub username with @
- `mermaid: true` (mandatory)
- `use_static_image: true` (mandatory only when SVG image is generated)
- `permalink` (mandatory) - `/projects/{number}` for PT, `/en/{number}` for EN, `/es/{number}` for ES
- `lang` (mandatory) - "pt", "en", or "es"
- `pv` and `nt` (mandatory) - previous/next card navigation
- `{% include mermaid-graphs.html %}` at the end

#### Concept Cards Must Include:
- `layout: post` (mandatory)
- `pretitle` (optional) - for additional context before the title
- `title` (mandatory) - main concept title
- `subtitle` (optional) - can be blank
- `concept: true` (mandatory)
- `parts` (mandatory) - concept descriptions
  - `part1`, `part2`, etc.: individual concept explanations
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
- Spanish posts: `{number}-es.svg` (e.g., `053-es.svg`)
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
- Support multiple languages: PT (Portuguese), EN (English), and ES (Spanish)
- Use `lang: "pt"` for Portuguese cards in `_posts/`
- Use `lang: "en"` for English cards in `en/_posts/`
- Use `lang: "es"` for Spanish cards in `es/_posts/`
- Include `translations` array linking to other language versions when available
- Supported language codes: "pt", "en", "es"

### Code Quality
- **Remove all trailing whitespaces** from files before committing
- Ensure consistent formatting and clean code standards

## Migrating cards from images to Mermaid

After migrating the content in the markdown files, you need to convert the existing image-based cards to the new Mermaid format.

**Important workflow:**

1. **Ensure proper file naming**: Use `YYYY-MM-DD-XXX.md` format with same date as original post for translations
2. **Generate SVG first**: Run image generation script one card at a time:
   ```bash
   python3 scripts/generate_images_only.py "filename.md"
   ```
3. **Add use_static_image only after successful SVG generation**: Add `use_static_image: true` to front matter ONLY after SVG is successfully created
4. **Test locally**: Run server and verify diagrams render correctly compared to previous image-based cards
5. **Commit together**: Stage and commit both the post changes AND the generated SVG files together

At the end ask to stage the changes and commit both the post changes AND the generated SVG files together

### Command Cards
This is what a Mermaid card looks like:

```markdown
---
layout: post
pretitle:
title: Adicionando
subtitle: arquivos para commit
command: git add arquivo.txt
descriptors:
  - command: comando para adicionar um ou<br>mais arquivos em staging
  - part1: nome de um ou mais arquivos
author: "@jtemporal"
number: "002"
mermaid: true
use_static_image: true
translations:
- lang: en
  url: /en/002
permalink: "/projects/002"
lang: "pt"
pv:
  url: "/projects/001"
  title: "#001 git init"
nt:
  url: "/projects/003"
  title: "#003 git commit -m 'alterações'"
---

{% include mermaid-graphs.html %}
```
This is the same card using the previous image-based format:

```markdown
---
layout: post
title: '#002 git add arquivo.txt'
image: "https://res.cloudinary.com/jesstemporal/image/upload/f_auto/v1642878670/gitfichas/pt/002/thumbnail_igi5fw.jpg"
permalink: "/projects/002"
translations:
- lang: en
  url: /en/002
lang: "pt"
pv:
  url: "/projects/001"
  title: "#001 git init"
nt:
  url: "/projects/003"
  title: "#003 git commit -m ‘alterações’"
---

##### Adicionando arquivos para commit

<img alt="Para adicionar arquivos para commit use o git add seguido do nome do arquivo" src="https://res.cloudinary.com/jesstemporal/image/upload/v1642878670/gitfichas/pt/002/full_zy7yy7.jpg"><br><br>

| Comando | Descrição |
|---------|-------------|
| `add` | Comando para adicionar um ou mais arquivos em staging |
| `arquivo.txt` | Nome de um ou mais arquivos |
{: .styled-table}
```

Note the differences:
- The command section is added with the actual git command
- The descriptors section will hold a command and part1 (and part[index] if needed) for each part of the command
- Descriptors that are longer than 30 characters should use `<br>` for line breaks in HTML contexts or `\n` for line breaks in other contexts
- The image section is removed
- The subtitle is added even if no subtitle is needed (it can be left blank)
- The pretitle can be used for additional context (also can be left blank)
- Add `mermaid: true` and `use_static_image: true` (only after SVG is generated)

### Concept cards

This is what a Mermaid concept card looks like:

```markdown
---
layout: post
pretitle: o que é o ambiente de
title: staging
subtitle:
concept: true
parts:
  - part1: é a área de preparação para commits
  - part2: onde vemos a coleção de arquivos alterados ou criados \nque farão parte do próximo commit
number: "005"
author: "@jtemporal"
mermaid: true
permalink: "/projects/005"
translations:
- lang: en
  url: /en/005
lang: "pt"
pv:
  url: "/projects/004"
  title: "#004 git show"
nt:
  url: "/projects/006"
  title: "#006 git status"
---

{% include mermaid-graphs.html %}
```

Note the differences for concept cards:
- Use `concept: true` instead of `command`
- Use `parts` array instead of `descriptors`
- Each part is numbered: `part1`, `part2`, etc.
- Line breaks in parts use `\n` for longer descriptions
