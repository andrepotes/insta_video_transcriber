#!/usr/bin/env python3
"""
Instagram Video Transcriber
A tool to download Instagram videos and transcribe them to text files.
"""

import argparse
import os
import sys
from pathlib import Path
from urllib.parse import urlparse
import yt_dlp
from faster_whisper import WhisperModel
from pydub import AudioSegment
import tempfile
import re
import time
from datetime import datetime


class InstagramTranscriber:
    def __init__(self, output_dir="transcriptions"):
        """Initialize the transcriber with output directory."""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Initialize Whisper model (using small model for better accuracy)
        print("Loading Whisper model...")
        self.model = WhisperModel("small", device="cpu", compute_type="int8")
        print("Whisper model loaded successfully!")
    
    def is_valid_instagram_url(self, url):
        """Check if the URL is a valid Instagram URL."""
        parsed = urlparse(url)
        return parsed.netloc in ['www.instagram.com', 'instagram.com'] and ('/p/' in url or '/reel/' in url)
    
    def download_video(self, url):
        """Download Instagram video using yt-dlp."""
        print(f"Downloading video from: {url}")
        
        # Create temporary directory for download
        temp_dir = tempfile.mkdtemp()
        ydl_opts = {
            'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                
                # Find the downloaded file
                for file_path in Path(temp_dir).glob('*'):
                    if file_path.suffix.lower() in ['.mp4', '.webm', '.mkv', '.m4a', '.mp3']:
                        return str(file_path)
                
                print("Error: Could not find downloaded video file")
                return None
                
        except Exception as e:
            print(f"Error downloading video: {e}")
            return None
    
    def extract_audio(self, video_path):
        """Extract audio from video file."""
        print("Extracting audio from video...")
        try:
            # Load audio directly from video file
            audio = AudioSegment.from_file(video_path)
            return audio
        except Exception as e:
            print(f"Error extracting audio: {e}")
            return None
    
    def transcribe_audio(self, audio):
        """Transcribe audio using Whisper."""
        print("Transcribing audio...")
        try:
            # Export audio to temporary WAV file for Whisper
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_audio:
                audio.export(temp_audio.name, format="wav")
                
                # Transcribe using Whisper
                segments, info = self.model.transcribe(
                    temp_audio.name,
                    language="pt",
                    beam_size=5,
                    word_timestamps=True
                )
                
                # Clean up temporary file
                os.unlink(temp_audio.name)
                
                # Combine all segments into one transcription
                transcription = " ".join([segment.text for segment in segments])
                return transcription.strip()
                
        except Exception as e:
            print(f"Error transcribing audio: {e}")
            return None
    
    def save_transcription(self, transcription, url):
        """Save transcription to file."""
        # Extract post ID from URL
        post_id_match = re.search(r'/reel/([^/?]+)', url)
        post_id = post_id_match.group(1) if post_id_match else "unknown"
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"instagram_{post_id}_transcription_{timestamp}.txt"
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"Instagram Video Transcription\n")
            f.write(f"URL: {url}\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"{'='*50}\n\n")
            f.write(transcription)
        
        print(f"Transcription saved to: {filepath}")
        return filepath
    
    def transcribe_video(self, url):
        """Main method to transcribe a single video."""
        if not self.is_valid_instagram_url(url):
            print("Error: Please provide a valid Instagram post URL")
            return False
        
        # Download video
        video_path = self.download_video(url)
        if not video_path:
            return False
        
        # Extract audio
        audio = self.extract_audio(video_path)
        if not audio:
            return False
        
        # Transcribe audio
        transcription = self.transcribe_audio(audio)
        if not transcription:
            return False
        
        # Save transcription
        output_file = self.save_transcription(transcription, url)
        return output_file
    
    def parse_selection(self, selection_str, total_videos):
        """Parse selection string and return list of video indices."""
        if not selection_str:
            return list(range(1, total_videos + 1))  # Select all if no selection specified
        
        selected_indices = set()
        
        # Split by comma and process each part
        parts = [part.strip() for part in selection_str.split(',')]
        
        for part in parts:
            if '-' in part:
                # Range selection (e.g., "1-5")
                try:
                    start, end = map(int, part.split('-'))
                    if 1 <= start <= end <= total_videos:
                        selected_indices.update(range(start, end + 1))
                    else:
                        print(f"Warning: Invalid range {part}. Skipping.")
                except ValueError:
                    print(f"Warning: Invalid range format {part}. Skipping.")
            else:
                # Single number selection (e.g., "3")
                try:
                    num = int(part)
                    if 1 <= num <= total_videos:
                        selected_indices.add(num)
                    else:
                        print(f"Warning: Video {num} not found. Available: 1-{total_videos}. Skipping.")
                except ValueError:
                    print(f"Warning: Invalid number {part}. Skipping.")
        
        return sorted(list(selected_indices))
    
    def load_urls_from_file(self, file_path):
        """Load URLs from structured text file."""
        urls = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    
                    # Parse format: "1. https://www.example.com/reel/video/link"
                    match = re.match(r'^\d+\.\s+(.+)$', line)
                    if match:
                        url = match.group(1).strip()
                        if self.is_valid_instagram_url(url):
                            urls.append(url)
                        else:
                            print(f"Warning: Line {line_num} contains invalid URL: {url}")
                    else:
                        print(f"Warning: Line {line_num} doesn't match expected format: {line}")
            
            print(f"Loaded {len(urls)} valid URLs from file: {file_path}")
            return urls
            
        except Exception as e:
            print(f"Error loading URLs from file: {e}")
            return []
    
    def transcribe_selected_videos(self, urls, selected_indices, username="unknown"):
        """Transcribe selected videos from the URLs list."""
        if not urls:
            print("No URLs provided for batch processing")
            return False
        
        total_videos = len(urls)
        selected_count = len(selected_indices)
        
        print(f"Starting batch transcription for {selected_count} selected videos")
        print(f"Total videos in file: {total_videos}")
        print(f"Selected videos: {', '.join(map(str, selected_indices))}")
        
        # Progress callback
        def progress_callback(current, total, url):
            print(f"Progress: {current}/{total} - Processing: {url}")
        
        # Transcribe selected videos
        print(f"\nStarting transcription of {selected_count} videos...")
        transcriptions = []
        
        for i, video_index in enumerate(selected_indices, 1):
            print(f"\nProcessing video {i}/{selected_count} (File index: {video_index})")
            if progress_callback:
                progress_callback(i, selected_count, urls[video_index - 1])
            
            transcription = self.transcribe_video(urls[video_index - 1])
            if transcription:
                # Read the transcription text from the saved file
                try:
                    with open(transcription, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Extract just the transcription text (skip metadata)
                        lines = content.split('\n')
                        text_lines = []
                        skip_metadata = True
                        for line in lines:
                            if skip_metadata and line.startswith('=' * 50):
                                skip_metadata = False
                                continue
                            if not skip_metadata and line.strip():
                                text_lines.append(line.strip())
                        
                        transcription_text = ' '.join(text_lines)
                        transcriptions.append(transcription_text)
                        print(f"Video {i} transcribed successfully")
                except Exception as e:
                    print(f"Error reading transcription for video {i}: {e}")
            else:
                print(f"Failed to transcribe video {i}")
                transcriptions.append("")  # Add empty string for failed transcriptions
        
        # Save merged transcription
        output_file = self.save_batch_transcription(transcriptions, selected_indices, username)
        
        # Summary
        successful = sum(1 for t in transcriptions if t.strip())
        print(f"\nBatch transcription completed!")
        print(f"Successfully transcribed: {successful}/{len(transcriptions)} videos")
        print(f"Output file: {output_file}")
        
        return output_file
    
    def save_batch_transcription(self, transcriptions, selected_indices, username):
        """Save merged transcriptions from selected videos."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"instagram_{username}_batch_transcription_{timestamp}.txt"
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"Instagram Batch Transcription\n")
            f.write(f"Username: @{username}\n")
            f.write(f"Selected Videos: {', '.join(map(str, selected_indices))}\n")
            f.write(f"Total Videos: {len(transcriptions)}\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"{'='*60}\n\n")
            
            # Write all transcriptions separated by newlines
            for i, transcription in enumerate(transcriptions, 1):
                if transcription.strip():
                    f.write(f"{transcription.strip()}\n\n")
                else:
                    f.write(f"[Video {selected_indices[i-1]}: Transcription failed]\n\n")
        
        print(f"\nBatch transcription saved to: {filepath}")
        return filepath


def main():
    parser = argparse.ArgumentParser(description='Transcribe Instagram videos to text')
    parser.add_argument('url', nargs='?', help='Instagram video URL (for single video mode)')
    parser.add_argument('-f', '--file', help='Text file containing numbered Instagram URLs')
    parser.add_argument('-o', '--output', default='transcriptions', 
                        help='Output directory for transcriptions (default: transcriptions)')
    parser.add_argument('-s', '--select', help='Video selection (e.g., "1,3,5" or "1-10" or "2-5,8,10-12")')
    parser.add_argument('-u', '--username', default='unknown',
                        help='Username for batch processing (default: unknown)')
    
    args = parser.parse_args()
    
    # Validate arguments
    if not args.url and not args.file:
        print("Error: Please provide either a URL or a URLs file for processing")
        parser.print_help()
        sys.exit(1)
    
    if args.url and args.file:
        print("Error: Please provide either a URL or a URLs file, not both")
        parser.print_help()
        sys.exit(1)
    
    # Initialize transcriber
    transcriber = InstagramTranscriber(args.output)
    
    if args.file:
        # Batch processing mode
        print("Batch mode: Processing URLs from file")
        urls = transcriber.load_urls_from_file(args.file)
        if not urls:
            print("No valid URLs found in file")
            sys.exit(1)
        
        # Parse selection
        selected_indices = transcriber.parse_selection(args.select, len(urls))
        if not selected_indices:
            print("No valid videos selected")
            sys.exit(1)
        
        # Transcribe selected videos
        result = transcriber.transcribe_selected_videos(urls, selected_indices, args.username)
        
        if result:
            print(f"\nBatch transcription completed successfully!")
            print(f"Output file: {result}")
        else:
            print("\nBatch transcription failed.")
            sys.exit(1)
    else:
        # Single video processing
        print("Single video mode: Processing one video")
        result = transcriber.transcribe_video(args.url)
        
        if result:
            print(f"\nTranscription completed successfully!")
            print(f"Output file: {result}")
        else:
            print("\nTranscription failed. Please check the URL and try again.")
            sys.exit(1)


if __name__ == "__main__":
    main()