#!/usr/bin/env python
"""
Screenshot test script - Creates screenshots of the UI components
"""

import sys
import os
import tempfile
from pathlib import Path

# Set headless mode but allow screenshots
os.environ['QT_QPA_PLATFORM'] = 'offscreen'

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from mbti_pet.config import ConfigManager
from mbti_pet.mbti_select import MBTISelectDialog
from mbti_pet.pet_window import PetWindow

def take_screenshot(widget, filename):
    """Take a screenshot of a widget"""
    from PyQt5.QtGui import QPixmap
    pixmap = widget.grab()
    pixmap.save(filename)
    print(f"Screenshot saved: {filename}")

def main():
    app = QApplication(sys.argv)
    
    # Create temp config using cross-platform temp directory
    temp_dir = Path(tempfile.gettempdir())
    config_path = temp_dir / "test_config.json"
    config_manager = ConfigManager(str(config_path))
    
    # Screenshot 1: MBTI Selection Dialog
    print("Creating MBTI Selection Dialog screenshot...")
    dialog = MBTISelectDialog(config_manager)
    dialog.show()
    
    screenshot_path = temp_dir / "mbti_select_dialog.png"
    QTimer.singleShot(500, lambda: [
        take_screenshot(dialog, str(screenshot_path)),
        dialog.close()
    ])
    
    # Screenshot 2: Pet Window
    def screenshot_pet():
        print("Creating Pet Window screenshot...")
        pet = PetWindow("ENFP", config_manager)
        pet.show()
        
        pet_screenshot_path = temp_dir / "pet_window.png"
        QTimer.singleShot(500, lambda: [
            take_screenshot(pet, str(pet_screenshot_path)),
            pet.close(),
            app.quit()
        ])
    
    QTimer.singleShot(1000, screenshot_pet)
    
    app.exec_()
    print("\nScreenshots created successfully!")
    print(f"Check {temp_dir}/mbti_select_dialog.png and {temp_dir}/pet_window.png")

if __name__ == "__main__":
    main()
