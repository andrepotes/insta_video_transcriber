/**
 * Instagram Reels URL Extractor - Bookmarklet Version
 * 
 * This is a minified version for use as a browser bookmarklet.
 * 
 * To use as bookmarklet:
 * 1. Copy the minified code below
 * 2. Create a new bookmark
 * 3. Set the URL to: javascript:[MINIFIED_CODE]
 * 4. Click the bookmark on any Instagram Reels page
 */

// Minified version for bookmarklet
javascript:(function(){console.log('🎬 Instagram Reels Extractor');const foundUrls=new Set();function extractReels(){const reels=[];document.querySelectorAll('a[href*="/reel/"]').forEach(link=>{const href=link.href;if(href&&href.includes('/reel/')&&!foundUrls.has(href)){foundUrls.add(href);reels.push(href);}});document.querySelectorAll('script').forEach(script=>{if(script.textContent){const patterns=[/https:\/\/www\.instagram\.com\/reel\/[A-Za-z0-9_-]+\/?/g,/\/reel\/[A-Za-z0-9_-]+\/?/g];patterns.forEach(pattern=>{const matches=script.textContent.match(pattern);if(matches){matches.forEach(match=>{let url=match;if(url.startsWith('/')){url='https://www.instagram.com'+url;}else if(!url.startsWith('http')){url='https://www.instagram.com/reel/'+url;}if(url.includes('/reel/')&&!foundUrls.has(url)){foundUrls.add(url);reels.push(url);}});}});}});return reels;}function cleanUrls(urls){return urls.map(url=>{let clean=url.split('?')[0];if(!clean.endsWith('/')){clean+='/';}return clean;}).sort();}async function scrollAndExtract(){let scrollCount=0;const maxScrolls=5;while(scrollCount<maxScrolls&&foundUrls.size<50){scrollCount++;window.scrollTo(0,document.body.scrollHeight);await new Promise(r=>setTimeout(r,2000));const newReels=extractReels();if(foundUrls.size===0)break;}return cleanUrls(Array.from(foundUrls));}scrollAndExtract().then(urls=>{console.log(`✅ Found ${urls.length} Reels:`);urls.forEach((url,i)=>console.log(`${i+1}. ${url}`));if(navigator.clipboard){navigator.clipboard.writeText(urls.join('\n')).then(()=>{alert(`📋 Copied ${urls.length} Reels URLs to clipboard!`);}).catch(()=>{console.log('❌ Could not copy to clipboard');});}else{console.log('❌ Clipboard not available');}});})();

/**
 * Full version for reference and development
 */
function fullVersion() {
    console.log('🎬 Instagram Reels URL Extractor - Bookmarklet');
    console.log('==============================================');
    
    const foundUrls = new Set();
    
    function extractReels() {
        const reels = [];
        
        // Method 1: Direct links
        document.querySelectorAll('a[href*="/reel/"]').forEach(link => {
            const href = link.href;
            if (href && href.includes('/reel/') && !foundUrls.has(href)) {
                foundUrls.add(href);
                reels.push(href);
            }
        });
        
        // Method 2: Script tags
        document.querySelectorAll('script').forEach(script => {
            if (script.textContent) {
                const patterns = [
                    /https:\/\/www\.instagram\.com\/reel\/[A-Za-z0-9_-]+\/?/g,
                    /\/reel\/[A-Za-z0-9_-]+\/?/g
                ];
                
                patterns.forEach(pattern => {
                    const matches = script.textContent.match(pattern);
                    if (matches) {
                        matches.forEach(match => {
                            let url = match;
                            if (url.startsWith('/')) {
                                url = 'https://www.instagram.com' + url;
                            } else if (!url.startsWith('http')) {
                                url = 'https://www.instagram.com/reel/' + url;
                            }
                            
                            if (url.includes('/reel/') && !foundUrls.has(url)) {
                                foundUrls.add(url);
                                reels.push(url);
                            }
                        });
                    }
                });
            }
        });
        
        return reels;
    }
    
    function cleanUrls(urls) {
        return urls.map(url => {
            let clean = url.split('?')[0];
            if (!clean.endsWith('/')) {
                clean += '/';
            }
            return clean;
        }).sort();
    }
    
    async function scrollAndExtract() {
        let scrollCount = 0;
        const maxScrolls = 5;
        
        // Initial extraction
        extractReels();
        
        // Scroll to load more
        while (scrollCount < maxScrolls && foundUrls.size < 50) {
            scrollCount++;
            window.scrollTo(0, document.body.scrollHeight);
            
            // Wait for content to load
            await new Promise(resolve => setTimeout(resolve, 2000));
            
            // Extract new Reels
            extractReels();
            
            // If no new content, stop scrolling
            if (foundUrls.size === 0) break;
        }
        
        return cleanUrls(Array.from(foundUrls));
    }
    
    scrollAndExtract().then(urls => {
        console.log(`✅ Found ${urls.length} Reels:`);
        urls.forEach((url, i) => {
            console.log(`${i + 1}. ${url}`);
        });
        
        // Copy to clipboard
        if (navigator.clipboard) {
            navigator.clipboard.writeText(urls.join('\n')).then(() => {
                alert(`📋 Copied ${urls.length} Reels URLs to clipboard!`);
            }).catch(() => {
                console.log('❌ Could not copy to clipboard');
            });
        } else {
            console.log('❌ Clipboard not available');
        }
    });
}
