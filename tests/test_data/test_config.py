"""
Test configuration and data for Instagram Video Transcriber tests
"""

# Test Instagram URLs and their expected transcriptions
TEST_CASES = {
    "reel_1": {
        "url": "https://www.instagram.com/reel/DOETVeCjLp4/?utm_source=ig_web_copy_link&igsh=MzRlODBiNWFlZA==",
        "expected_file": "expected_transcription_1.txt",
        "description": "Construction and architecture advice video"
    },
    "reel_2": {
        "url": "https://www.instagram.com/reel/DOJc_1NDAwe/?utm_source=ig_web_copy_link&igsh=MzRlODBiNWFlZA==",
        "expected_file": "expected_transcription_2.txt", 
        "description": "Thermal and plumbing construction advice video"
    }
}

# Minimum accuracy thresholds for different test types
ACCURACY_THRESHOLDS = {
    "minimum": 80.0,    # Minimum acceptable accuracy
    "good": 90.0,       # Good accuracy
    "excellent": 95.0   # Excellent accuracy
}

# Test configuration
TEST_CONFIG = {
    "skip_integration_tests": False,  # Set to True to skip slow integration tests
    "mock_transcription": True,       # Use mocked transcription for faster tests
    "test_timeout": 300,              # Timeout for transcription tests in seconds
}
