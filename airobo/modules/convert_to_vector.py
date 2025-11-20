#!/usr/bin/env python3
"""
Convert PNG images to SVG vector format for better scalability.
This script will create SVG versions of your app icon and splash screen.

DEPRECATED: This script is maintained for backward compatibility.
Use: from airobo.modules.imageConverter import convert_images_in_directory
"""

from pathlib import Path
from airobo.modules.imageConverter import convert_images_in_directory


def main():
    config_dir = Path(r"C:\airoboConfigs")
    convert_images_in_directory(config_dir)


if __name__ == "__main__":
    main()
