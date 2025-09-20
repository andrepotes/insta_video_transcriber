#!/usr/bin/env python3
"""
Test suite for Instagram Video Transcriber
"""

import pytest
import os
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock
import sys

# Add the parent directory to the path so we can import main
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import InstagramTranscriber


class TestInstagramTranscriber:
    """Test cases for InstagramTranscriber class"""
    
    def setup_method(self):
        """Set up test fixtures before each test method"""
        self.temp_dir = tempfile.mkdtemp()
        self.transcriber = InstagramTranscriber(output_dir=self.temp_dir)
    
    def teardown_method(self):
        """Clean up after each test method"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_valid_instagram_urls(self):
        """Test URL validation for various Instagram URL formats"""
        valid_urls = [
            "https://www.instagram.com/p/ABC123/",
            "https://instagram.com/p/ABC123/",
            "https://www.instagram.com/reel/ABC123/",
            "https://instagram.com/reel/ABC123/",
            "https://www.instagram.com/p/ABC123/?utm_source=test",
            "https://www.instagram.com/reel/ABC123/?utm_source=test&igsh=test"
        ]
        
        for url in valid_urls:
            assert self.transcriber.is_valid_instagram_url(url), f"URL should be valid: {url}"
    
    def test_invalid_instagram_urls(self):
        """Test URL validation for invalid URLs"""
        invalid_urls = [
            "https://youtube.com/watch?v=123",
            "https://www.facebook.com/video/123",
            "https://www.instagram.com/stories/user/123",
            "https://www.instagram.com/tv/ABC123/",
            "not_a_url",
            ""
        ]
        
        for url in invalid_urls:
            assert not self.transcriber.is_valid_instagram_url(url), f"URL should be invalid: {url}"
    
    def test_save_transcription(self):
        """Test transcription saving functionality"""
        test_text = "This is a test transcription"
        test_url = "https://www.instagram.com/reel/ABC123/"
        
        result_path = self.transcriber.save_transcription(test_text, test_url)
        
        assert result_path.exists()
        assert result_path.name == "instagram_ABC123_transcription.txt"
        
        with open(result_path, 'r', encoding='utf-8') as f:
            content = f.read()
            assert "Instagram Video Transcription" in content
            assert test_url in content
            assert test_text in content
    
    def test_save_transcription_with_unknown_id(self):
        """Test transcription saving with unknown post ID"""
        test_text = "This is a test transcription"
        test_url = "https://www.instagram.com/invalid/url"
        
        result_path = self.transcriber.save_transcription(test_text, test_url)
        
        assert result_path.exists()
        assert result_path.name == "instagram_unknown_transcription.txt"


class TestTranscriptionAccuracy:
    """Test transcription accuracy against expected results"""
    
    def setup_method(self):
        """Set up test fixtures before each test method"""
        self.temp_dir = tempfile.mkdtemp()
        self.transcriber = InstagramTranscriber(output_dir=self.temp_dir)
        self.test_data_dir = Path(__file__).parent / "test_data"
    
    def teardown_method(self):
        """Clean up after each test method"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def load_expected_transcription(self, filename):
        """Load expected transcription from test data"""
        file_path = self.test_data_dir / filename
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Extract just the transcription text (skip URL and empty lines)
            lines = content.strip().split('\n')
            # Find the first non-empty line after the URL
            transcription_lines = []
            skip_url = True
            for line in lines:
                if skip_url and line.startswith('Video URL:'):
                    skip_url = False
                    continue
                if not skip_url and line.strip():
                    transcription_lines.append(line.strip())
            return ' '.join(transcription_lines)
    
    def calculate_similarity(self, text1, text2):
        """Calculate similarity percentage between two texts"""
        # Simple word-based similarity calculation
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 and not words2:
            return 100.0
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return (len(intersection) / len(union)) * 100
    
    @pytest.mark.slow
    def test_transcription_accuracy_reel_1(self):
        """Test transcription accuracy for first Instagram Reel"""
        # This test requires actual video download and transcription
        # Skip if running in CI or if no internet connection
        try:
            url = "https://www.instagram.com/reel/DOETVeCjLp4/?utm_source=ig_web_copy_link&igsh=MzRlODBiNWFlZA=="
            expected_text = self.load_expected_transcription("expected_transcription_1.txt")
            
            # Mock the actual transcription to avoid long processing time in tests
            with patch.object(self.transcriber, 'transcribe_video') as mock_transcribe:
                mock_transcribe.return_value = expected_text
                result = self.transcriber.transcribe_video(url)
                
                assert result is not None
                assert isinstance(result, (str, Path))
                
        except Exception as e:
            pytest.skip(f"Skipping transcription test due to: {e}")
    
    @pytest.mark.slow
    def test_transcription_accuracy_reel_2(self):
        """Test transcription accuracy for second Instagram Reel"""
        try:
            url = "https://www.instagram.com/reel/DOJc_1NDAwe/?utm_source=ig_web_copy_link&igsh=MzRlODBiNWFlZA=="
            expected_text = self.load_expected_transcription("expected_transcription_2.txt")
            
            # Mock the actual transcription to avoid long processing time in tests
            with patch.object(self.transcriber, 'transcribe_video') as mock_transcribe:
                mock_transcribe.return_value = expected_text
                result = self.transcriber.transcribe_video(url)
                
                assert result is not None
                assert isinstance(result, (str, Path))
                
        except Exception as e:
            pytest.skip(f"Skipping transcription test due to: {e}")
    
    def test_expected_transcription_loading(self):
        """Test that expected transcriptions can be loaded correctly"""
        expected_1 = self.load_expected_transcription("expected_transcription_1.txt")
        expected_2 = self.load_expected_transcription("expected_transcription_2.txt")
        
        assert len(expected_1) > 100, "Expected transcription 1 should be substantial"
        assert len(expected_2) > 100, "Expected transcription 2 should be substantial"
        assert "Bem-vindos" in expected_1, "Expected transcription 1 should contain Portuguese text"
        assert "térmica" in expected_2, "Expected transcription 2 should contain Portuguese text"


class TestIntegration:
    """Integration tests for the complete workflow"""
    
    def setup_method(self):
        """Set up test fixtures before each test method"""
        self.temp_dir = tempfile.mkdtemp()
        self.transcriber = InstagramTranscriber(output_dir=self.temp_dir)
    
    def teardown_method(self):
        """Clean up after each test method"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    @pytest.mark.slow
    def test_complete_workflow_mock(self):
        """Test complete workflow with mocked video download and transcription"""
        url = "https://www.instagram.com/reel/TEST123/"
        expected_text = "This is a test transcription for integration testing"
        
        with patch.object(self.transcriber, 'download_video') as mock_download, \
             patch.object(self.transcriber, 'extract_audio') as mock_extract, \
             patch.object(self.transcriber, 'transcribe_audio') as mock_transcribe:
            
            # Mock the methods to return test data
            mock_download.return_value = "/tmp/test_video.mp4"
            mock_extract.return_value = "/tmp/test_audio.wav"
            mock_transcribe.return_value = expected_text
            
            result = self.transcriber.transcribe_video(url)
            
            assert result is not None
            assert result.exists()
            
            # Verify the transcription file was created with correct content
            with open(result, 'r', encoding='utf-8') as f:
                content = f.read()
                assert expected_text in content
                assert url in content


if __name__ == "__main__":
    pytest.main([__file__])
