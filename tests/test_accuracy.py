#!/usr/bin/env python3
"""
Accuracy Test Script
Tests the transcriber against known expected transcriptions.
"""

import os
import sys
from pathlib import Path
from difflib import SequenceMatcher
import re


def clean_text(text):
    """Clean text for comparison by removing extra whitespace and normalizing."""
    # Remove extra whitespace and normalize
    text = re.sub(r'\s+', ' ', text.strip())
    # Remove punctuation differences
    text = re.sub(r'[.,!?;:]', '', text)
    return text.lower()


def calculate_similarity(text1, text2):
    """Calculate similarity between two texts using SequenceMatcher."""
    clean1 = clean_text(text1)
    clean2 = clean_text(text2)
    return SequenceMatcher(None, clean1, clean2).ratio()


def load_expected_transcription(file_path):
    """Load expected transcription from file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Skip the first line (URL) and get the transcription
            lines = content.split('\n')[1:]  # Skip URL line
            transcription = '\n'.join(lines).strip()
            return transcription
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return None


def test_transcription_accuracy():
    """Test transcription accuracy against expected results."""
    print("Testing Instagram Video Transcriber Accuracy")
    print("=" * 50)
    
    # Test data files
    test_files = [
        {
            'file': 'tests/test_data/sample_1.txt',
            'url': 'https://www.instagram.com/reel/DIy_O6Ctilf/',
            'description': 'Website launch announcement'
        },
        {
            'file': 'tests/test_data/sample_2.txt', 
            'url': 'https://www.instagram.com/reel/DOypuuTCsYh/',
            'description': 'EPIs and EPCs safety equipment'
        },
        {
            'file': 'tests/test_data/sample_3.txt',
            'url': 'https://www.instagram.com/reel/DOtgIrljBDB/',
            'description': 'Construction site documentation requirements'
        },
        {
            'file': 'tests/test_data/sample_4.txt',
            'url': 'https://www.instagram.com/reel/DOoWf_YjHP6/',
            'description': 'Construction permits and legal requirements'
        }
    ]
    
    # Create structured URLs file for testing
    urls_file = "tests/test_accuracy_urls.txt"
    with open(urls_file, 'w', encoding='utf-8') as f:
        f.write("# Test URLs for accuracy testing\n")
        for i, test in enumerate(test_files, 1):
            f.write(f"{i}. {test['url']}\n")
    
    print(f"Created test URLs file: {urls_file}")
    print()
    
    # Run transcription
    print("Running transcription...")
    os.system(f"python3 main.py -f {urls_file}")
    print()
    
    # Check results
    results = []
    for i, test in enumerate(test_files, 1):
        print(f"Testing {i}: {test['description']}")
        print(f"URL: {test['url']}")
        
        # Load expected transcription
        expected = load_expected_transcription(test['file'])
        if not expected:
            print("❌ Could not load expected transcription")
            continue
        
        # Find the specific generated transcription file for this video
        video_id = test['url'].split('/reel/')[1].split('/')[0]
        transcriptions_dir = Path("transcriptions")
        generated_files = list(transcriptions_dir.glob(f"instagram_{video_id}_transcription_*.txt"))
        
        if not generated_files:
            print("❌ No generated transcription files found for this video")
            continue
        
        # Get the most recent file for this specific video
        latest_file = max(generated_files, key=os.path.getctime)
        
        try:
            with open(latest_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # Extract transcription (skip metadata)
                lines = content.split('\n')
                transcription_lines = []
                skip_metadata = True
                for line in lines:
                    if skip_metadata and line.startswith('=' * 50):
                        skip_metadata = False
                        continue
                    if not skip_metadata and line.strip():
                        transcription_lines.append(line.strip())
                
                generated = ' '.join(transcription_lines)
        except Exception as e:
            print(f"❌ Error reading generated file: {e}")
            continue
        
        # Calculate similarity
        similarity = calculate_similarity(expected, generated)
        percentage = similarity * 100
        
        print(f"Expected length: {len(expected)} characters")
        print(f"Generated length: {len(generated)} characters")
        print(f"Similarity: {percentage:.1f}%")
        
        if percentage >= 95:
            print("✅ Excellent accuracy!")
        elif percentage >= 90:
            print("✅ Good accuracy")
        elif percentage >= 80:
            print("⚠️  Acceptable accuracy")
        else:
            print("❌ Low accuracy")
        
        results.append({
            'description': test['description'],
            'similarity': percentage,
            'expected_length': len(expected),
            'generated_length': len(generated)
        })
        
        print("-" * 40)
        print()
    
    # Summary
    if results:
        avg_similarity = sum(r['similarity'] for r in results) / len(results)
        print("SUMMARY")
        print("=" * 20)
        print(f"Average accuracy: {avg_similarity:.1f}%")
        print(f"Tests passed: {len([r for r in results if r['similarity'] >= 90])}/{len(results)}")
        
        print("\nDetailed Results:")
        for result in results:
            status = "✅" if result['similarity'] >= 90 else "⚠️" if result['similarity'] >= 80 else "❌"
            print(f"{status} {result['description']}: {result['similarity']:.1f}%")
    
    # Cleanup
    if os.path.exists(urls_file):
        os.remove(urls_file)
        print(f"\nCleaned up {urls_file}")


if __name__ == "__main__":
    test_transcription_accuracy()
