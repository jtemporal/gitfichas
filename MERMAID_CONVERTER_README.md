# Mermaid to Static SVG Converter

This tool converts dynamic Mermaid diagrams to static SVG images for better performance and accessibility.

## 🎯 Key Benefits

- ✅ **Non-destructive**: Original markdown files remain untouched
- ✅ **Gradual migration**: Convert posts one by one as needed
- ✅ **Fallback support**: Dynamic rendering still works for unconverted posts
- ✅ **Performance boost**: Static images load faster and reduce JavaScript overhead
- ✅ **Better SEO**: Images are accessible to search engines and work without JavaScript
- ✅ **SVG format**: Vector graphics scale perfectly at any size and are accessible to screen readers

## 🔧 How It Works

### 1. Jekyll Include Logic
The `_includes/mermaid-graphs.html` file now includes smart detection logic:

```liquid
{% if page.use_static_image %}
  <img src="/assets/img/mermaid/{{ page.number }}.svg" alt="{{ page.title }}" class="mermaid-image" />
{% elsif page.command %}
  <!-- Original dynamic Mermaid rendering -->
{% endif %}
```

### 2. Opt-in Conversion
To convert a post to use static images, simply add one line to its front matter:

```yaml
---
layout: post
title: commit
mermaid: true
use_static_image: true  # ← Add this line
---
```

### 3. Image Generation
Run the script to generate images for posts that need them:

```bash
python3 scripts/generate_images_only.py
```

## 📁 Files Structure

```
├── scripts/                          # Modular script architecture
│   ├── generate_images_only.py       # Main non-destructive script
│   ├── generate_embedded_fonts.py    # Font embedding utility
│   ├── mermaid_generator.py          # Mermaid diagram generation logic
│   ├── config_manager.py             # Configuration and path management
│   ├── utils.py                      # Statistics tracking and logging
│   └── setup-mermaid.sh              # Automated setup script for new codespaces
├── requirements.txt                  # Python dependencies
├── generate_mermaid_images.py        # Original script (destructive)
├── generate_mermaid_images_v2.py     # Enhanced original (destructive)
├── _includes/mermaid-graphs.html     # Updated with smart detection
├── assets/css/
│   ├── mermaid.css                   # Web-specific styles
│   ├── embedded-svg.css              # SVG-specific styles
│   └── embedded-fonts.css            # Base64 embedded fonts (auto-generated)
├── gitfichas-mermaid-theme.json      # Standalone theme configuration
└── assets/img/mermaid/              # Generated static images
    ├── 053.svg                      # Portuguese version (SVG format)
    ├── 053-en.svg                   # English version (SVG format)
    └── ...
```

## 🚀 Usage

### Script Architecture

The generator uses a **modular architecture** for better maintainability:

- **`generate_images_only.py`**: Main orchestrator script
- **`mermaid_generator.py`**: Handles Mermaid syntax generation from front matter
- **`config_manager.py`**: Manages paths, CSS files, and CLI configuration
- **`utils.py`**: Provides statistics tracking and logging utilities
- **`generate_embedded_fonts.py`**: Separate utility for font embedding

This modular design makes the code more:
- 📦 **Maintainable**: Each module has a single responsibility
- 🧪 **Testable**: Components can be tested independently
- 🔧 **Extensible**: Easy to add new diagram types or features
- 🐛 **Debuggable**: Issues are easier to isolate and fix

### Basic Usage

```bash
# Generate images for all Mermaid posts
python3 scripts/generate_images_only.py

# Generate images for specific posts
python3 scripts/generate_images_only.py "053.md"

# Verbose output
python3 scripts/generate_images_only.py --verbose

# Force regeneration of existing images
python3 scripts/generate_images_only.py --force
```

### Step-by-Step Migration

1. **Generate static images:**
   ```bash
   python3 scripts/generate_images_only.py "053.md"
   ```

