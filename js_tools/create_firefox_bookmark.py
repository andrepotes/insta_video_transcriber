#!/usr/bin/env python3
"""
Firefox Bookmark Creator for Instagram Reels Extractor

This script creates a Firefox bookmark file that can be imported to automatically
add the Instagram Reels Extractor bookmarklet to your browser.
"""

import json
import os
from datetime import datetime
from pathlib import Path

def read_bookmarklet_code():
    """Read the bookmarklet code from the JavaScript file."""
    script_dir = Path(__file__).parent
    bookmarklet_file = script_dir / "instagram_reels_bookmarklet.js"
    
    try:
        with open(bookmarklet_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Extract the minified bookmarklet code
        # Look for the javascript: line
        lines = content.split('\n')
        for line in lines:
            if line.strip().startswith('javascript:'):
                return line.strip()
        
        # If not found, look for the minified version in comments
        for line in lines:
            if 'javascript:(function(){' in line:
                return line.strip()
        
        raise ValueError("Bookmarklet code not found in file")
        
    except FileNotFoundError:
        print(f"Error: Could not find {bookmarklet_file}")
        return None
    except Exception as e:
        print(f"Error reading bookmarklet file: {e}")
        return None

def create_firefox_bookmark_html(bookmarklet_code):
    """Create an HTML file that can be imported into Firefox."""
    html_content = f"""<!DOCTYPE NETSCAPE-Bookmark-file-1>
<!-- This is an automatically generated file.
     It will be imported and its contents will be replaced.
     DO NOT EDIT! -->
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<TITLE>Bookmarks</TITLE>
<H1>Bookmarks</H1>
<DL><p>
    <DT><A HREF="{bookmarklet_code}" ADD_DATE="{int(datetime.now().timestamp())}" LAST_MODIFIED="{int(datetime.now().timestamp())}" ID="instagram-reels-extractor">🎬 Extract Instagram Reels</A>
</DL><p>
"""
    return html_content

def create_firefox_bookmark_json(bookmarklet_code):
    """Create a JSON file for Firefox bookmark import (alternative method)."""
    bookmark_data = {
        "title": "🎬 Extract Instagram Reels",
        "url": bookmarklet_code,
        "dateAdded": int(datetime.now().timestamp() * 1000000),  # Firefox uses microseconds
        "lastModified": int(datetime.now().timestamp() * 1000000),
        "id": "instagram-reels-extractor",
        "type": "bookmark"
    }
    
    return json.dumps(bookmark_data, indent=2)

def create_manual_instructions():
    """Create manual instructions for adding the bookmark."""
    return """
# Manual Bookmark Creation Instructions

## Method 1: Direct Bookmark Creation (Easiest)

1. **Open Firefox** and go to any Instagram Reels page
2. **Right-click** on the bookmark bar (or press Ctrl+Shift+B to show it)
3. **Select "Add Bookmark..."**
4. **Set the following:**
   - Name: `🎬 Extract Instagram Reels`
   - URL: Copy the bookmarklet code from below
   - Folder: Choose "Bookmarks Toolbar" or "Other Bookmarks"
5. **Click "Save"**

## Method 2: Import HTML File

1. **Run this script** to generate the bookmark file
2. **Open Firefox** → Bookmarks → Manage Bookmarks (Ctrl+Shift+O)
3. **Click "Import and Backup"** → "Import Bookmarks from HTML"
4. **Select** the generated `instagram_reels_bookmark.html` file
5. **Choose** where to import (Bookmarks Toolbar recommended)

## Method 3: Drag and Drop

1. **Create a new text file** with `.html` extension
2. **Copy the generated HTML content** into the file
3. **Drag the file** into Firefox bookmarks toolbar
4. **Rename** the bookmark to "🎬 Extract Instagram Reels"

## Bookmarklet Code:
"""

def main():
    """Main function to create Firefox bookmark files."""
    print("🎬 Firefox Bookmark Creator for Instagram Reels Extractor")
    print("=" * 60)
    
    # Read the bookmarklet code
    bookmarklet_code = read_bookmarklet_code()
    if not bookmarklet_code:
        print("❌ Failed to read bookmarklet code. Exiting.")
        return
    
    print(f"✅ Found bookmarklet code ({len(bookmarklet_code)} characters)")
    
    # Create output directory
    output_dir = Path(__file__).parent / "firefox_bookmarks"
    output_dir.mkdir(exist_ok=True)
    
    # Create HTML bookmark file
    html_content = create_firefox_bookmark_html(bookmarklet_code)
    html_file = output_dir / "instagram_reels_bookmark.html"
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Created HTML bookmark file: {html_file}")
    
    # Create JSON bookmark file (alternative)
    json_content = create_firefox_bookmark_json(bookmarklet_code)
    json_file = output_dir / "instagram_reels_bookmark.json"
    
    with open(json_file, 'w', encoding='utf-8') as f:
        f.write(json_content)
    
    print(f"✅ Created JSON bookmark file: {json_file}")
    
    # Create instructions file
    instructions = create_manual_instructions()
    instructions += f"\n```javascript\n{bookmarklet_code}\n```"
    
    instructions_file = output_dir / "FIREFOX_BOOKMARK_INSTRUCTIONS.md"
    with open(instructions_file, 'w', encoding='utf-8') as f:
        f.write(instructions)
    
    print(f"✅ Created instructions file: {instructions_file}")
    
    # Create a simple text file with just the bookmarklet code
    code_file = output_dir / "bookmarklet_code.txt"
    with open(code_file, 'w', encoding='utf-8') as f:
        f.write(bookmarklet_code)
    
    print(f"✅ Created bookmarklet code file: {code_file}")
    
    print("\n" + "=" * 60)
    print("📋 Next Steps:")
    print("1. Open the instructions file: firefox_bookmarks/FIREFOX_BOOKMARK_INSTRUCTIONS.md")
    print("2. Follow the manual instructions to add the bookmark")
    print("3. Or import the HTML file: firefox_bookmarks/instagram_reels_bookmark.html")
    print("4. Test the bookmark on any Instagram Reels page!")
    print("\n🎯 The bookmark will extract Reels URLs and copy them to clipboard!")

if __name__ == "__main__":
    main()
