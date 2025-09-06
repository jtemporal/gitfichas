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
import requests
import base64
from pathlib import Path
from typing import Dict, List, Any, Optional

class MermaidImageOnlyGenerator:
    def __init__(self, root_dir: str = ".", verbose: bool = False):
        self.root_dir = Path(root_dir)
        self.verbose = verbose
        self.posts_dirs = [
            self.root_dir / "_posts",
            self.root_dir / "en" / "_posts"
        ]
        self.images_dir = self.root_dir / "assets" / "img" / "mermaid"
        self.images_dir.mkdir(parents=True, exist_ok=True)
        
        # CSS file paths - create combined CSS with embedded fonts
        self.base_mermaid_css_path = self.root_dir / 'assets' / 'css' / 'embedded-svg.css'
        self.embedded_fonts_css_path = self.root_dir / 'assets' / 'css' / 'embedded-fonts.css'
        self.combined_css_path = self.root_dir / 'combined-mermaid.css'
        self.theme_path = self.root_dir / 'gitfichas-mermaid-theme.json'
        
        # Statistics
        self.stats = {
            'total_processed': 0,
            'total_success': 0,
            'total_skipped': 0,
            'total_errors': 0
        }
        
        # Initialize combined CSS file only (theme file is standalone)
        self._validate_theme_file()
        self._create_combined_css()
        
    def log(self, message: str, level: str = "INFO"):
        """Log message with optional verbose output."""
        if level == "ERROR" or self.verbose:
            prefix = f"[{level}]" if level != "INFO" else ""
            print(f"{prefix} {message}")
    
    def _validate_theme_file(self):
        """Validate that the standalone theme file exists."""
        if not self.theme_path.exists():
            raise FileNotFoundError(f"Theme file not found: {self.theme_path}. Please ensure gitfichas-mermaid-theme.json exists in the project root.")
        
        # Validate it's valid JSON
        try:
            import json
            with open(self.theme_path, 'r', encoding='utf-8') as f:
                json.load(f)
            self.log(f"✓ Using theme file: {self.theme_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in theme file {self.theme_path}: {e}")

    def _create_combined_css(self):
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
                
            self.log(f"✓ Created combined CSS file: {self.combined_css_path}")
            
        except Exception as e:
            self.log(f"Error creating combined CSS: {e}", "ERROR")

    def _cleanup_temp_files(self):
        """Clean up temporary files at the end."""
        self.combined_css_path.unlink(missing_ok=True)
    
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
            self.log(f"Error parsing YAML: {e}", "ERROR")
            return {}, content
    
    def generate_mermaid_syntax(self, front_matter: Dict[str, Any]) -> Optional[str]:
        """Generate Mermaid syntax from front matter data."""
        if not front_matter.get('mermaid', False):
            return None
            
        # Handle command-based diagrams
        if 'command' in front_matter:
            return self._generate_command_diagram(front_matter)
        
        # Handle concept-based diagrams  
        elif 'concept' in front_matter:
            return self._generate_concept_diagram(front_matter)
            
        return None
    
    def _escape_quotes(self, text: str) -> str:
        """Escape quotes in text for Mermaid syntax."""
        if not text:
            return ""
        return text.replace('"', '\"').replace("'", "\'")
    
    def _generate_command_diagram(self, fm: Dict[str, Any]) -> str:
        """Generate Mermaid syntax for command-based diagrams."""
        command = fm.get('command', '')
        command_parts = command.split()
        descriptors = fm.get('descriptors', [])
        info = fm.get('info', '')
        
        mermaid = "block-beta\ncolumns 1\n\n"
        
        # Generate based on command parts count
        if len(command_parts) == 3:
            part1 = self._escape_quotes(descriptors[1].get('part1', '')) if len(descriptors) > 1 else ''
            command_desc = self._escape_quotes(descriptors[0].get('command', '')) if len(descriptors) > 0 else ''
            
            mermaid += f"""block:notes
  space:2 f["{part1}"]
end

block:command
  a("{self._escape_quotes(command_parts[0])}") b("{self._escape_quotes(command_parts[1])}") c("{self._escape_quotes(command_parts[2])}")
end

block:notes2
  space g["{command_desc}"] space
end
"""
        
        elif len(command_parts) == 4:
            part1 = self._escape_quotes(descriptors[1].get('part1', '')) if len(descriptors) > 1 else ''
            command_desc = self._escape_quotes(descriptors[0].get('command', '')) if len(descriptors) > 0 else ''
            part2 = self._escape_quotes(descriptors[2].get('part2', '')) if len(descriptors) > 2 else ''
            
            mermaid += f"""block:notes
  space:2 f["{part1}"] space
end

block:command
  a("{self._escape_quotes(command_parts[0])}") b("{self._escape_quotes(command_parts[1])}") c("{self._escape_quotes(command_parts[2])}") d("{self._escape_quotes(command_parts[3])}")
end

block:notes2
  space g["{command_desc}"] space h["{part2}"]
end
"""
        
        elif len(command_parts) == 5:
            part1 = self._escape_quotes(descriptors[1].get('part1', '')) if len(descriptors) > 1 else ''
            part3 = self._escape_quotes(descriptors[3].get('part3', '')) if len(descriptors) > 3 else ''
            command_desc = self._escape_quotes(descriptors[0].get('command', '')) if len(descriptors) > 0 else ''
            part2 = self._escape_quotes(descriptors[2].get('part2', '')) if len(descriptors) > 2 else ''
            
            mermaid += f"""block:notes
  space:2 f["{part1}"] space i["{part3}"]
end

block:command
  a("{self._escape_quotes(command_parts[0])}") b("{self._escape_quotes(command_parts[1])}") c("{self._escape_quotes(command_parts[2])}") d("{self._escape_quotes(command_parts[3])}") e("{self._escape_quotes(command_parts[4])}")
end

block:notes2
  space g["{command_desc}"] space h["{part2}"] space
end
"""
        
        elif len(command_parts) == 6:
            part1 = self._escape_quotes(descriptors[1].get('part1', '')) if len(descriptors) > 1 else ''
            part3 = self._escape_quotes(descriptors[3].get('part3', '')) if len(descriptors) > 3 else ''
            command_desc = self._escape_quotes(descriptors[0].get('command', '')) if len(descriptors) > 0 else ''
            part2 = self._escape_quotes(descriptors[2].get('part2', '')) if len(descriptors) > 2 else ''
            part4 = self._escape_quotes(descriptors[4].get('part4', '')) if len(descriptors) > 4 else ''
            
            mermaid += f"""block:notes
  space:2 f["{part1}"] space i["{part3}"] space
end

block:command
  a("{self._escape_quotes(command_parts[0])}") b("{self._escape_quotes(command_parts[1])}") c("{self._escape_quotes(command_parts[2])}") d("{self._escape_quotes(command_parts[3])}") e("{self._escape_quotes(command_parts[4])}") k("{self._escape_quotes(command_parts[5])}")
end

block:notes2
  space g["{command_desc}"] space h["{part2}"] space l["{part4}"]
end
"""
        
        # Add info block if present
        if info:
            mermaid += f"""
block:info
  j["{self._escape_quotes(info)}"]
end
"""
        
        # Add arrows
        mermaid += """
%% arrows %%
b --> g
c --> f
classDef textFont font-family:'Chilanka', font-size:1.2em, color:#000, line-height:2em;
"""
        
        if len(command_parts) == 4:
            mermaid += "d --> h\n"
        elif len(command_parts) == 5:
            mermaid += "d --> h\ne --> i\n"
        elif len(command_parts) == 6:
            mermaid += "d --> h\ne --> i\nk --> l\nclassDef textFont font-family:'Chilanka', font-size:1.2em, color:#000, line-height:2.2em;\n"
        
        # Add styling
        mermaid += """
%% styling %%
classDef transparent fill:#fff, stroke:#fff;
class a,b,c,d,e,f,g,h,i,j,k,l,notes,notes2,command,info transparent
classDef commandFont font-family:'Borel', font-size:1.6em, line-height:2.2em;
class a,b,c,d,e,k commandFont
class f,g,h,i,j,l textFont
"""
        
        return mermaid
    
    def _generate_concept_diagram(self, fm: Dict[str, Any]) -> str:
        """Generate Mermaid syntax for concept-based diagrams."""
        parts = fm.get('parts', [])
        info = fm.get('info', '')
        
        mermaid = "block-beta\ncolumns 1\n\n"
        
        if len(parts) >= 1:
            part1 = self._escape_quotes(parts[0].get('part1', ''))
            mermaid += f"""block:notes
  a["{part1}"]
end
"""
        
        if len(parts) >= 2:
            part2 = self._escape_quotes(parts[1].get('part2', ''))
            mermaid += f"""block:notes2
  b["{part2}"]
end
"""
        
        if len(parts) >= 3:
            part3 = self._escape_quotes(parts[2].get('part3', ''))
            mermaid += f"""
block:notes3
  c["{part3}"]
end
"""
        
        if info:
            mermaid += f"""block:info
  f["{self._escape_quotes(info)}"]
end
"""
        
        # Add styling
        mermaid += """
%% styling %%
classDef transparent fill:#fff, stroke:#fff;
class a,b,c,notes,notes2,notes3,info transparent
classDef textFont font-family:'Chilanka', font-size:1.2em, color:#000, line-height:1.4em;
class a,b,c,notes,notes2,notes3,info textFont
"""
        
        return mermaid
    
    def generate_image(self, mermaid_syntax: str, output_path: Path) -> bool:
        """Generate image from Mermaid syntax using Mermaid CLI with mermaid.css file directly."""
        try:
            # Create temporary file for mermaid syntax
            temp_file = output_path.with_suffix('.mmd')
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(mermaid_syntax)
            
            # Run mermaid CLI to generate image using mermaid.css directly
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
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            # Clean up only the temporary mermaid file
            temp_file.unlink(missing_ok=True)
            
            if result.returncode == 0:
                self.log(f"✓ Generated image: {output_path}")
                return True
            else:
                self.log(f"✗ Error generating image: {result.stderr}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"✗ Exception generating image: {e}", "ERROR")
            return False
    
    def process_file(self, file_path: Path, force: bool = False) -> bool:
        """Process a single markdown file - ONLY generate image, don't modify file."""
        self.log(f"\nProcessing: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            front_matter, body = self.extract_front_matter(content)
            
            if not front_matter.get('mermaid', False):
                self.log(f"  Skipping: Not a mermaid post")
                self.stats['total_skipped'] += 1
                return False
            
            # Generate mermaid syntax
            mermaid_syntax = self.generate_mermaid_syntax(front_matter)
            if not mermaid_syntax:
                self.log(f"  Skipping: Could not generate mermaid syntax")
                self.stats['total_skipped'] += 1
                return False
            
            # Determine output image path
            number = front_matter.get('number', file_path.stem.split('-')[-1])
            lang = front_matter.get('lang', 'pt')
            
            if lang == 'en':
                image_filename = f"{number}-en.svg"
            else:
                image_filename = f"{number}.svg"
            
            image_path = self.images_dir / image_filename
            
            # Check if image already exists
            if image_path.exists() and not force:
                self.log(f"  Image already exists: {image_path}")
                self.stats['total_skipped'] += 1
                return False
            
            # Generate image (no file modification!)
            if self.generate_image(mermaid_syntax, image_path):
                self.stats['total_success'] += 1
                return True
            else:
                self.stats['total_errors'] += 1
                return False
                
        except Exception as e:
            self.log(f"✗ Error processing {file_path}: {e}", "ERROR")
            self.stats['total_errors'] += 1
            return False
    
    def process_files(self, filename_filter: Optional[str] = None, force: bool = False) -> None:
        """Process all markdown files or those matching the filter."""
        
        for posts_dir in self.posts_dirs:
            if not posts_dir.exists():
                continue
                
            self.log(f"\nProcessing directory: {posts_dir}")
            
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
                    
                self.stats['total_processed'] += 1
                self.process_file(file_path, force)
        
        self.print_summary()
    
    def print_summary(self):
        """Print processing summary."""
        print(f"\n=== Summary ===")
        print(f"Total files processed: {self.stats['total_processed']}")
        print(f"Images generated: {self.stats['total_success']}")
        print(f"Skipped: {self.stats['total_skipped']}")
        print(f"Failed: {self.stats['total_errors']}")
        
        if self.stats['total_success'] > 0:
            print(f"\n✅ Generated images in: {self.images_dir}")
            print(f"\n💡 To use static images, add 'use_static_image: true' to post front matter")
        
        # Clean up temporary files
        self._cleanup_temp_files()

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
