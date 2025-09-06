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
python3 generate_images_only.py
```

## 📁 Files Structure

```
├── generate_images_only.py           # New non-destructive script
├── generate_mermaid_images.py        # Original script (destructive)
├── generate_mermaid_images_v2.py     # Enhanced original (destructive)
├── _includes/mermaid-graphs.html     # Updated with smart detection
└── assets/img/mermaid/              # Generated static images
    ├── 053.png                      # Portuguese version
    ├── 053-en.png                   # English version
    └── ...
```

## 🚀 Usage

### Basic Usage

```bash
# Generate images for all Mermaid posts
python3 generate_images_only.py

# Generate images for specific posts
python3 generate_images_only.py "053.md"

# Verbose output
python3 generate_images_only.py --verbose

# Force regeneration of existing images
python3 generate_images_only.py --force
```

### Step-by-Step Migration

1. **Generate static images:**
   ```bash
   python3 generate_images_only.py "053.md"
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

## 📋 Requirements

### System Dependencies
- **Node.js and npm**
- **System libraries for headless Chrome:**
  ```bash
  sudo apt-get install -y libasound2t64 libatk-bridge2.0-0t64 libatk1.0-0t64 libdrm2 libgtk-3-0t64 libgbm1
  ```

### Python Dependencies
```bash
pip install PyYAML
```

### Mermaid CLI
Auto-installed by the script:
```bash
npm install -g @mermaid-js/mermaid-cli
```

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
- Generate all images at once: `python3 generate_images_only.py`
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

1. **Image not loading:**
   - Check if image file exists in `assets/img/mermaid/`
   - Verify filename matches pattern: `{number}.png` or `{number}-en.png`

2. **Still seeing dynamic rendering:**
   - Ensure `use_static_image: true` is in front matter
   - Check Jekyll server logs for errors

3. **Image generation fails:**
   - Install required system libraries
   - Check Mermaid CLI installation: `npx @mermaid-js/mermaid-cli --version`

### Debug Mode
```bash
python3 generate_images_only.py --verbose "053.md"
```

## 🔮 Future Enhancements

- [ ] Automatic detection of outdated images
- [ ] Batch front matter updates
- [ ] Performance monitoring integration
- [ ] SVG output support
- [ ] Custom image dimensions per post

## 🎉 Benefits Summary

### Performance
- ⚡ Faster page loads (no client-side rendering)
- 📱 Better mobile experience
- 🔋 Reduced CPU usage on client devices

### Reliability
- 🌐 Works without JavaScript
- 🔒 Consistent rendering across browsers
- 📱 Better accessibility support

### Development
- 🛡️ Non-destructive migration
- 🔄 Easy rollback (just remove the flag)
- 🧪 A/B testing friendly

## 📝 License

MIT License - Feel free to adapt for your own Jekyll sites!
