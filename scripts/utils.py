#!/usr/bin/env python3
"""
Statistics and Logging for GitFichas Mermaid Generator
=====================================================

Handles statistics tracking and logging functionality.
"""

from pathlib import Path
from typing import Dict


class StatsTracker:
    """Tracks processing statistics."""

    def __init__(self):
        self.stats = {
            'total_processed': 0,
            'total_success': 0,
            'total_skipped': 0,
            'total_errors': 0
        }

    def increment_processed(self):
        """Increment processed count."""
        self.stats['total_processed'] += 1

    def increment_success(self):
        """Increment success count."""
        self.stats['total_success'] += 1

    def increment_skipped(self):
        """Increment skipped count."""
        self.stats['total_skipped'] += 1

    def increment_errors(self):
        """Increment error count."""
        self.stats['total_errors'] += 1

    def get_stats(self) -> Dict[str, int]:
        """Get current statistics."""
        return self.stats.copy()

    def print_summary(self, images_dir: Path):
        """Print processing summary."""
        print(f"\n=== Summary ===")
        print(f"Total files processed: {self.stats['total_processed']}")
        print(f"Images generated: {self.stats['total_success']}")
        print(f"Skipped: {self.stats['total_skipped']}")
        print(f"Failed: {self.stats['total_errors']}")

        if self.stats['total_success'] > 0:
            print(f"\n✅ Generated images in: {images_dir}")
            print(f"\n💡 To use static images, add 'use_static_image: true' to post front matter")


class Logger:
    """Handles logging with optional verbose output."""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose

    def log(self, message: str, level: str = "INFO"):
        """Log message with optional verbose output."""
        if level == "ERROR" or self.verbose:
            prefix = f"[{level}]" if level != "INFO" else ""
            print(f"{prefix} {message}")

    def info(self, message: str):
        """Log info message."""
        self.log(message, "INFO")

    def error(self, message: str):
        """Log error message."""
        self.log(message, "ERROR")

    def success(self, message: str):
        """Log success message (always shown)."""
        print(f"✓ {message}")

    def warning(self, message: str):
        """Log warning message (always shown)."""
        print(f"⚠ {message}")

    def failure(self, message: str):
        """Log failure message (always shown)."""
        print(f"✗ {message}")
