#!/usr/bin/env python3
"""
One-Click Firefox Setup for Instagram Reels Extractor

This script creates both bookmark files and a Firefox extension
for easy installation of the Instagram Reels Extractor.
"""

import subprocess
import sys
from pathlib import Path

def run_script(script_name):
    """Run a Python script and return success status."""
    try:
        script_path = Path(__file__).parent / script_name
        result = subprocess.run([sys.executable, str(script_path)], 
                              capture_output=True, text=True, check=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running {script_name}:")
        print(e.stdout)
        print(e.stderr)
        return False
    except FileNotFoundError:
        print(f"❌ Script not found: {script_name}")
        return False

def main():
    """Main function to set up all Firefox tools."""
    print("🎬 Firefox Setup for Instagram Reels Extractor")
    print("=" * 60)
    print("This will create both bookmark files and a Firefox extension.")
    print()
    
    # Create bookmark files
    print("📌 Creating Firefox bookmark files...")
    bookmark_success = run_script("create_firefox_bookmark.py")
    
    print("\n" + "=" * 40)
    
    # Create Firefox extension
    print("🔧 Creating Firefox extension...")
    extension_success = run_script("create_firefox_extension.py")
    
    print("\n" + "=" * 60)
    print("📋 Setup Complete!")
    
    if bookmark_success:
        print("✅ Bookmark files created in: js_tools/firefox_bookmarks/")
        print("   - instagram_reels_bookmark.html (import this)")
        print("   - FIREFOX_BOOKMARK_INSTRUCTIONS.md (follow these)")
    
    if extension_success:
        print("✅ Firefox extension created in: js_tools/firefox_extension/")
        print("   - Load manifest.json in about:debugging")
        print("   - Or follow README.md for installation")
    
    print("\n🎯 Choose your preferred method:")
    print("1. 📌 Bookmark: Import the HTML file or follow manual instructions")
    print("2. 🔧 Extension: Load the extension in Firefox for a toolbar button")
    print("\n💡 Both methods will extract Reels URLs and copy them to clipboard!")

if __name__ == "__main__":
    main()
