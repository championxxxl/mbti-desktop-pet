"""
Configuration management for MBTI Desktop Pet
"""

import os
from typing import Dict, Any
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


# Global configuration instance
config = PetConfig.from_env()
