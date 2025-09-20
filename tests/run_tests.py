#!/usr/bin/env python3
"""
Test Runner
Runs all tests for the Instagram Video Transcriber.
"""

import os
import sys
import subprocess
from pathlib import Path


def run_accuracy_test():
    """Run the accuracy test."""
    print("Running Accuracy Test")
    print("=" * 30)
    
    # Change to project root directory
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    # Run accuracy test
    result = subprocess.run([sys.executable, "tests/test_accuracy.py"], 
                          capture_output=True, text=True)
    
    print(result.stdout)
    if result.stderr:
        print("Errors:")
        print(result.stderr)
    
    return result.returncode == 0


def run_unit_tests():
    """Run unit tests if they exist."""
    print("\nRunning Unit Tests")
    print("=" * 30)
    
    # Check if pytest is available
    try:
        result = subprocess.run([sys.executable, "-m", "pytest", "tests/", "-v"], 
                              capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("Errors:")
            print(result.stderr)
        return result.returncode == 0
    except FileNotFoundError:
        print("pytest not found, skipping unit tests")
        return True


def main():
    """Run all tests."""
    print("Instagram Video Transcriber - Test Suite")
    print("=" * 50)
    
    # Run accuracy test
    accuracy_passed = run_accuracy_test()
    
    # Run unit tests
    unit_passed = run_unit_tests()
    
    # Summary
    print("\nTest Summary")
    print("=" * 20)
    print(f"Accuracy Test: {'✅ PASSED' if accuracy_passed else '❌ FAILED'}")
    print(f"Unit Tests: {'✅ PASSED' if unit_passed else '❌ FAILED'}")
    
    if accuracy_passed and unit_passed:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print("\n❌ Some tests failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
