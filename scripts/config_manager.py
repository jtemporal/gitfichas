#!/usr/bin/env python3
"""
Configuration Manager for GitFichas Mermaid Generator
====================================================

Handles configuration, paths, and CSS management for the image generation system.
"""

import json
import re
from pathlib import Path
from typing import Dict, Any


class ConfigManager:
    """Manages configuration and paths for the Mermaid generator."""

    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir)
        self._setup_paths()
        self._setup_directories()

    def _setup_paths(self):
        """Setup all required paths."""
        # Post directories
        self.posts_dirs = [
            self.root_dir / "_posts",
            self.root_dir / "en" / "_posts",
            self.root_dir / "es" / "_posts"
        ]

        # Output directory
        self.images_dir = self.root_dir / "assets" / "img" / "mermaid"

        # CSS file paths
        self.base_mermaid_css_path = self.root_dir / 'assets' / 'css' / 'embedded-svg.css'
        self.embedded_fonts_css_path = self.root_dir / 'assets' / 'css' / 'embedded-fonts.css'
        self.combined_css_path = self.root_dir / 'combined-mermaid.css'

        # Theme configuration
        self.theme_path = self.root_dir / 'gitfichas-mermaid-theme.json'

        # Puppeteer configuration
        self.puppeteer_config_path = self.root_dir / 'puppeteer-config.json'

    def _setup_directories(self):
        """Create required directories if they don't exist."""
        self.images_dir.mkdir(parents=True, exist_ok=True)

    def validate_theme_file(self) -> None:
        """Validate that the standalone theme file exists and is valid JSON."""
        if not self.theme_path.exists():
            raise FileNotFoundError(
                f"Theme file not found: {self.theme_path}. "
                f"Please ensure gitfichas-mermaid-theme.json exists in the project root."
            )

        try:
            with open(self.theme_path, 'r', encoding='utf-8') as f:
                json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in theme file {self.theme_path}: {e}")

    def create_combined_css(self) -> Path:
        """Create combined CSS file with embedded fonts for Mermaid CLI."""
        try:
            # Read the embedded-svg.css file (which includes the @import for embedded fonts)
            with open(self.base_mermaid_css_path, 'r', encoding='utf-8') as f:
                svg_css = f.read()

            # Remove the @import line and replace with actual embedded fonts CSS
            svg_css_without_import = re.sub(r'^@import.*?;.*?\n', '', svg_css, flags=re.MULTILINE)

            # Read the embedded fonts CSS file directly
            embedded_fonts_css = ""
            if self.embedded_fonts_css_path.exists():
                with open(self.embedded_fonts_css_path, 'r', encoding='utf-8') as f:
                    embedded_fonts_css = f.read()

            # Combine: embedded fonts first, then SVG-specific CSS
            combined_css = embedded_fonts_css + "\n\n" + svg_css_without_import

            # Write combined CSS file
            with open(self.combined_css_path, 'w', encoding='utf-8') as f:
                f.write(combined_css)

            return self.combined_css_path

        except Exception as e:
            raise RuntimeError(f"Error creating combined CSS: {e}")

    def cleanup_temp_files(self):
        """Clean up temporary files."""
        self.combined_css_path.unlink(missing_ok=True)

    def get_mermaid_cli_command(self, temp_file: Path, output_path: Path) -> list:
        """Get the Mermaid CLI command arguments."""
        cmd = [
            'npx', '@mermaid-js/mermaid-cli',
            '-i', str(temp_file),
            '-o', str(output_path),
            '-b', 'white',
            '--width', '1200',
            '--height', '675',
            '-e', 'svg',
            '--configFile', str(self.theme_path),
            '--cssFile', str(self.combined_css_path)
        ]

        # Add puppeteer config if it exists
        if self.puppeteer_config_path.exists():
            cmd.extend(['-p', str(self.puppeteer_config_path)])

        return cmd

    def get_image_path(self, front_matter: Dict[str, Any], file_path: Path) -> Path:
        """Determine the output image path based on front matter and file path."""
        number = front_matter.get('number', file_path.stem.split('-')[-1])
        lang = front_matter.get('lang', 'pt')

        if lang == 'en':
            image_filename = f"{number}-en.svg"
        elif lang == 'es':
            image_filename = f"{number}-es.svg"
        else:
            image_filename = f"{number}.svg"

        return self.images_dir / image_filename
