# Instagram Video Transcriber

A Python tool that downloads Instagram videos and transcribes them to text files using OpenAI's Whisper model.

## Features

- Download Instagram videos from URLs
- Extract audio from videos
- Transcribe audio to text using Whisper AI
- Save transcriptions to organized text files
- Command-line interface for easy usage

## Installation

1. Clone or download this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Make sure you have FFmpeg installed on your system:
   - Ubuntu/Debian: `sudo apt install ffmpeg`
   - macOS: `brew install ffmpeg`
   - Windows: Download from https://ffmpeg.org/

## Usage

### Basic Usage

```bash
python main.py "https://www.instagram.com/p/VIDEO_ID/"
```

### Specify Output Directory

```bash
python main.py "https://www.instagram.com/p/VIDEO_ID/" -o my_transcriptions
```

## How It Works

1. **URL Validation**: Checks if the provided URL is a valid Instagram post URL
2. **Video Download**: Uses `yt-dlp` to download the Instagram video
3. **Audio Extraction**: Extracts audio from the video file
4. **Transcription**: Uses OpenAI Whisper to transcribe the audio to text
5. **File Output**: Saves the transcription to a text file with metadata

## Output

Transcriptions are saved as text files in the format:
- Filename: `instagram_{POST_ID}_transcription.txt`
- Content: Includes the original URL, timestamp, and transcribed text

## Requirements

- Python 3.7+
- FFmpeg
- Internet connection for downloading videos
- Sufficient disk space for temporary video/audio files

## Notes

- The tool uses the "base" Whisper model for a good balance of speed and accuracy
- Videos are limited to 720p for faster processing
- Temporary files are automatically cleaned up after processing
- Instagram URLs must be public posts (not private accounts)

## Troubleshooting

- If download fails, ensure the Instagram URL is public and accessible
- If transcription fails, check that FFmpeg is properly installed
- For better accuracy, consider using a larger Whisper model (change "base" to "small", "medium", or "large" in the code)
