#!/usr/bin/env python3
"""
Generate embedded fonts CSS file for GitFichas
==============================================

This script downloads Google Fonts and creates a CSS file with base64 embedded fonts
that can be used for SVG generation without requiring external font downloads.

Usage:
    python3 scripts/generate_embedded_fonts.py

Output:
    assets/css/embedded-fonts.css

Author: GitHub Copilot
License: MIT
"""

import requests
import base64
import re
from pathlib import Path

def download_and_embed_fonts() -> str:
    """Download Google Fonts and return base64 embedded CSS."""
    fonts_to_embed = [
        "https://fonts.googleapis.com/css2?family=Chilanka&display=swap",
        "https://fonts.googleapis.com/css2?family=Borel&display=swap"
    ]

    embedded_css = "/* Embedded Google Fonts for GitFichas SVG generation */\n"
    embedded_css += "/* Generated automatically - do not edit manually */\n\n"

    for font_url in fonts_to_embed:
        try:
            print(f"Downloading font from: {font_url}")

            # Get the CSS file
            response = requests.get(font_url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            css_content = response.text

            # Find all font URLs in the CSS
            font_urls = re.findall(r'url\((https://[^)]+)\)', css_content)

            print(f"  Found {len(font_urls)} font files to embed")

            # Download each font file and replace with base64
            for i, font_file_url in enumerate(font_urls):
                print(f"  Downloading font file {i+1}/{len(font_urls)}: {font_file_url.split('/')[-1]}")
                font_response = requests.get(font_file_url)
                if font_response.status_code == 200:
                    # Convert to base64
                    font_base64 = base64.b64encode(font_response.content).decode('utf-8')

                    # Determine font format from URL
                    if '.woff2' in font_file_url:
                        format_type = 'woff2'
                    elif '.woff' in font_file_url:
                        format_type = 'woff'
                    elif '.ttf' in font_file_url:
                        format_type = 'truetype'
                    else:
                        format_type = 'woff2'  # default

                    data_url = f"data:font/{format_type};base64,{font_base64}"
                    css_content = css_content.replace(font_file_url, data_url)
                    print(f"    ✓ Embedded {len(font_base64)} characters of base64 data")
                else:
                    print(f"    ✗ Failed to download: {font_response.status_code}")

            embedded_css += f"/* {font_url} */\n"
            embedded_css += css_content + "\n\n"
            print(f"✓ Successfully embedded fonts from: {font_url}")

        except Exception as e:
            print(f"✗ Error embedding font {font_url}: {e}")
            continue

    return embedded_css

def main():
    """Main function to generate embedded fonts CSS."""
    print("GitFichas Embedded Fonts Generator")
    print("=================================\n")

    # Generate embedded fonts CSS
    embedded_css = download_and_embed_fonts()

    # Write to assets/css/embedded-fonts.css
    output_path = Path("assets/css/embedded-fonts.css")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(embedded_css)

    print(f"\n✅ Embedded fonts saved to: {output_path}")
    print(f"   File size: {output_path.stat().st_size / 1024:.1f} KB")
    print("\nYou can now use this file for SVG generation without downloading fonts each time!")


if __name__ == "__main__":
    main()
