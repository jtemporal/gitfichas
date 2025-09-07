#!/usr/bin/env python3
"""
GitFichas Mermaid Image Generator (Non-Destructive)
===================================================

This script generates static SVG images from Mermaid diagrams in Jekyll posts
WITHOUT modifying the original markdown files.

The Jekyll include file (_includes/mermaid-graphs.html) has been updated to
automatically detect and use static images when available, falling back to
dynamic rendering when not.

Usage:
    python3 scripts/generate_images_only.py [filter]

Examples:
    python3 scripts/generate_images_only.py           # Generate images for all mermaid posts
    python3 scripts/generate_images_only.py "053.md"  # Generate images only for posts with "053.md" in filename

Author: GitHub Copilot
License: MIT
"""

import os
import re
import yaml
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional

# Import our new modules
from config_manager import ConfigManager
from mermaid_generator import MermaidDiagramGenerator
from utils import StatsTracker, Logger


class MermaidImageOnlyGenerator:
    """Main generator class that orchestrates the image generation process."""

    def __init__(self, root_dir: str = ".", verbose: bool = False):
        self.config = ConfigManager(root_dir)
        self.stats = StatsTracker()
        self.logger = Logger(verbose)

        # Initialize configuration
        self._initialize()

    def _initialize(self):
        """Initialize the generator by validating configuration and creating CSS."""
        try:
            self.config.validate_theme_file()
            self.logger.info(f"✓ Using theme file: {self.config.theme_path}")

            self.config.create_combined_css()
            self.logger.info(f"✓ Created combined CSS file: {self.config.combined_css_path}")

        except Exception as e:
            self.logger.error(f"Initialization failed: {e}")
            raise

    def extract_front_matter(self, content: str) -> tuple[Dict[str, Any], str]:
        """Extract YAML front matter from markdown content."""
        pattern = r'^---\s*\n(.*?\n)---\s*\n(.*)$'
        match = re.match(pattern, content, re.DOTALL)

        if not match:
            return {}, content

        front_matter_str = match.group(1)
        body = match.group(2)

        try:
            front_matter = yaml.safe_load(front_matter_str)
            return front_matter or {}, body
        except yaml.YAMLError as e:
            self.logger.error(f"Error parsing YAML: {e}")
            return {}, content

    def generate_image(self, mermaid_syntax: str, output_path: Path) -> bool:
        """Generate image from Mermaid syntax using Mermaid CLI."""
        try:
            # Create temporary file for mermaid syntax
            temp_file = output_path.with_suffix('.mmd')
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(mermaid_syntax)

            # Get command from config manager
            cmd = self.config.get_mermaid_cli_command(temp_file, output_path)

            result = subprocess.run(cmd, capture_output=True, text=True)

            # Clean up temporary mermaid file
            temp_file.unlink(missing_ok=True)

            if result.returncode == 0:
                self.logger.success(f"Generated image: {output_path}")
                return True
            else:
                self.logger.error(f"Error generating image: {result.stderr}")
                return False

        except Exception as e:
            self.logger.error(f"Exception generating image: {e}")
            return False

        except Exception as e:
            self.log(f"✗ Exception generating image: {e}", "ERROR")
            return False

    def process_file(self, file_path: Path, force: bool = False) -> bool:
        """Process a single markdown file - ONLY generate image, don't modify file."""
        self.logger.info(f"\nProcessing: {file_path}")

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            front_matter, body = self.extract_front_matter(content)

            if not front_matter.get('mermaid', False):
                self.logger.info(f"  Skipping: Not a mermaid post")
                self.stats.increment_skipped()
                return False

            # Generate mermaid syntax using the new generator
            mermaid_syntax = MermaidDiagramGenerator.generate_from_front_matter(front_matter)
            if not mermaid_syntax:
                self.logger.info(f"  Skipping: Could not generate mermaid syntax")
                self.stats.increment_skipped()
                return False

            # Determine output image path using config manager
            image_path = self.config.get_image_path(front_matter, file_path)

            # Check if image already exists
            if image_path.exists() and not force:
                self.logger.info(f"  Image already exists: {image_path}")
                self.stats.increment_skipped()
                return False

            # Generate image (no file modification!)
            if self.generate_image(mermaid_syntax, image_path):
                self.stats.increment_success()
                return True
            else:
                self.stats.increment_errors()
                return False

        except Exception as e:
            self.logger.error(f"Error processing {file_path}: {e}")
            self.stats.increment_errors()
            return False

    def process_files(self, filename_filter: Optional[str] = None, force: bool = False) -> None:
        """Process all markdown files or those matching the filter."""

        for posts_dir in self.config.posts_dirs:
            if not posts_dir.exists():
                continue

            self.logger.info(f"\nProcessing directory: {posts_dir}")

            for file_path in posts_dir.glob("*.md"):
                if filename_filter and filename_filter not in file_path.name:
                    # Also check in file content for more flexible filtering
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            if filename_filter.lower() not in content.lower():
                                continue
                    except:
                        continue

                self.stats.increment_processed()
                self.process_file(file_path, force)

        self.print_summary()

    def print_summary(self):
        """Print processing summary."""
        self.stats.print_summary(self.config.images_dir)

        # Clean up temporary files
        self.config.cleanup_temp_files()

def check_dependencies():
    """Check if required dependencies are available."""
    # Check if mermaid CLI is available
    try:
        result = subprocess.run(['npx', '@mermaid-js/mermaid-cli', '--version'],
                              capture_output=True, text=True)
        if result.returncode != 0:
            print("Installing Mermaid CLI...")
            subprocess.run(['npm', 'install', '-g', '@mermaid-js/mermaid-cli'], check=True)
            print("✓ Mermaid CLI installed successfully")
    except subprocess.CalledProcessError:
        print("Error: Could not install Mermaid CLI. Please install Node.js and npm first.")
        sys.exit(1)
    except FileNotFoundError:
        print("Error: Node.js/npm not found. Please install Node.js first.")
        sys.exit(1)

def main():
    """Main function."""
    import argparse

    parser = argparse.ArgumentParser(description='Generate static images from Jekyll Mermaid posts (non-destructive)')
    parser.add_argument('filter', nargs='?', help='Filter posts by filename or content')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--force', '-f', action='store_true', help='Regenerate images even if they exist')

    args = parser.parse_args()

    check_dependencies()

    generator = MermaidImageOnlyGenerator(verbose=args.verbose)

    # Process files
    if args.filter:
        print(f"Generating images for posts matching: {args.filter}")
    else:
        print("Generating images for all mermaid posts...")

    generator.process_files(args.filter, args.force)

if __name__ == "__main__":
    main()
