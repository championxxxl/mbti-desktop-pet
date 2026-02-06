"""
Tests for MBTI Desktop Pet Configuration Management
"""

import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

import pytest
import json
import tempfile

from mbti_pet.config import ConfigManager


class TestConfigManager:
    """Test ConfigManager functionality"""
    
    def test_config_manager_creation(self, tmp_path):
        """Test that ConfigManager can be created with custom path"""
        config_path = tmp_path / "test_config.json"
        manager = ConfigManager(str(config_path))
        assert manager.config_path == config_path
    
    def test_config_manager_creates_directory(self, tmp_path):
        """Test that ConfigManager creates parent directory"""
        config_path = tmp_path / "subdir" / "config.json"
        manager = ConfigManager(str(config_path))
        assert config_path.parent.exists()
    
    def test_load_empty_config(self, tmp_path):
        """Test loading when config file doesn't exist"""
        config_path = tmp_path / "config.json"
        manager = ConfigManager(str(config_path))
        config = manager.load()
        assert config == {}
    
    def test_save_and_load_config(self, tmp_path):
        """Test saving and loading configuration"""
        config_path = tmp_path / "config.json"
        manager = ConfigManager(str(config_path))
        
        test_config = {
            "mbti_type": "INTJ",
            "window_position": [100, 200]
        }
        
        assert manager.save(test_config) == True
        loaded_config = manager.load()
        assert loaded_config == test_config
    
    def test_mbti_type_management(self, tmp_path):
        """Test MBTI type saving and loading"""
        config_path = tmp_path / "config.json"
        manager = ConfigManager(str(config_path))
        
        # Initially no MBTI type
        assert manager.get_mbti_type() is None
        
        # Set MBTI type
        assert manager.set_mbti_type("ENFP") == True
        assert manager.get_mbti_type() == "ENFP"
        
        # Update MBTI type
        assert manager.set_mbti_type("INTJ") == True
        assert manager.get_mbti_type() == "INTJ"
    
    def test_window_position_management(self, tmp_path):
        """Test window position saving and loading"""
        config_path = tmp_path / "config.json"
        manager = ConfigManager(str(config_path))
        
        # Initially no position
        assert manager.get_window_position() is None
        
        # Set position
        assert manager.set_window_position(150, 250) == True
        position = manager.get_window_position()
        assert position == (150, 250)
        
        # Update position
        assert manager.set_window_position(300, 400) == True
        position = manager.get_window_position()
        assert position == (300, 400)
    
    def test_window_size_management(self, tmp_path):
        """Test window size saving and loading"""
        config_path = tmp_path / "config.json"
        manager = ConfigManager(str(config_path))
        
        # Initially no size
        assert manager.get_window_size() is None
        
        # Set size
        assert manager.set_window_size(800, 600) == True
        size = manager.get_window_size()
        assert size == (800, 600)
    
    def test_corrupted_config_file(self, tmp_path):
        """Test handling of corrupted config file"""
        config_path = tmp_path / "config.json"
        
        # Write invalid JSON
        with open(config_path, 'w') as f:
            f.write("This is not valid JSON {{{")
        
        manager = ConfigManager(str(config_path))
        config = manager.load()
        assert config == {}  # Should return empty dict on error
    
    def test_config_persistence(self, tmp_path):
        """Test that configuration persists across manager instances"""
        config_path = tmp_path / "config.json"
        
        # First manager instance
        manager1 = ConfigManager(str(config_path))
        manager1.set_mbti_type("ENTP")
        manager1.set_window_position(100, 200)
        
        # Second manager instance (simulating restart)
        manager2 = ConfigManager(str(config_path))
        assert manager2.get_mbti_type() == "ENTP"
        assert manager2.get_window_position() == (100, 200)
    
    def test_all_16_mbti_types(self, tmp_path):
        """Test saving and loading all 16 MBTI types"""
        config_path = tmp_path / "config.json"
        manager = ConfigManager(str(config_path))
        
        mbti_types = [
            "INTJ", "INTP", "ENTJ", "ENTP",
            "INFJ", "INFP", "ENFJ", "ENFP",
            "ISTJ", "ISFJ", "ESTJ", "ESFJ",
            "ISTP", "ISFP", "ESTP", "ESFP"
        ]
        
        for mbti_type in mbti_types:
            manager.set_mbti_type(mbti_type)
            assert manager.get_mbti_type() == mbti_type


class TestPetConfig:
    """Test PetConfig dataclass functionality"""
    
    def test_pet_config_from_env(self):
        """Test creating PetConfig from environment"""
        from mbti_pet.config import PetConfig
        config = PetConfig.from_env()
        
        assert config.default_mbti_type == "ENFP"
        assert config.pet_name == "PetBot"
        assert config.window_always_on_top == True
    
    def test_pet_config_to_dict(self):
        """Test converting PetConfig to dictionary"""
        from mbti_pet.config import PetConfig
        config = PetConfig.from_env()
        config_dict = config.to_dict()
        
        assert isinstance(config_dict, dict)
        assert "default_mbti_type" in config_dict
        assert "pet_name" in config_dict
        
        # API keys should be masked
        if config.openai_api_key:
            assert config_dict["openai_api_key"] == "***"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
