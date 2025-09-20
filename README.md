# Instagram Video Transcriber

A Python tool that downloads Instagram videos and transcribes them to text files using OpenAI's Whisper model.

## Features

- **Single Video Transcription**: Download and transcribe individual Instagram Reels
- **Batch Processing**: Process multiple videos from a structured URLs file
- **Flexible Selection**: Choose specific videos or ranges (e.g., "1,3,5" or "1-10")
- **High Accuracy**: Uses faster-whisper for 95-100% transcription accuracy
- **Portuguese Support**: Optimized for Portuguese language content
- **Progress Tracking**: Real-time progress updates during batch processing
- **Merged Output**: Combines multiple transcriptions into a single text file
- **Structured Input**: Clean, numbered URLs file format
- **Command-line Interface**: Easy-to-use CLI with comprehensive options

## Installation

1. Clone or download this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Single Video Transcription

```bash
python3 main.py "https://www.instagram.com/reel/VIDEO_ID/"
```

### Batch Processing (Multiple Videos)

#### Method 1: Using Structured URLs File
```bash
# Process all videos in file
python3 main.py -f urls.txt -u creator_name

# Process specific videos (individual selection)
python3 main.py -f urls.txt -u creator_name -s "1,3,5"

# Process range of videos
python3 main.py -f urls.txt -u creator_name -s "1-10"

# Process mixed selection
python3 main.py -f urls.txt -u creator_name -s "1,3-5,8,10-12"

# Specify output directory
python3 main.py -f urls.txt -u creator_name -o my_transcriptions
```

#### Method 2: Create Structured URLs File
```bash
# Interactive creation
python3 create_structured_urls.py bruno.casasdotejo --interactive

# From command line
python3 create_structured_urls.py bruno.casasdotejo --urls "URL1" "URL2" "URL3"

# From existing file
python3 create_structured_urls.py bruno.casasdotejo --file existing_urls.txt
```

### Structured URLs File Format

Create a text file with numbered Instagram Reel URLs:

```
# Instagram Reels URLs for @bruno.casasdotejo
# Format: number. URL
# Generated: 2024-09-20

1. https://www.instagram.com/reel/DIy_O6Ctilf/
2. https://www.instagram.com/reel/DOypuuTCsYh/
3. https://www.instagram.com/reel/DOtgIrljBDB/
4. https://www.instagram.com/reel/DOoWf_YjHP6/
5. https://www.instagram.com/reel/DOETVeCjLp4/
6. https://www.instagram.com/reel/DOJc_1NDAwe/
```

### Getting Reels URLs (Manual Methods)

Since Instagram restricts automated extraction, use these methods:

#### Browser Console Method (Easiest)
1. Go to the Instagram profile's Reels page
2. Open Developer Tools (F12) → Console tab
3. Run this JavaScript:
```javascript
const reels = [];
document.querySelectorAll('a[href*="/reel/"]').forEach(link => {
    const href = link.href;
    if (href.includes('/reel/') && !reels.includes(href)) {
        reels.push(href);
    }
});
console.log('Found Reels URLs:');
reels.forEach((url, index) => console.log(`${index + 1}. ${url}`));
navigator.clipboard.writeText(reels.join('\n'));
```
4. URLs will be copied to clipboard - paste into a text file
5. Use `create_structured_urls.py` to format them properly

### Command Line Options

```bash
python3 main.py [URL] [OPTIONS]

Options:
  -f, --file FILE        Text file containing numbered Instagram URLs
  -o, --output DIR       Output directory for transcriptions (default: transcriptions)
  -s, --select SELECTION Video selection (e.g., "1,3,5" or "1-10" or "2-5,8,10-12")
  -u, --username NAME    Username for batch processing (default: unknown)
```

### Selection Examples

```bash
# Select videos 1, 3, and 5
python3 main.py -f urls.txt -u username -s "1,3,5"

# Select videos 1 through 10
python3 main.py -f urls.txt -u username -s "1-10"

# Select videos 2 through 5, 8, and 10 through 12
python3 main.py -f urls.txt -u username -s "2-5,8,10-12"

# Select all videos (no -s option needed)
python3 main.py -f urls.txt -u username
```

## How It Works

1. **URL Validation**: Checks if the provided URL is a valid Instagram post URL
2. **Video Download**: Uses `yt-dlp` to download the Instagram video
3. **Audio Extraction**: Extracts audio from the video using `pydub`
4. **Transcription**: Uses `faster-whisper` to transcribe the audio to text
5. **File Output**: Saves the transcription to a text file with metadata

## File Structure

```
transcriptions/
├── instagram_VIDEO_ID_transcription_TIMESTAMP.txt  # Individual transcriptions
└── instagram_USERNAME_batch_transcription_TIMESTAMP.txt  # Batch transcriptions
```

## Requirements

- Python 3.7+
- yt-dlp
- faster-whisper
- pydub
- requests

## Troubleshooting

**"No valid URLs found in file"**: 
- Check that your URLs file follows the correct format
- Ensure URLs are valid Instagram Reel URLs
- Use `create_structured_urls.py` to format your URLs properly

**"Video X not found"**: 
- Check that the video number exists in your URLs file
- Ensure the selection syntax is correct (e.g., "1-5" not "1-5-10")

**"Transcription failed"**: 
- Check your internet connection
- Verify the Instagram URL is accessible
- Try downloading the video manually to test

## Examples

### Complete Workflow

1. **Get Reels URLs** using browser console method
2. **Create structured file**:
   ```bash
   python3 create_structured_urls.py bruno.casasdotejo --interactive
   ```
3. **Transcribe selected videos**:
   ```bash
   python3 main.py -f bruno_structured_urls.txt -u bruno.casasdotejo -s "1-4"
   ```

### Quick Start

```bash
# Create sample URLs file
echo "1. https://www.instagram.com/reel/VIDEO_ID/" > sample.txt

# Transcribe the video
python3 main.py -f sample.txt -u username
```

This tool provides a clean, structured approach to batch Instagram video transcription with flexible selection options!