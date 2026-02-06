"""
Main entry point for MBTI Desktop Pet
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add src directory to path
src_path = Path(__file__).parent.parent
sys.path.insert(0, str(src_path))

from mbti_pet.ui import main as ui_main


def main():
    """Main application entry point"""
    # Load environment variables
    load_dotenv()
    
    # Create data directory if it doesn't exist
    data_dir = Path("./data")
    data_dir.mkdir(exist_ok=True)
    
    # Launch UI
    print("Starting MBTI Desktop Pet...")
    print("=" * 50)
    print("Welcome to your intelligent MBTI-based desktop companion!")
    print("=" * 50)
    
    ui_main()


if __name__ == "__main__":
    main()
