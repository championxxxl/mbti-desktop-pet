#!/usr/bin/env python
"""
Manual test script for MBTI Desktop Pet UI
This script allows you to test the desktop pet in an X11 environment
"""

import sys
import os
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Import main function
from mbti_pet.main import main

if __name__ == "__main__":
    print("=" * 70)
    print("MBTI Desktop Pet - Manual Test")
    print("=" * 70)
    print()
    print("This will launch the desktop pet application.")
    print()
    print("Test checklist:")
    print("1. MBTI Selection Dialog should appear if no config exists")
    print("2. You should be able to select a personality type")
    print("3. Desktop pet should appear on screen as transparent window")
    print("4. You should be able to drag the pet around")
    print("5. Right-click should show context menu")
    print("6. Clicking pet should open chat window")
    print("7. Emoji should display if no GIF file exists")
    print()
    print("=" * 70)
    print()
    
    # Run the application
    main()
