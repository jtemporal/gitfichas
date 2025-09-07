# GitFichas Devcontainer Configuration

This devcontainer provides a complete development environment for GitFichas with all dependencies pre-installed.

## What's Included

- **Base Image**: `mcr.microsoft.com/devcontainers/javascript-node`
- **Ruby 3.1**: For Jekyll development
- **Node.js**: For Mermaid CLI and front-end tools
- **Python**: For SVG generation scripts
- **System Dependencies**: Chrome libraries for headless browser support

## Automatic Setup

The `post-create.sh` script runs automatically and installs:

1. **System Dependencies**: Chrome/Puppeteer libraries for headless browser
2. **Python Dependencies**: PyYAML from `requirements.txt`
3. **Mermaid CLI**: Global installation via npm
4. **Embedded Fonts**: Generates base64 embedded fonts if needed
5. **Testing**: Validates the entire setup

## Port Forwarding

- **Port 4000**: Jekyll development server (auto-forwarded)

## VS Code Extensions

Pre-installed extensions for enhanced development:
- `yzhang.markdown-all-in-one`: Enhanced Markdown editing
- `ms-python.python`: Python development support
- `bradlc.vscode-tailwindcss`: CSS utilities
- `bierner.markdown-mermaid`: Mermaid diagram preview

## Usage

After the devcontainer starts:

```bash
# Start Jekyll server
bundle exec jekyll serve

# Generate Mermaid SVGs
cd scripts
python3 generate_images_only.py --verbose

# Generate embedded fonts
python3 generate_embedded_fonts.py
```

## Files

- `devcontainer.json`: Main devcontainer configuration
- `scripts/post-create.sh`: Automated setup script
