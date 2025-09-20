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

// Minified version for bookmarklet - Respects DOM order (pinned first, then chronological)
javascript:(async function(){console.log('🎬 Instagram Reels Extractor');const foundUrls=new Set();function extractReels(){const reels=[];document.querySelectorAll('a[href*="/reel/"]').forEach(link=>{const href=link.href;if(href&&href.includes('/reel/')&&!foundUrls.has(href)){foundUrls.add(href);reels.push({url:href,domOrder:reels.length});}});reels.sort((a,b)=>a.domOrder-b.domOrder);return reels.slice(0,200).map(item=>item.url);}function cleanUrls(urls){return urls.map(url=>{let clean=url.split('?')[0];if(!clean.endsWith('/')){clean+='/';}return clean;});}async function scrollAndExtract(){let scrollCount=0;const maxScrolls=10;const maxReels=200;let noNewContentCount=0;const maxNoNewContent=2;extractReels();console.log(`📊 Found ${foundUrls.size} Reels initially...`);while(scrollCount<maxScrolls&&foundUrls.size<maxReels){scrollCount++;const beforeScroll=foundUrls.size;window.scrollTo(0,document.body.scrollHeight);setTimeout(()=>{window.scrollTo(0,document.body.scrollHeight-1000);setTimeout(()=>{window.scrollTo(0,document.body.scrollHeight);},200);},200);await new Promise(resolve=>setTimeout(resolve,2500));extractReels();const afterScroll=foundUrls.size;if(afterScroll>beforeScroll){noNewContentCount=0;console.log(`✅ Found ${afterScroll-beforeScroll} new Reels (Total: ${afterScroll})`);}else{noNewContentCount++;console.log(`⚠️ No new Reels found (${noNewContentCount}/${maxNoNewContent})`);}if(noNewContentCount>=maxNoNewContent){console.log('📄 No new content found after multiple attempts, stopping scroll');break;}await new Promise(resolve=>setTimeout(resolve,500));}return cleanUrls(Array.from(foundUrls));}try{const reels=await scrollAndExtract();const structuredUrls=reels.map((url,i)=>`${i+1}. ${url}`).join('\n');console.log(`✅ Found ${reels.length} Reels:`);reels.forEach((url,i)=>console.log(`${i+1}. ${url}`));if(navigator.clipboard){await navigator.clipboard.writeText(structuredUrls);alert(`📋 Copied ${reels.length} structured URLs to clipboard!\n\nPaste into a text file and run:\npython3 main.py -f urls.txt`);}else{console.log('❌ Clipboard not available');}}catch(err){console.log('❌ Error:',err);}})();

/**
 * Full version for reference and development
 */
function fullVersion() {
    console.log('🎬 Instagram Reels URL Extractor - Bookmarklet');
    console.log('==============================================');
    
    const foundUrls = new Set();
    
    function extractReels() {
        const reels = [];
        
        // Get all Reels in DOM order (respects Instagram's sorting)
        // This includes pinned Reels first, then chronological order
        document.querySelectorAll('a[href*="/reel/"]').forEach(link => {
            const href = link.href;
            if (href && href.includes('/reel/') && !foundUrls.has(href)) {
                foundUrls.add(href);
                reels.push({
                    url: href,
                    domOrder: reels.length
                });
            }
        });
        
        // Sort by DOM order (first appearing on page = first in list)
        reels.sort((a, b) => a.domOrder - b.domOrder);
        
        return reels.map(item => item.url);
    }
    
    function cleanUrls(urls) {
        return urls.map(url => {
            let clean = url.split('?')[0];
            if (!clean.endsWith('/')) {
                clean += '/';
            }
            return clean;
        }); // Don't sort - maintain order (most recent first)
    }
    
    async function scrollAndExtract() {
        let scrollCount = 0;
        const maxScrolls = 10;
        const maxReels = 200;
        let noNewContentCount = 0;
        const maxNoNewContent = 2;
        
        // Initial extraction
        extractReels();
        console.log(`📊 Found ${foundUrls.size} Reels initially...`);
        
        // Scroll to load more
        while (scrollCount < maxScrolls && foundUrls.size < maxReels) {
            scrollCount++;
            const beforeScroll = foundUrls.size;
            
            // Scroll to bottom
            window.scrollTo(0, document.body.scrollHeight);
            
            // Try scroll up and down to trigger lazy loading
            setTimeout(() => {
                window.scrollTo(0, document.body.scrollHeight - 1000);
                setTimeout(() => {
                    window.scrollTo(0, document.body.scrollHeight);
                }, 200);
            }, 200);
            
            // Wait for content to load
            await new Promise(resolve => setTimeout(resolve, 2500));
            
            // Extract new Reels
            extractReels();
            const afterScroll = foundUrls.size;
            
            // Check if we found new URLs
            if (afterScroll > beforeScroll) {
                noNewContentCount = 0;
                console.log(`✅ Found ${afterScroll - beforeScroll} new Reels (Total: ${afterScroll})`);
            } else {
                noNewContentCount++;
                console.log(`⚠️ No new Reels found (${noNewContentCount}/${maxNoNewContent})`);
            }
            
            // Stop if no new content for too many attempts
            if (noNewContentCount >= maxNoNewContent) {
                console.log('📄 No new content found after multiple attempts, stopping scroll');
                break;
            }
            
            // Small delay between scrolls
            await new Promise(resolve => setTimeout(resolve, 500));
        }
        
        return cleanUrls(Array.from(foundUrls));
    }
    
    scrollAndExtract().then(urls => {
        console.log(`✅ Found ${urls.length} Reels:`);
        urls.forEach((url, i) => {
            console.log(`${i + 1}. ${url}`);
        });
        
        // Generate structured format for direct use with main.py
        const structuredUrls = urls.map((url, i) => `${i + 1}. ${url}`).join('\n');
        
        // Copy structured URLs to clipboard
        if (navigator.clipboard) {
            navigator.clipboard.writeText(structuredUrls).then(() => {
                alert(`📋 Copied ${urls.length} structured URLs to clipboard!\n\nPaste into a text file and run:\npython3 main.py -f urls.txt`);
            }).catch(() => {
                console.log('❌ Could not copy to clipboard');
            });
        } else {
            console.log('❌ Clipboard not available');
        }
    });
}
