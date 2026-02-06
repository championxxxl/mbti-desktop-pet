"""
Configuration management for MBTI Desktop Pet
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass
from dotenv import load_dotenv


@dataclass
class PetConfig:
    """Configuration for the desktop pet"""
    # API Keys
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    
    # Pet settings
    default_mbti_type: str = "ENFP"
    pet_name: str = "PetBot"
    
    # Memory settings
    memory_db_path: str = "./data/memory.db"
    max_memory_size: int = 1000
    
    # Monitoring settings
    screen_monitor_enabled: bool = True
    screen_monitor_interval: int = 30
    text_monitor_enabled: bool = True
    
    # Automation settings
    automation_enabled: bool = True
    auto_suggest_enabled: bool = True
    
    # UI settings
    window_always_on_top: bool = True
    start_minimized: bool = False
    
    @classmethod
    def from_env(cls) -> 'PetConfig':
        """Load configuration from environment variables"""
        load_dotenv()
        
        return cls(
            openai_api_key=os.getenv("OPENAI_API_KEY", ""),
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY", ""),
            default_mbti_type=os.getenv("DEFAULT_MBTI_TYPE", "ENFP"),
            pet_name=os.getenv("PET_NAME", "PetBot"),
            memory_db_path=os.getenv("MEMORY_DB_PATH", "./data/memory.db"),
            max_memory_size=int(os.getenv("MAX_MEMORY_SIZE", "1000")),
            screen_monitor_enabled=os.getenv("SCREEN_MONITOR_ENABLED", "true").lower() == "true",
            screen_monitor_interval=int(os.getenv("SCREEN_MONITOR_INTERVAL", "30")),
            text_monitor_enabled=os.getenv("TEXT_MONITOR_ENABLED", "true").lower() == "true",
            automation_enabled=os.getenv("AUTOMATION_ENABLED", "true").lower() == "true",
            auto_suggest_enabled=os.getenv("AUTO_SUGGEST_ENABLED", "true").lower() == "true",
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary"""
        return {
            "openai_api_key": "***" if self.openai_api_key else "",
            "anthropic_api_key": "***" if self.anthropic_api_key else "",
            "default_mbti_type": self.default_mbti_type,
            "pet_name": self.pet_name,
            "memory_db_path": self.memory_db_path,
            "max_memory_size": self.max_memory_size,
            "screen_monitor_enabled": self.screen_monitor_enabled,
            "screen_monitor_interval": self.screen_monitor_interval,
            "text_monitor_enabled": self.text_monitor_enabled,
            "automation_enabled": self.automation_enabled,
            "auto_suggest_enabled": self.auto_suggest_enabled,
        }


class ConfigManager:
    """Manager for persistent configuration using JSON files"""
    
    DEFAULT_CONFIG_PATH = "./data/config.json"
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration manager
        
        Args:
            config_path: Path to configuration file (default: ./data/config.json)
        """
        self.config_path = Path(config_path or self.DEFAULT_CONFIG_PATH)
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
    
    def load(self) -> Dict[str, Any]:
        """
        Load configuration from JSON file
        
        Returns:
            Dictionary containing configuration data, or empty dict if file doesn't exist
        """
        if not self.config_path.exists():
            return {}
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not load config from {self.config_path}: {e}")
            return {}
    
    def save(self, config: Dict[str, Any]) -> bool:
        """
        Save configuration to JSON file
        
        Args:
            config: Configuration dictionary to save
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            return True
        except IOError as e:
            print(f"Error: Could not save config to {self.config_path}: {e}")
            return False
    
    def get_mbti_type(self) -> Optional[str]:
        """
        Get saved MBTI type from configuration
        
        Returns:
            MBTI type string or None if not set
        """
        config = self.load()
        return config.get("mbti_type")
    
    def set_mbti_type(self, mbti_type: str) -> bool:
        """
        Save MBTI type to configuration
        
        Args:
            mbti_type: MBTI type string (e.g., "ENFP", "INTJ")
            
        Returns:
            True if successful, False otherwise
        """
        config = self.load()
        config["mbti_type"] = mbti_type
        return self.save(config)
    
    def get_window_position(self) -> Optional[Tuple[int, int]]:
        """
        Get saved window position
        
        Returns:
            Tuple of (x, y) coordinates or None if not set
        """
        config = self.load()
        pos = config.get("window_position")
        if pos and isinstance(pos, list) and len(pos) == 2:
            return tuple(pos)
        return None
    
    def set_window_position(self, x: int, y: int) -> bool:
        """
        Save window position to configuration
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            True if successful, False otherwise
        """
        config = self.load()
        config["window_position"] = [x, y]
        return self.save(config)
    
    def get_window_size(self) -> Optional[Tuple[int, int]]:
        """
        Get saved window size
        
        Returns:
            Tuple of (width, height) or None if not set
        """
        config = self.load()
        size = config.get("window_size")
        if size and isinstance(size, list) and len(size) == 2:
            return tuple(size)
        return None
    
    def set_window_size(self, width: int, height: int) -> bool:
        """
        Save window size to configuration
        
        Args:
            width: Window width
            height: Window height
            
        Returns:
            True if successful, False otherwise
        """
        config = self.load()
        config["window_size"] = [width, height]
        return self.save(config)


# Global configuration instance
config = PetConfig.from_env()
