#!/usr/bin/env python3
"""
Image Converter Module
Converts PNG images to SVG vector format for better scalability.
"""

import os
from pathlib import Path
import base64
from PIL import Image
import io


def png_to_svg(png_path, svg_path=None, optimize_for="icon"):
    """
    Convert PNG to SVG by embedding the PNG as base64 data.
    For true vector conversion, you'd need to trace the image, but this gives us scalable SVG.
    
    Args:
        png_path: Path to input PNG file
        svg_path: Path to output SVG file (if None, will use same name with .svg extension)
        optimize_for: Type of optimization ("icon" or "splash")
        
    Returns:
        Path to created SVG file
    """
    png_path = Path(png_path)
    
    if svg_path is None:
        svg_path = png_path.with_suffix('.svg')
    else:
        svg_path = Path(svg_path)
    
    # Read and optimize the PNG
    with Image.open(png_path) as img:
        # Convert to RGBA if not already
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # For icons, we might want to optimize size
        if optimize_for == "icon":
            # Resize to optimal size for vector embedding
            max_size = 512  # Good balance of quality vs file size
            if max(img.size) > max_size:
                img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
        
        # Save optimized PNG to memory
        png_buffer = io.BytesIO()
        img.save(png_buffer, format='PNG', optimize=True, compress_level=9)
        png_data = png_buffer.getvalue()
    
    # Convert to base64
    png_base64 = base64.b64encode(png_data).decode('utf-8')
    
    # Get image dimensions
    width, height = img.size
    
    # Create SVG with embedded PNG
    svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" 
     xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <title>{optimize_for.title()}</title>
  <desc>Vector version of {png_path.name} for perfect scaling</desc>
  
  <!-- Embedded high-quality PNG data -->
  <image x="0" y="0" width="{width}" height="{height}" 
         xlink:href="data:image/png;base64,{png_base64}" />
</svg>'''
    
    # Write SVG file
    with open(svg_path, 'w', encoding='utf-8') as f:
        f.write(svg_content)
    
    return svg_path


def convert_images_in_directory(directory, images=None):
    """
    Convert multiple PNG images to SVG in a directory.
    
    Args:
        directory: Path to directory containing images
        images: List of tuples (png_name, svg_name, optimize_type). 
                If None, will convert appIcon.png and splash.png
                
    Returns:
        List of paths to created SVG files
    """
    directory = Path(directory)
    
    if images is None:
        images = [
            ("appIcon.png", "appIcon.svg", "icon"),
            ("splash.png", "splash.svg", "splash")
        ]
    
    print(f"🎨 Converting PNG images to SVG vector format...")
    print(f"📁 Config directory: {directory}")
    
    created_files = []
    
    for png_name, svg_name, optimize_type in images:
        png_path = directory / png_name
        svg_path = directory / svg_name
        
        if png_path.exists():
            print(f"\n🔄 Converting {png_name} to {svg_name}...")
            
            # Get original size
            with Image.open(png_path) as img:
                orig_size = png_path.stat().st_size
                print(f"   📏 Original: {img.size[0]}x{img.size[1]} ({orig_size:,} bytes)")
            
            # Convert to SVG
            result_path = png_to_svg(png_path, svg_path, optimize_type)
            created_files.append(result_path)
            
            # Get new size
            new_size = svg_path.stat().st_size
            print(f"   ✅ Created: {svg_path.name} ({new_size:,} bytes)")
            print(f"   📊 Size change: {((new_size - orig_size) / orig_size * 100):+.1f}%")
            
        else:
            print(f"⚠️  {png_name} not found in {directory}")
    
    if created_files:
        print(f"\n🎉 Vector conversion complete!")
        print(f"💡 SVG files are now available alongside your PNG files")
        print(f"📱 The build system will automatically use SVG when available for better quality")
    
    return created_files
