
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

```javascript
javascript:(function(){console.log('🎬 Instagram Reels Extractor');const foundUrls=new Set();function extractReels(){const reels=[];document.querySelectorAll('a[href*="/reel/"]').forEach(link=>{const href=link.href;if(href&&href.includes('/reel/')&&!foundUrls.has(href)){foundUrls.add(href);reels.push(href);}});document.querySelectorAll('script').forEach(script=>{if(script.textContent){const patterns=[/https:\/\/www\.instagram\.com\/reel\/[A-Za-z0-9_-]+\/?/g,/\/reel\/[A-Za-z0-9_-]+\/?/g];patterns.forEach(pattern=>{const matches=script.textContent.match(pattern);if(matches){matches.forEach(match=>{let url=match;if(url.startsWith('/')){url='https://www.instagram.com'+url;}else if(!url.startsWith('http')){url='https://www.instagram.com/reel/'+url;}if(url.includes('/reel/')&&!foundUrls.has(url)){foundUrls.add(url);reels.push(url);}});}});}});return reels;}function cleanUrls(urls){return urls.map(url=>{let clean=url.split('?')[0];if(!clean.endsWith('/')){clean+='/';}return clean;}).sort();}async function scrollAndExtract(){let scrollCount=0;const maxScrolls=5;while(scrollCount<maxScrolls&&foundUrls.size<50){scrollCount++;window.scrollTo(0,document.body.scrollHeight);await new Promise(r=>setTimeout(r,2000));const newReels=extractReels();if(foundUrls.size===0)break;}return cleanUrls(Array.from(foundUrls));}scrollAndExtract().then(urls=>{console.log(`✅ Found ${urls.length} Reels:`);urls.forEach((url,i)=>console.log(`${i+1}. ${url}`));if(navigator.clipboard){navigator.clipboard.writeText(urls.join('\n')).then(()=>{alert(`📋 Copied ${urls.length} Reels URLs to clipboard!`);}).catch(()=>{console.log('❌ Could not copy to clipboard');});}else{console.log('❌ Clipboard not available');}});})();
```