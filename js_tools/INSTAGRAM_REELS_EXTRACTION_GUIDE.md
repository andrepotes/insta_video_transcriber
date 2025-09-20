# Instagram Reels URL Extraction Guide

This guide provides multiple methods to extract Reels URLs from Instagram profile pages for use with the Instagram Video Transcriber.

## Method 1: JavaScript Console (Recommended)

### Step 1: Open Instagram Profile
1. Go to the Instagram profile's Reels page: 
2. Scroll down to load more Reels (optional, but recommended for more URLs)

### Step 2: Open Developer Console
1. Press `F12` or right-click → "Inspect"
2. Click on the "Console" tab

### Step 3: Run the Extraction Script
1. Copy the entire contents of `instagram_reels_extractor.js`
2. Paste it into the console
3. Press `Enter` to run

### Step 4: Get Results
- URLs will be displayed in the console
- URLs will be automatically copied to clipboard
- A popup will show the first 10 URLs found

## Method 2: Browser Bookmarklet

### Step 1: Create the Bookmarklet
1. Copy this code:
```javascript
javascript:(function(){console.log('🎬 Instagram Reels Extractor');const foundUrls=new Set();function extractReels(){const reels=[];document.querySelectorAll('a[href*="/reel/"]').forEach(link=>{const href=link.href;if(href&&href.includes('/reel/')&&!foundUrls.has(href)){foundUrls.add(href);reels.push(href);}});document.querySelectorAll('script').forEach(script=>{if(script.textContent){const patterns=[/https:\/\/www\.instagram\.com\/reel\/[A-Za-z0-9_-]+\/?/g,/\/reel\/[A-Za-z0-9_-]+\/?/g];patterns.forEach(pattern=>{const matches=script.textContent.match(pattern);if(matches){matches.forEach(match=>{let url=match;if(url.startsWith('/')){url='https://www.instagram.com'+url;}else if(!url.startsWith('http')){url='https://www.instagram.com/reel/'+url;}if(url.includes('/reel/')&&!foundUrls.has(url)){foundUrls.add(url);reels.push(url);}});}});}});return reels;}function cleanUrls(urls){return urls.map(url=>{let clean=url.split('?')[0];if(!clean.endsWith('/')){clean+='/';}return clean;}).sort();}async function scrollAndExtract(){let scrollCount=0;const maxScrolls=5;while(scrollCount<maxScrolls&&foundUrls.size<50){scrollCount++;window.scrollTo(0,document.body.scrollHeight);await new Promise(r=>setTimeout(r,2000));const newReels=extractReels();if(foundUrls.size===0)break;}return cleanUrls(Array.from(foundUrls));}scrollAndExtract().then(urls=>{console.log(`✅ Found ${urls.length} Reels:`);urls.forEach((url,i)=>console.log(`${i+1}. ${url}`));if(navigator.clipboard){navigator.clipboard.writeText(urls.join('\n')).then(()=>{alert(`📋 Copied ${urls.length} Reels URLs to clipboard!`);}).catch(()=>{console.log('❌ Could not copy to clipboard');});}else{console.log('❌ Clipboard not available');}});})();
```

2. Create a new bookmark in your browser
3. Name it: "Extract Instagram Reels"
4. Set the URL to the code above (starting with `javascript:`)

### Step 2: Use the Bookmarklet
1. Go to the Instagram profile's Reels page
2. Click the bookmarklet you created
3. URLs will be copied to clipboard and displayed

## Method 3: Manual Copy-Paste

### Step 1: Get URLs Manually
1. Go to each Reel individually
2. Right-click on the Reel → "Copy link address"
3. Paste into a text file

### Step 2: Format for Transcriber
Use the `create_structured_urls.py` script:
```bash
python3 create_structured_urls.py username --interactive
```

## Using Extracted URLs

### Option 1: Create Structured URLs File
```bash
python3 create_structured_urls.py username --interactive
```

### Option 2: Create File Manually
Create a text file with this format:
```
1. https://www.instagram.com/reel/ABC123/
2. https://www.instagram.com/reel/DEF456/
3. https://www.instagram.com/reel/GHI789/
```

### Option 3: Run Transcription
```bash
# Transcribe all videos
python3 main.py -f urls.txt -u username

# Transcribe specific videos
python3 main.py -f urls.txt -u username -s "1,3,5"

# Transcribe range of videos
python3 main.py -f urls.txt -u username -s "1-10"
```

## Troubleshooting

### "No Reels found"
- Make sure you're on the Reels tab (not Posts or IGTV)
- Scroll down to load more Reels before running the script
- Try refreshing the page

### "Script doesn't work"
- Make sure JavaScript is enabled
- Try a different browser (Chrome/Firefox work best)
- Check if you're logged into Instagram

### "URLs not copying"
- Manually copy from the console output
- Check if clipboard permissions are enabled
- Try the manual copy-paste method

## Features of the Extraction Script

### Automatic Features
- ✅ **Auto-scroll**: Automatically scrolls to load more Reels
- ✅ **URL cleaning**: Removes extra parameters and standardizes format
- ✅ **Duplicate removal**: Automatically removes duplicate URLs
- ✅ **Clipboard copying**: Automatically copies URLs to clipboard
- ✅ **Progress tracking**: Shows progress during extraction
- ✅ **Visual popup**: Shows results in a popup window

### Configuration Options
- **Max Reels**: Limit the number of Reels to extract (default: 50)
- **Auto-scroll**: Enable/disable automatic scrolling (default: enabled)
- **Scroll delay**: Time between scrolls (default: 2 seconds)
- **Max scrolls**: Maximum number of scroll attempts (default: 10)

## Example Workflow

1. **Go to Instagram**: `https://www.instagram.com/username/reels/`
2. **Open Console**: Press F12 → Console tab
3. **Run Script**: Copy and paste `instagram_reels_extractor.js`
4. **Wait for Results**: Script will scroll and extract URLs
5. **Get URLs**: URLs copied to clipboard automatically
6. **Create File**: Use `create_structured_urls.py` to format
7. **Transcribe**: Run `python3 main.py -f urls.txt -u username`

This method is much faster than manually copying each URL and works reliably with Instagram's current restrictions!
