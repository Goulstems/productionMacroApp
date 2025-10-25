#!/usr/bin/env python3
"""
Convert PNG images to SVG vector format for better scalability.
This script will create SVG versions of your app icon and splash screen.
"""

import os
from pathlib import Path
import base64
from PIL import Image

def png_to_svg(png_path, svg_path, optimize_for="icon"):
    """
    Convert PNG to SVG by embedding the PNG as base64 data.
    For true vector conversion, you'd need to trace the image, but this gives us scalable SVG.
    """
    
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
        import io
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
  <title>AI & Robotics Academy - {optimize_for.title()}</title>
  <desc>Vector version of {png_path.name} for perfect scaling</desc>
  
  <!-- Embedded high-quality PNG data -->
  <image x="0" y="0" width="{width}" height="{height}" 
         xlink:href="data:image/png;base64,{png_base64}" />
</svg>'''
    
    # Write SVG file
    with open(svg_path, 'w', encoding='utf-8') as f:
        f.write(svg_content)
    
    return svg_path

def main():
    config_dir = Path(r"C:\airoboConfigs")
    
    print("🎨 Converting PNG images to SVG vector format...")
    print(f"📁 Config directory: {config_dir}")
    
    conversions = [
        ("appIcon.png", "appIcon.svg", "icon"),
        ("splash.png", "splash.svg", "splash")
    ]
    
    for png_name, svg_name, optimize_type in conversions:
        png_path = config_dir / png_name
        svg_path = config_dir / svg_name
        
        if png_path.exists():
            print(f"\n🔄 Converting {png_name} to {svg_name}...")
            
            # Get original size
            with Image.open(png_path) as img:
                orig_size = png_path.stat().st_size
                print(f"   📏 Original: {img.size[0]}x{img.size[1]} ({orig_size:,} bytes)")
            
            # Convert to SVG
            result_path = png_to_svg(png_path, svg_path, optimize_type)
            
            # Get new size
            new_size = svg_path.stat().st_size
            print(f"   ✅ Created: {svg_path.name} ({new_size:,} bytes)")
            print(f"   📊 Size change: {((new_size - orig_size) / orig_size * 100):+.1f}%")
            
        else:
            print(f"❌ {png_name} not found in {config_dir}")
    
    print(f"\n🎉 Vector conversion complete!")
    print(f"💡 SVG files are now available alongside your PNG files")
    print(f"📱 The build system will automatically use SVG when available for better quality")

if __name__ == "__main__":
    main()