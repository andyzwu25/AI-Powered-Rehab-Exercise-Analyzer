#!/usr/bin/env python3
"""Test script to check if modules can be imported"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app.models.pose_analyzer import PoseAnalyzer
    print("✓ Successfully imported PoseAnalyzer")
except ImportError as e:
    print(f"✗ Failed to import PoseAnalyzer: {e}")

try:
    from app.utils.file_utils import allowed_file, create_upload_folder
    print("✓ Successfully imported file_utils")
except ImportError as e:
    print(f"✗ Failed to import file_utils: {e}")

print("Current working directory:", os.getcwd())
print("Python path:", sys.path[:3])  # Show first 3 entries 