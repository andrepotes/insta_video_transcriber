# JavaScript Tools for Instagram Reels URL Extraction

This folder contains JavaScript tools for extracting Reels URLs from Instagram profile pages.

## Files

### `instagram_reels_extractor.js`
**Full-featured extraction script** with advanced features:
- ✅ **Automatic scrolling** to load more Reels
- ✅ **URL cleaning** and deduplication
- ✅ **Clipboard integration** for easy copying
- ✅ **Progress tracking** with visual feedback
- ✅ **Visual popup** showing results
- ✅ **Configurable parameters** (max Reels, scroll delay, etc.)
- ✅ **Multiple extraction methods** for reliability

**Usage:**
1. Go to Instagram Reels page: `https://www.instagram.com/username/reels/`
2. Open Developer Tools (F12) → Console tab
3. Copy and paste the entire contents of this file
4. Press Enter to run
5. URLs will be automatically extracted and copied to clipboard

### `instagram_reels_bookmarklet.js`
**Minified bookmarklet version** for one-click extraction:
- ✅ **One-click extraction** from any Instagram Reels page
- ✅ **Automatic scrolling** and URL collection
- ✅ **Clipboard copying** with success notification
- ✅ **Lightweight** and fast

**Usage:**
1. Create a bookmark with the minified code from this file
2. Go to Instagram Reels page
3. Click the bookmark
4. URLs will be extracted and copied to clipboard

### `INSTAGRAM_REELS_EXTRACTION_GUIDE.md`
**Comprehensive usage guide** with:
- ✅ **Step-by-step instructions** for all methods
- ✅ **Troubleshooting guide** for common issues
- ✅ **Configuration options** and customization
- ✅ **Example workflows** and best practices

## Quick Start

### Method 1: Console Script (Recommended)
```bash
# 1. Go to Instagram Reels page
# 2. Open Console (F12) → Console tab
# 3. Copy and paste instagram_reels_extractor.js
# 4. Press Enter - URLs automatically extracted and copied!
```

### Method 2: Browser Bookmarklet
```bash
# 1. Create bookmark with code from instagram_reels_bookmarklet.js
# 2. Go to Instagram Reels page
# 3. Click bookmark - URLs extracted and copied!
```

### Method 3: Simple Console Method
```javascript
// Basic extraction (paste in console)
const reels = [];
document.querySelectorAll('a[href*="/reel/"]').forEach(link => {
    const href = link.href;
    if (href.includes('/reel/') && !reels.includes(href)) {
        reels.push(href);
    }
});
navigator.clipboard.writeText(reels.join('\n'));
```

## Integration with Main Project

After extracting URLs with these JavaScript tools:

1. **Format URLs**: Use `create_structured_urls.py` to create structured file
2. **Transcribe**: Run `python3 main.py -f urls.txt -u username`

## Features Comparison

| Feature | Console Script | Bookmarklet | Simple Method |
|---------|---------------|-------------|---------------|
| Auto-scroll | ✅ | ✅ | ❌ |
| URL cleaning | ✅ | ✅ | ❌ |
| Progress tracking | ✅ | ❌ | ❌ |
| Visual popup | ✅ | ❌ | ❌ |
| Configurable | ✅ | ❌ | ❌ |
| Clipboard copy | ✅ | ✅ | ✅ |
| Multiple methods | ✅ | ✅ | ❌ |

## Troubleshooting

- **"No Reels found"**: Make sure you're on the Reels tab, scroll down to load more
- **"Script doesn't work"**: Check if JavaScript is enabled, try different browser
- **"URLs not copying"**: Manually copy from console output

For detailed troubleshooting, see `INSTAGRAM_REELS_EXTRACTION_GUIDE.md`.