2. **Add opt-in flag to post front matter:**
   ```yaml
   use_static_image: true
   ```

3. **Test the result:**
   - Visit the post in your browser
   - Verify the image loads correctly
   - Check that styling is preserved

4. **Repeat for other posts as needed**

### Font Management

The system uses **embedded Google Fonts** (Chilanka and Borel) for consistent rendering:

```bash
# Generate embedded fonts (run when fonts need updating)
python3 scripts/generate_embedded_fonts.py

# Regenerate all SVG images with new fonts
python3 scripts/generate_images_only.py --force
```

**Font Architecture:**
- **`embedded-fonts.css`**: Base64-encoded font definitions (auto-generated)
- **`embedded-svg.css`**: SVG-specific styles that import embedded fonts
- **`mermaid.css`**: Web-specific styles for interactive diagrams

This separation ensures:
- ✅ **Consistent rendering** across all platforms
- ✅ **No external font dependencies** in SVG files
- ✅ **Faster loading** with embedded fonts
- ✅ **Offline compatibility** for generated images

## 📋 Requirements

### Quick Setup for New Codespaces

If you're setting up in a fresh codespace, you can use the automated setup script:

```bash
# Automated setup (recommended) - can be run from anywhere
scripts/setup-mermaid.sh
```

Or manually run this setup sequence:

```bash
# 1. Ensure Node.js and npm are available (usually pre-installed in Codespaces)
node --version && npm --version

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Install Mermaid CLI globally
npm install -g @mermaid-js/mermaid-cli

# 4. Generate embedded fonts (if not already present)
python3 scripts/generate_embedded_fonts.py

# 5. Test the setup
python3 scripts/generate_images_only.py --help
```

### System Dependencies
- **Node.js and npm** (usually pre-installed in GitHub Codespaces)
- **System libraries for headless Chrome:**
  ```bash
  sudo apt-get update
  sudo apt-get install -y libasound2t64 libatk-bridge2.0-0t64 libatk1.0-0t64 libdrm2 libgtk-3-0t64 libgbm1
  ```

### Python Dependencies
- **PyYAML** (usually pre-installed)
  ```bash
  pip install PyYAML
  ```

### Mermaid CLI
Auto-installed by the script, but can be manually installed:
```bash
npm install -g @mermaid-js/mermaid-cli
```

### Required Files
The following files must exist for the script to work:
- `gitfichas-mermaid-theme.json` (theme configuration)
- `assets/css/embedded-fonts.css` (generated by `generate_embedded_fonts.py`)
- `assets/css/embedded-svg.css` (SVG-specific styles)

## 🎨 Styling

The CSS has been updated to support both approaches:

```css
/* For dynamic Mermaid diagrams */
.mermaid {
    /* existing styles */
}

/* For static images */
.mermaid-image {
    margin-top: 2vh;
    background-color: transparent;
    border: none;
    width: 80vw;
    max-height: 65vh;
    object-fit: contain;
    text-align: center;
    width: 100%;
}
```

## 🔄 Migration Strategies

### Strategy 1: Gradual Migration (Recommended)
- Convert high-traffic posts first
- Test each conversion thoroughly
- Keep original rendering for less critical posts

### Strategy 2: Bulk Migration
- Generate all images at once: `python3 scripts/generate_images_only.py`
- Add `use_static_image: true` to all posts programmatically
- Test thoroughly before deploying

### Strategy 3: A/B Testing
- Convert a subset of posts
- Compare performance metrics
- Gradually expand based on results

## 🧪 Testing

### Test Individual Posts
```bash
# Start Jekyll server
bundle exec jekyll serve

# Visit converted posts
# Portuguese: http://localhost:4000/projects/053
# English: http://localhost:4000/en/053
```

### Verify Both Modes Work
1. **Static image mode:** Post with `use_static_image: true`
2. **Dynamic mode:** Post without the flag

Both should render identically!

## 📊 Example Conversion

