#!/usr/bin/env python3
"""
Firefox Extension Creator for Instagram Reels Extractor

This script creates a simple Firefox extension that adds the Instagram Reels
Extractor as a browser action button.
"""

import json
import os
import zipfile
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

def create_manifest_json():
    """Create manifest.json for Firefox extension."""
    manifest = {
        "manifest_version": 2,
        "name": "Instagram Reels Extractor",
        "version": "1.0.0",
        "description": "Extract Instagram Reels URLs from profile pages with one click",
        "permissions": [
            "activeTab",
            "clipboardWrite"
        ],
        "browser_action": {
            "default_title": "Extract Instagram Reels",
            "default_icon": {
                "16": "icon16.png",
                "32": "icon32.png",
                "48": "icon48.png",
                "128": "icon128.png"
            }
        },
        "content_scripts": [
            {
                "matches": ["*://www.instagram.com/*/reels/*"],
                "js": ["content.js"],
                "run_at": "document_end"
            }
        ],
        "icons": {
            "16": "icon16.png",
            "32": "icon32.png",
            "48": "icon48.png",
            "128": "icon128.png"
        }
    }
    return json.dumps(manifest, indent=2)

def create_content_script(bookmarklet_code):
    """Create content script for the extension."""
    # Extract the JavaScript code from the bookmarklet
    js_code = bookmarklet_code.replace('javascript:', '')
    
    content_script = f"""
// Instagram Reels Extractor - Content Script
// This script runs on Instagram Reels pages

console.log('🎬 Instagram Reels Extractor extension loaded');

// Listen for messages from the browser action
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {{
    if (request.action === 'extractReels') {{
        extractReels();
        sendResponse({{success: true}});
    }}
}});

// Extract Reels URLs function
{js_code}

// Make extractReels available globally
window.extractReels = extractReels;

// Auto-extract on page load (optional)
if (window.location.href.includes('/reels/')) {{
    console.log('🎬 Auto-extracting Reels on page load...');
    setTimeout(extractReels, 2000); // Wait 2 seconds for page to load
}}
"""
    return content_script

def create_background_script():
    """Create background script for the extension."""
    background_script = """
// Instagram Reels Extractor - Background Script

chrome.browserAction.onClicked.addListener((tab) => {
    // Check if we're on an Instagram Reels page
    if (tab.url.includes('instagram.com') && tab.url.includes('/reels/')) {
        // Execute the extraction script
        chrome.tabs.executeScript(tab.id, {
            code: 'if (window.extractReels) { window.extractReels(); } else { console.log("Extension not ready, please refresh the page"); }'
        });
    } else {
        // Open Instagram Reels page
        chrome.tabs.create({
            url: 'https://www.instagram.com/bruno.casasdotejo/reels/',
            active: true
        });
    }
});
"""
    return background_script

def create_icon_svg():
    """Create SVG icon for the extension."""
    svg_content = """<svg width="128" height="128" viewBox="0 0 128 128" xmlns="http://www.w3.org/2000/svg">
  <rect width="128" height="128" rx="20" fill="#E4405F"/>
  <rect x="20" y="20" width="88" height="88" rx="8" fill="white" opacity="0.1"/>
  <rect x="30" y="30" width="68" height="68" rx="4" fill="white"/>
  <rect x="40" y="40" width="48" height="48" rx="2" fill="#E4405F"/>
  <rect x="50" y="50" width="28" height="28" rx="1" fill="white"/>
  <rect x="60" y="60" width="8" height="8" fill="#E4405F"/>
  <text x="64" y="100" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" font-weight="bold" fill="white">REELS</text>
</svg>"""
    return svg_content

def create_readme():
    """Create README for the extension."""
    readme_content = """# Instagram Reels Extractor - Firefox Extension

This is a Firefox extension that adds a button to extract Instagram Reels URLs.

## Installation

### Method 1: Load as Temporary Extension (Recommended for testing)

1. Open Firefox
2. Go to `about:debugging`
3. Click "This Firefox"
4. Click "Load Temporary Add-on"
5. Select the `manifest.json` file from this folder
6. The extension will be loaded and active

### Method 2: Package and Install

1. Zip all files in this folder
2. Rename the zip file to `instagram-reels-extractor.xpi`
3. In Firefox, go to `about:addons`
4. Click the gear icon → "Install Add-on From File"
5. Select the `.xpi` file

## Usage

1. Go to any Instagram Reels page (e.g., `https://www.instagram.com/username/reels/`)
2. Click the extension button in the toolbar
3. Reels URLs will be extracted and copied to clipboard
4. A popup will show the results

## Features

- ✅ One-click Reels URL extraction
- ✅ Automatic scrolling to load more Reels
- ✅ Clipboard integration
- ✅ Visual feedback with popup
- ✅ Works on any Instagram Reels page

## Troubleshooting

- If the extension doesn't work, refresh the Instagram page
- Make sure you're on the Reels tab (not Posts or IGTV)
- Check the browser console for any error messages

## Development

To modify the extension:
1. Edit the files in this folder
2. Reload the extension in `about:debugging`
3. Test on Instagram Reels pages
"""
    return readme_content

