#!/usr/bin/env python3
"""
Cross-platform publishing script for airobo
Double-click friendly with persistent terminal!
"""

import os
import re
import subprocess
import sys
import time
from pathlib import Path

def ensure_terminal_visible():
    """Ensure we have a visible terminal window"""
    if os.name == 'nt':  # Windows
        # Try to allocate a console if we don't have one
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            if kernel32.GetConsoleWindow() == 0:
                kernel32.AllocConsole()
        except:
            pass

def main():
    ensure_terminal_visible()
    
    print("=" * 50)
    print("      AIROBO PyPI Publishing Script")
    print("=" * 50)
    print()
    
    try:
        # Change to script directory
        script_dir = Path(__file__).parent
        os.chdir(script_dir)
        
        # Read current version
        toml_path = Path("pyproject.toml")
        if not toml_path.exists():
            print("❌ Error: pyproject.toml not found!")
            input("Press Enter to exit...")
            return
        
        with open(toml_path, 'r') as f:
            content = f.read()
        
        version_match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', content)
        if not version_match:
            print("❌ Error: Could not find version in pyproject.toml!")
            input("Press Enter to exit...")
            return
        
        current_version = version_match.group(1)
        
        # Increment patch version
        parts = current_version.split('.')
        if len(parts) != 3:
            print(f"❌ Error: Invalid version format: {current_version}")
            input("Press Enter to exit...")
            return
        
        major, minor, patch = parts
        new_patch = int(patch) + 1
        new_version = f"{major}.{minor}.{new_patch}"
        
        print(f"📝 Auto-incrementing version: {current_version} → {new_version}")
        
        # Update version in pyproject.toml
        new_content = re.sub(
            r'version\s*=\s*["\'][^"\']+["\']',
            f'version = "{new_version}"',
            content
        )
        
        with open(toml_path, 'w') as f:
            f.write(new_content)
        
        print("✅ Version updated in pyproject.toml")
        
        # Clean old builds
        print("🧹 Cleaning old builds...")
        for folder in ['dist', 'build', 'airobo.egg-info']:
            if Path(folder).exists():
                if os.name == 'nt':  # Windows
                    subprocess.run(['rmdir', '/s', '/q', folder], shell=True)
                else:  # Mac/Linux
                    subprocess.run(['rm', '-rf', folder])
        
        # Build package
        print("🔨 Building package...")
        result = subprocess.run([sys.executable, '-m', 'build'], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Build failed: {result.stderr}")
            input("Press Enter to exit...")
            return
        
        print("✅ Package built successfully!")
        
        # Read PyPI token
        env_path = Path(".env")
        if not env_path.exists():
            print("❌ Error: .env file not found!")
            input("Press Enter to exit...")
            return
        
        with open(env_path, 'r') as f:
            env_content = f.read()
        
        token_match = re.search(r'apiToken\s*=\s*(.+)', env_content)
        if not token_match:
            print("❌ Error: Could not find apiToken in .env!")
            input("Press Enter to exit...")
            return
        
        pypi_token = token_match.group(1).strip()
        
        # Upload to PyPI
        print("📤 Uploading to PyPI...")
        result = subprocess.run([
            'twine', 'upload', f'dist/*',
            '--username', '__token__',
            '--password', pypi_token
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"❌ Upload failed: {result.stderr}")
            input("Press Enter to exit...")
            return
        
        print(f"✅ Successfully published version {new_version}!")
        print(f"🌐 View at: https://pypi.org/project/airobo/{new_version}/")
        
        # Update local installation
        print("🔄 Updating local installation...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'airobo'])
        
        print()
        print("=" * 50)
        print(f"   🎉 SUCCESS! Version {new_version} published!")
        print("=" * 50)
        print()
        print("Users can now install with:")
        print("  pip install --upgrade airobo")
        print()
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print(f"Error details: {type(e).__name__}")
    
    print("\n" + "=" * 50)
    print("Script finished! Terminal will stay open...")
    print("=" * 50)
    
    # Multiple ways to keep terminal open
    try:
        input("\nPress Enter to close this window...")
    except (EOFError, KeyboardInterrupt):
        print("\nForcing terminal to stay open for 10 seconds...")
        time.sleep(10)

if __name__ == "__main__":
    main()