**Before (Dynamic):**
```yaml
---
mermaid: true
---
{% include mermaid-graphs.html %}
```

**After (Static):**
```yaml
---
mermaid: true
use_static_image: true
---
{% include mermaid-graphs.html %}
```

The include automatically detects the flag and serves the static image!

## 🐛 Troubleshooting

### Common Issues

1. **Import errors in new codespace:**
   ```bash
   # Error: ModuleNotFoundError: No module named 'config_manager'
   # Solution: The script now auto-fixes Python path, but ensure you're running from project root
   cd /workspaces/gitfichas
   python3 scripts/generate_images_only.py --help
   ```

2. **Missing embedded-fonts.css:**
   ```bash
   # Error: FileNotFoundError: embedded-fonts.css not found
   # Solution: Generate the embedded fonts first
   python3 scripts/generate_embedded_fonts.py
   ```

3. **Missing theme configuration:**
   ```bash
   # Error: Theme file not found: gitfichas-mermaid-theme.json
   # Solution: Ensure the theme file exists in project root
   ls -la gitfichas-mermaid-theme.json
   ```

4. **Mermaid CLI not found:**
   ```bash
   # Error: npx: @mermaid-js/mermaid-cli command not found
   # Solution: Install Mermaid CLI globally
   npm install -g @mermaid-js/mermaid-cli
   ```

5. **Image not loading:**
   - Check if image file exists in `assets/img/mermaid/`
   - Verify filename matches pattern: `{number}.svg` or `{number}-en.svg`
   - Ensure the SVG format is being used (not PNG)

2. **Still seeing dynamic rendering:**
   - Ensure `use_static_image: true` is in front matter
   - Check Jekyll server logs for errors
   - Verify image file was generated successfully

3. **Image generation fails:**
   - Install required system libraries
   - Check Mermaid CLI installation: `npx @mermaid-js/mermaid-cli --version`
   - Verify theme file exists: `gitfichas-mermaid-theme.json`
   - Check embedded fonts: `assets/css/embedded-fonts.css`

4. **Font rendering issues:**
   - Regenerate embedded fonts: `python3 scripts/generate_embedded_fonts.py`
   - Force regenerate images: `python3 scripts/generate_images_only.py --force`

5. **Module import errors:**
   - Ensure all scripts are in the `scripts/` directory
   - Check that Python path includes the scripts directory
   - Verify all module files exist: `config_manager.py`, `mermaid_generator.py`, `utils.py`

### Debug Mode
```bash
# Verbose output for detailed debugging
python3 scripts/generate_images_only.py --verbose "053.md"

# Test individual components
python3 -c "
import sys; sys.path.append('scripts')
from mermaid_generator import MermaidDiagramGenerator
print('✓ Mermaid generator working')
"
```

### Development Testing
```bash
# Test the modular architecture
cd scripts
python3 -c "
from config_manager import ConfigManager
from utils import StatsTracker, Logger
print('✓ All modules importing correctly')
"
```

## 🎉 Benefits Summary

### Performance
- ⚡ **Faster page loads** (no client-side rendering)
- 📱 **Better mobile experience**
- 🔋 **Reduced CPU usage** on client devices
- 🎯 **SVG format** for perfect scaling and accessibility

### Reliability
- 🌐 **Works without JavaScript**
- 🔒 **Consistent rendering** across browsers
- 📱 **Better accessibility** support
- 🎨 **Embedded fonts** ensure consistent typography

### Development
- 🛡️ **Non-destructive migration**
- 🔄 **Easy rollback** (just remove the flag)
- 🧪 **A/B testing friendly**
- 📦 **Modular architecture** for easier maintenance
- 🔧 **Extensible design** for future enhancements
- 🐛 **Better debugging** with separated concerns
- 📊 **Comprehensive logging** and statistics tracking

## 📝 License

MIT License - Feel free to adapt for your own Jekyll sites!
