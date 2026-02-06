"""
Main entry point for MBTI Desktop Pet
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from PyQt5.QtWidgets import QApplication

# Add src directory to path
src_path = Path(__file__).parent.parent
sys.path.insert(0, str(src_path))

from mbti_pet.config import ConfigManager
from mbti_pet.mbti_select import MBTISelectDialog
from mbti_pet.pet_window import PetWindow


def main():
    """Main application entry point with new desktop pet workflow"""
    # Load environment variables
    load_dotenv()
    
    # Create data and assets directories if they don't exist
    data_dir = Path("./data")
    data_dir.mkdir(exist_ok=True)
    
    assets_dir = Path("./assets/pets")
    assets_dir.mkdir(parents=True, exist_ok=True)
    
    print("Starting MBTI Desktop Pet...")
    print("=" * 50)
    print("Welcome to your intelligent MBTI-based desktop companion!")
    print("=" * 50)
    
    # Create QApplication
    app = QApplication(sys.argv)
    app.setApplicationName("MBTI Desktop Pet")
    app.setQuitOnLastWindowClosed(True)
    
    # Initialize config manager
    config_manager = ConfigManager()
    
    # Check if MBTI type is already configured
    mbti_type = config_manager.get_mbti_type()
    
    if not mbti_type:
        # No saved configuration - show MBTI selection dialog
        print("No MBTI type configured. Showing selection dialog...")
        
        dialog = MBTISelectDialog(config_manager)
        result = dialog.exec_()
        
        if result == MBTISelectDialog.Accepted:
            mbti_type = dialog.get_selected_type()
            print(f"Selected MBTI type: {mbti_type}")
        else:
            # User cancelled - exit
            print("No MBTI type selected. Exiting...")
            return
    else:
        print(f"Loaded MBTI type from config: {mbti_type}")
    
    # Create and show desktop pet window
    pet_window = PetWindow(mbti_type, config_manager)
    pet_window.show()
    
    print(f"Desktop pet window created with {mbti_type} personality")
    print("Right-click on the pet for menu options")
    print("Click on the pet to open chat window")
    print("=" * 50)
    
    # Start event loop
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