def create_extension_files():
    """Create all files needed for the Firefox extension."""
    print("🎬 Creating Firefox Extension for Instagram Reels Extractor")
    print("=" * 60)
    
    # Read bookmarklet code
    bookmarklet_code = read_bookmarklet_code()
    if not bookmarklet_code:
        print("❌ Failed to read bookmarklet code. Exiting.")
        return None
    
    print(f"✅ Found bookmarklet code ({len(bookmarklet_code)} characters)")
    
    # Create extension directory
    extension_dir = Path(__file__).parent / "firefox_extension"
    extension_dir.mkdir(exist_ok=True)
    
    # Create manifest.json
    manifest_content = create_manifest_json()
    manifest_file = extension_dir / "manifest.json"
    with open(manifest_file, 'w', encoding='utf-8') as f:
        f.write(manifest_content)
    print(f"✅ Created manifest.json")
    
    # Create content script
    content_script = create_content_script(bookmarklet_code)
    content_file = extension_dir / "content.js"
    with open(content_file, 'w', encoding='utf-8') as f:
        f.write(content_script)
    print(f"✅ Created content.js")
    
    # Create background script
    background_script = create_background_script()
    background_file = extension_dir / "background.js"
    with open(background_file, 'w', encoding='utf-8') as f:
        f.write(background_script)
    print(f"✅ Created background.js")
    
    # Create icon files (SVG for now, would need PNG conversion for production)
    icon_svg = create_icon_svg()
    icon_file = extension_dir / "icon.svg"
    with open(icon_file, 'w', encoding='utf-8') as f:
        f.write(icon_svg)
    print(f"✅ Created icon.svg")
    
    # Create README
    readme_content = create_readme()
    readme_file = extension_dir / "README.md"
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print(f"✅ Created README.md")
    
    # Create a simple installation script
    install_script = """#!/bin/bash
# Firefox Extension Installation Script

echo "🎬 Installing Instagram Reels Extractor Extension"
echo "================================================"

# Check if Firefox is running
if pgrep -x "firefox" > /dev/null; then
    echo "⚠️  Firefox is running. Please close it before installing the extension."
    echo "   Or use the temporary add-on method in about:debugging"
    exit 1
fi

# Create the extension directory in Firefox profile
FIREFOX_PROFILE=$(find ~/.mozilla/firefox -name "*.default*" -type d | head -1)
if [ -z "$FIREFOX_PROFILE" ]; then
    echo "❌ Could not find Firefox profile directory"
    exit 1
fi

EXTENSION_DIR="$FIREFOX_PROFILE/extensions/instagram-reels-extractor@example.com"
mkdir -p "$EXTENSION_DIR"

# Copy extension files
cp manifest.json "$EXTENSION_DIR/"
cp content.js "$EXTENSION_DIR/"
cp background.js "$EXTENSION_DIR/"
cp icon.svg "$EXTENSION_DIR/"

echo "✅ Extension installed to: $EXTENSION_DIR"
echo "🎯 Restart Firefox to activate the extension"
echo "📋 The extension will appear in your toolbar"
"""
    
    install_file = extension_dir / "install.sh"
    with open(install_file, 'w', encoding='utf-8') as f:
        f.write(install_script)
    os.chmod(install_file, 0o755)  # Make executable
    print(f"✅ Created install.sh")
    
    return extension_dir

def main():
    """Main function to create Firefox extension."""
    extension_dir = create_extension_files()
    
    if extension_dir:
        print("\n" + "=" * 60)
        print("📋 Extension Created Successfully!")
        print(f"📁 Extension directory: {extension_dir}")
        print("\n🎯 Next Steps:")
        print("1. Open Firefox and go to about:debugging")
        print("2. Click 'This Firefox' → 'Load Temporary Add-on'")
        print("3. Select the manifest.json file from the extension directory")
        print("4. Go to any Instagram Reels page and click the extension button!")
        print("\n📖 For detailed instructions, see the README.md in the extension directory")

if __name__ == "__main__":
    main()
