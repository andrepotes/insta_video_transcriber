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
    
    def download_video(self, url, temp_dir):
        """Download Instagram video using yt-dlp."""
        print(f"Downloading video from: {url}")
        
        ydl_opts = {
            'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
            'format': 'best',  # Use best available format
            'quiet': False,
            'no_warnings': False,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                # Find the downloaded file
                for file in os.listdir(temp_dir):
                    if file.endswith(('.mp4', '.webm', '.mkv', '.m4a', '.mp3')):
                        return os.path.join(temp_dir, file)
        except Exception as e:
            print(f"Error downloading video: {e}")
            return None
    
    def extract_audio(self, video_path, temp_dir):
        """Extract audio from video file using pydub."""
        print("Extracting audio from video...")
        
        try:
            # Load video and extract audio
            audio = AudioSegment.from_file(video_path)
            audio_path = os.path.join(temp_dir, "audio.wav")
            
            # Export as WAV for speech recognition
            audio.export(audio_path, format="wav")
            return audio_path
        except Exception as e:
            print(f"Error extracting audio: {e}")
            return None
    
    def transcribe_audio(self, audio_path):
        """Transcribe audio using Faster Whisper."""
        print("Transcribing audio...")
        
        try:
            # Use Faster Whisper to transcribe with Portuguese language hint
            segments, info = self.model.transcribe(
                audio_path, 
                language="pt",  # Portuguese language
                beam_size=5,    # Better accuracy
                word_timestamps=True
            )
            
            # Combine all segments into full text
            full_text = ""
            for segment in segments:
                full_text += segment.text + " "
            
            return full_text.strip()
        except Exception as e:
            print(f"Error transcribing audio: {e}")
            return None
    
    def save_transcription(self, text, original_url):
        """Save transcription to text file."""
        # Create filename from URL - extract the actual post ID
        import re
        match = re.search(r'/reel/([^/?]+)', original_url) or re.search(r'/p/([^/?]+)', original_url)
        if match:
            post_id = match.group(1)
        else:
            post_id = "unknown"
        filename = f"instagram_{post_id}_transcription.txt"
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"Instagram Video Transcription\n")
            f.write(f"URL: {original_url}\n")
            f.write(f"{'='*50}\n\n")
            f.write(text)
        
        print(f"Transcription saved to: {filepath}")
        return filepath
    
    def transcribe_video(self, url):
        """Main method to transcribe an Instagram video."""
        if not self.is_valid_instagram_url(url):
            print("Error: Please provide a valid Instagram post URL")
            return False
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Download video
            video_path = self.download_video(url, temp_dir)
            if not video_path:
                return False
            
            # Extract audio
            audio_path = self.extract_audio(video_path, temp_dir)
            if not audio_path:
                return False
            
            # Transcribe audio
            transcription = self.transcribe_audio(audio_path)
            if not transcription:
                return False
            
            # Save transcription
            output_file = self.save_transcription(transcription, url)
            return output_file


def main():
    parser = argparse.ArgumentParser(description='Transcribe Instagram videos to text')
    parser.add_argument('url', help='Instagram video URL')
    parser.add_argument('-o', '--output', default='transcriptions', 
                       help='Output directory for transcriptions (default: transcriptions)')
    
    args = parser.parse_args()
    
    # Initialize transcriber
    transcriber = InstagramTranscriber(args.output)
    
    # Transcribe the video
    result = transcriber.transcribe_video(args.url)
    
    if result:
        print(f"\n✅ Transcription completed successfully!")
        print(f"📁 Output file: {result}")
    else:
        print("\n❌ Transcription failed. Please check the URL and try again.")
        sys.exit(1)


if __name__ == "__main__":
    main()
