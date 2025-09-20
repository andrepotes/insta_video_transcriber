/**
 * Instagram Reels URL Extractor
 * 
 * This JavaScript code can be used in the browser console to extract
 * Reels URLs from Instagram profile pages.
 * 
 * Usage:
 * 1. Go to https://www.instagram.com/username/reels/
 * 2. Scroll down to load more Reels
 * 3. Open Developer Tools (F12) → Console tab
 * 4. Copy and paste this entire script
 * 5. Press Enter to run
 * 6. URLs will be copied to clipboard and displayed
 */

(function() {
    'use strict';
    
    console.log('🎬 Instagram Reels URL Extractor');
    console.log('================================');
    
    // Configuration
    const CONFIG = {
        maxReels: 20,           // Maximum number of Reels to extract (focus on recent ones)
        scrollDelay: 1500,      // Delay between scrolls (ms) - faster for recent content
        maxScrolls: 3,          // Maximum number of scroll attempts (focus on top content)
        autoScroll: false,      // Don't auto-scroll - focus on visible content first
        showProgress: true,     // Show progress during extraction
        prioritizeVisible: true // Prioritize currently visible Reels
    };
    
    // Storage for found URLs
    const foundUrls = new Set();
    let scrollCount = 0;
    let lastUrlCount = 0;
    
    /**
     * Extract Reels URLs from the current page, prioritizing visible ones
     */
    function extractReelsUrls() {
        const reels = [];
        
        // Method 1: Look for visible Reels in the main content area (PRIORITY)
        // These are the most recent Reels that are currently visible
        const mainContentSelectors = [
            'main a[href*="/reel/"]',           // Main content area
            'article a[href*="/reel/"]',        // Article elements
            '[role="main"] a[href*="/reel/"]',  // Main role elements
            'section a[href*="/reel/"]'         // Section elements
        ];
        
        mainContentSelectors.forEach(selector => {
            const links = document.querySelectorAll(selector);
            links.forEach(link => {
                const href = link.href;
                if (href && href.includes('/reel/') && !foundUrls.has(href)) {
                    foundUrls.add(href);
                    reels.push({
                        url: href,
                        element: link,
                        priority: 1, // High priority for visible elements
                        position: getElementPosition(link)
                    });
                }
            });
        });
        
        // Method 2: Look for Reels in the viewport (currently visible)
        const viewportReels = document.querySelectorAll('a[href*="/reel/"]');
        viewportReels.forEach(link => {
            const rect = link.getBoundingClientRect();
            const isInViewport = rect.top >= 0 && rect.left >= 0 && 
                               rect.bottom <= window.innerHeight && 
                               rect.right <= window.innerWidth;
            
            if (isInViewport) {
                const href = link.href;
                if (href && href.includes('/reel/') && !foundUrls.has(href)) {
                    foundUrls.add(href);
                    reels.push({
                        url: href,
                        element: link,
                        priority: 0, // Highest priority for viewport elements
                        position: getElementPosition(link)
                    });
                }
            }
        });
        
        // Method 3: Look in script tags for additional Reels (LOWER PRIORITY)
        // Only if we don't have enough visible Reels
        if (reels.length < CONFIG.maxReels) {
            const scripts = document.querySelectorAll('script');
            scripts.forEach(script => {
                if (script.textContent) {
                    const patterns = [
                        /https:\/\/www\.instagram\.com\/reel\/[A-Za-z0-9_-]+\/?/g,
                        /"\/reel\/[A-Za-z0-9_-]+\/?/g,
                        /instagram\.com\/reel\/[A-Za-z0-9_-]+\/?/g
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
                                    reels.push({
                                        url: url,
                                        element: null,
                                        priority: 3, // Lower priority for script content
                                        position: 999999
                                    });
                                }
                            });
                        }
                    });
                }
            });
        }
        
        // Sort by priority and position (most recent first)
        reels.sort((a, b) => {
            if (a.priority !== b.priority) {
                return a.priority - b.priority; // Lower priority number = higher priority
            }
            return a.position - b.position; // Lower position = higher on page
        });
        
        // Return only URLs, limited to maxReels
        return reels.slice(0, CONFIG.maxReels).map(item => item.url);
    }
    
    /**
     * Get the position of an element on the page
     */
    function getElementPosition(element) {
        let position = 0;
        let current = element;
        while (current && current.parentNode) {
            position += Array.from(current.parentNode.children).indexOf(current);
            current = current.parentNode;
        }
        return position;
    }
    
    /**
     * Clean and standardize URLs
     */
    function cleanUrls(urls) {
        return urls.map(url => {
            // Remove extra parameters and ensure proper format
            let cleanUrl = url.split('?')[0];
            if (!cleanUrl.endsWith('/')) {
                cleanUrl += '/';
            }
            return cleanUrl;
        });
    }
    
    /**
     * Scroll to load more Reels
     */
    function scrollToLoadMore() {
        return new Promise((resolve) => {
            const currentHeight = document.body.scrollHeight;
            
            // Scroll to bottom
            window.scrollTo(0, document.body.scrollHeight);
            
            // Wait for new content to load
            setTimeout(() => {
                const newHeight = document.body.scrollHeight;
                resolve(newHeight > currentHeight);
            }, CONFIG.scrollDelay);
        });
    }
    
    /**
     * Show progress
     */
    function showProgress() {
        if (CONFIG.showProgress) {
            console.log(`📊 Found ${foundUrls.size} Reels so far... (Scroll ${scrollCount}/${CONFIG.maxScrolls})`);
        }
    }
    
    /**
     * Main extraction function
     */
    async function extractAllReels() {
        console.log('🔍 Starting Reels extraction...');
        console.log(`📋 Max Reels: ${CONFIG.maxReels}`);
        console.log(`🔄 Auto-scroll: ${CONFIG.autoScroll ? 'Enabled' : 'Disabled'}`);
        console.log(`👁️ Prioritize Visible: ${CONFIG.prioritizeVisible ? 'Enabled' : 'Disabled'}`);
        console.log('');
        
        // First, extract visible Reels without scrolling
        console.log('📱 Extracting currently visible Reels...');
        let newReels = extractReelsUrls();
        showProgress();
        
        // If we have enough visible Reels, we're done
        if (foundUrls.size >= CONFIG.maxReels) {
            console.log(`✅ Found enough visible Reels (${foundUrls.size})`);
        } else if (CONFIG.autoScroll) {
            console.log('📜 Scrolling to load more Reels...');
            // Auto-scroll to load more Reels only if needed
            while (scrollCount < CONFIG.maxScrolls && foundUrls.size < CONFIG.maxReels) {
                scrollCount++;
                
                const hasNewContent = await scrollToLoadMore();
                if (!hasNewContent) {
                    console.log('📄 No new content loaded, stopping scroll');
                    break;
                }
                
                // Extract new Reels after scrolling
                newReels = extractReelsUrls();
                showProgress();
                
                // Check if we've reached the limit
                if (foundUrls.size >= CONFIG.maxReels) {
                    console.log(`🎯 Reached maximum Reels limit (${CONFIG.maxReels})`);
                    break;
                }
            }
        } else {
            console.log('📱 Using only visible Reels (auto-scroll disabled)');
        }
        
        // Clean and sort URLs
        const cleanUrls = cleanUrls(Array.from(foundUrls));
        const sortedUrls = cleanUrls.sort();
        
        console.log('');
        console.log('✅ Extraction Complete!');
        console.log(`📊 Total Reels found: ${sortedUrls.length}`);
        console.log('');
        
        // Display URLs
        if (sortedUrls.length > 0) {
            console.log('📋 Extracted Reels URLs:');
            console.log('========================');
            sortedUrls.forEach((url, index) => {
                console.log(`${index + 1}. ${url}`);
            });
            
            // Copy to clipboard
            if (navigator.clipboard) {
                try {
                    await navigator.clipboard.writeText(sortedUrls.join('\n'));
                    console.log('');
                    console.log('📋 URLs copied to clipboard!');
                    console.log('');
                    console.log('💡 Next steps:');
                    console.log('1. Create a structured URLs file:');
                    console.log('   python3 create_structured_urls.py bruno.casasdotejo --interactive');
                    console.log('2. Or create manually with format:');
                    console.log('   1. https://www.instagram.com/reel/ABC123/');
                    console.log('   2. https://www.instagram.com/reel/DEF456/');
                    console.log('3. Run transcription:');
                    console.log('   python3 main.py -f urls.txt -u bruno.casasdotejo');
                } catch (err) {
                    console.log('❌ Could not copy to clipboard:', err);
                    console.log('📋 Please copy the URLs manually from above');
                }
            } else {
                console.log('❌ Clipboard not available, please copy URLs manually');
            }
        } else {
            console.log('❌ No Reels found on this page');
            console.log('💡 Make sure you are on the Reels tab of an Instagram profile');
        }
        
        return sortedUrls;
    }
    
    /**
     * Create a visual popup with results
     */
    function createResultsPopup(urls) {
        const popup = document.createElement('div');
        popup.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 10000;
            background: #000;
            color: #fff;
            padding: 20px;
            border-radius: 8px;
            max-width: 400px;
            max-height: 300px;
            overflow-y: auto;
            font-family: Arial, sans-serif;
            font-size: 14px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            border: 2px solid #0095f6;
        `;
        
        popup.innerHTML = `
            <h3 style="margin: 0 0 10px 0; color: #0095f6;">🎬 Found ${urls.length} Reels</h3>
            <div style="max-height: 200px; overflow-y: auto; font-size: 12px;">
                ${urls.slice(0, 10).map((url, i) => 
                    `<div style="margin: 5px 0; word-break: break-all;">${i+1}. ${url}</div>`
                ).join('')}
                ${urls.length > 10 ? `<div style="color: #999;">... and ${urls.length - 10} more</div>` : ''}
            </div>
            <button onclick="this.parentElement.remove()" style="
                background: #0095f6;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                cursor: pointer;
                margin-top: 10px;
            ">Close</button>
        `;
        
        document.body.appendChild(popup);
    }
    
    // Start extraction
    extractAllReels().then(urls => {
        if (urls.length > 0) {
            createResultsPopup(urls);
        }
    });
    
})();
