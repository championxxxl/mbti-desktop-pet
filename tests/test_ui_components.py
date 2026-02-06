"""
Basic tests for MBTI Selection and Pet Window
Tests that components can be instantiated (UI tests in headless environment)
"""

import sys
import os
from pathlib import Path

# Set up headless Qt for testing
os.environ['QT_QPA_PLATFORM'] = 'offscreen'

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

import pytest
from PyQt5.QtWidgets import QApplication

from mbti_pet.config import ConfigManager
from mbti_pet.mbti_select import MBTISelectDialog
from mbti_pet.pet_window import PetWindow


@pytest.fixture(scope="module")
def qapp():
    """Create QApplication for testing"""
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    yield app


class TestMBTISelectDialog:
    """Test MBTI Selection Dialog"""
    
    def test_dialog_creation(self, qapp, tmp_path):
        """Test that dialog can be created"""
        config_path = tmp_path / "config.json"
        config_manager = ConfigManager(str(config_path))
        
        dialog = MBTISelectDialog(config_manager)
        assert dialog is not None
        assert dialog.selected_type is None
    
    def test_dialog_has_groups(self, qapp, tmp_path):
        """Test that dialog has all MBTI groups"""
        config_path = tmp_path / "config.json"
        config_manager = ConfigManager(str(config_path))
        
        dialog = MBTISelectDialog(config_manager)
        
        # Check that all groups are defined
        assert "分析家 Analysts" in dialog.MBTI_GROUPS
        assert "外交家 Diplomats" in dialog.MBTI_GROUPS
        assert "守卫者 Sentinels" in dialog.MBTI_GROUPS
        assert "探险家 Explorers" in dialog.MBTI_GROUPS
    
    def test_dialog_has_all_types(self, qapp, tmp_path):
        """Test that dialog includes all 16 MBTI types"""
        config_path = tmp_path / "config.json"
        config_manager = ConfigManager(str(config_path))
        
        dialog = MBTISelectDialog(config_manager)
        
        all_types = []
        for group_data in dialog.MBTI_GROUPS.values():
            all_types.extend(group_data["types"])
        
        expected_types = [
            "INTJ", "INTP", "ENTJ", "ENTP",
            "INFJ", "INFP", "ENFJ", "ENFP",
            "ISTJ", "ISFJ", "ESTJ", "ESFJ",
            "ISTP", "ISFP", "ESTP", "ESFP"
        ]
        
        assert sorted(all_types) == sorted(expected_types)


class TestPetWindow:
    """Test Desktop Pet Window"""
    
    def test_window_creation(self, qapp, tmp_path):
        """Test that pet window can be created"""
        config_path = tmp_path / "config.json"
        config_manager = ConfigManager(str(config_path))
        
        window = PetWindow("ENFP", config_manager)
        assert window is not None
        assert window.mbti_type == "ENFP"
    
    def test_window_personality(self, qapp, tmp_path):
        """Test that window has correct personality"""
        config_path = tmp_path / "config.json"
        config_manager = ConfigManager(str(config_path))
        
        window = PetWindow("INTJ", config_manager)
        assert window.personality.type.value == "INTJ"
        assert window.personality.traits.default_emoji == "🎯"
    
    def test_window_all_mbti_types(self, qapp, tmp_path):
        """Test that window can be created with all MBTI types"""
        config_path = tmp_path / "config.json"
        config_manager = ConfigManager(str(config_path))
        
        mbti_types = [
            "INTJ", "INTP", "ENTJ", "ENTP",
            "INFJ", "INFP", "ENFJ", "ENFP",
            "ISTJ", "ISFJ", "ESTJ", "ESFJ",
            "ISTP", "ISFP", "ESTP", "ESFP"
        ]
        
        for mbti_type in mbti_types:
            window = PetWindow(mbti_type, config_manager)
            assert window.mbti_type == mbti_type
            assert window.personality is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
