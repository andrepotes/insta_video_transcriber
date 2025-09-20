#!/usr/bin/env python3
"""
Structured URLs File Creator
Creates a properly formatted URLs file from JavaScript console output or manual input.
"""

import argparse
import re
from datetime import datetime


def clean_url(url):
    """Clean and standardize a Reels URL."""
    # Remove extra parameters and ensure proper format
    clean_url = url.split('?')[0]
    if not clean_url.endswith('/'):
        clean_url += '/'
    return clean_url


def create_structured_urls_file(urls, username, output_file=None):
    """Create a structured URLs file from a list of URLs."""
    if not output_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"{username}_structured_urls_{timestamp}.txt"
    
    # Clean URLs
    clean_urls = [clean_url(url) for url in urls if '/reel/' in url]
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"# Instagram Reels URLs for @{username}\n")
        f.write(f"# Format: number. URL\n")
        f.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"# Total URLs: {len(clean_urls)}\n\n")
        
        for i, url in enumerate(clean_urls, 1):
            f.write(f"{i}. {url}\n")
    
    return output_file, clean_urls


def main():
    parser = argparse.ArgumentParser(description='Create structured Instagram Reels URLs file')
    parser.add_argument('username', help='Instagram username (without @)')
    parser.add_argument('-o', '--output', help='Output file name')
    parser.add_argument('--urls', nargs='+', help='Reels URLs to include')
    parser.add_argument('--file', help='File containing Reels URLs (one per line)')
    parser.add_argument('--interactive', action='store_true', help='Interactive mode for manual input')
    
    args = parser.parse_args()
    
    urls = []
    
    # Get URLs from command line arguments
    if args.urls:
        urls.extend(args.urls)
    
    # Get URLs from file
    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '/reel/' in line:
                        urls.append(line)
        except Exception as e:
            print(f"Error reading file {args.file}: {e}")
            return
    
    # Interactive mode
    if args.interactive or not urls:
        print(f"Structured URLs File Creator for @{args.username}")
        print("Enter Reels URLs (one per line, press Enter twice when done):")
        print("You can paste multiple URLs at once.")
        print()
        
        while True:
            url = input("Reels URL: ").strip()
            if not url:
                break
            if '/reel/' in url:
                urls.append(url)
            else:
                print("Warning: This doesn't look like a Reels URL. Skipping...")
    
    if not urls:
        print("No URLs provided. Exiting.")
        return
    
    # Create the structured file
    output_file, clean_urls = create_structured_urls_file(urls, args.username, args.output)
    
    print(f"\nSuccess! Created {output_file} with {len(clean_urls)} URLs:")
    for i, url in enumerate(clean_urls, 1):
        print(f"  {i}. {url}")
    
    print(f"\nTo transcribe these Reels, run:")
    print(f"python3 main.py -f {output_file} -u {args.username}")
    print(f"\nTo transcribe specific videos, use --select option:")
    print(f"python3 main.py -f {output_file} -u {args.username} -s '1,3,5'")
    print(f"python3 main.py -f {output_file} -u {args.username} -s '1-4'")
    print(f"python3 main.py -f {output_file} -u {args.username} -s '2-5,8,10-12'")


if __name__ == "__main__":
    main()
