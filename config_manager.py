"""
Configuration manager.
Handles:
- User settings
- LM parameters (temperature, top_k, top_p, etc.)
- System prompts
- File I/O for configs
All in JSON format.
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional
import constants as C
from logger import logger

class ConfigManager:
    """Manages all configuration and LM settings."""
    
    def __init__(self):
        self.config_dir = Path(C.CONFIG_DIR)
        self.config_dir.mkdir(exist_ok=True)
        
        # Default configuration
        self.config = {
            "lm_settings": {
                "model": C.DEFAULT_MODEL,
                "temperature": C.DEFAULT_TEMPERATURE,
                "top_k": C.DEFAULT_TOP_K,
                "top_p": C.DEFAULT_TOP_P,
                "max_tokens": C.DEFAULT_MAX_TOKENS,
                "penalty_delay": C.DEFAULT_PENALTY_DELAY,
                "base_url": C.LM_STUDIO_BASE_URL
            },
            "system_prompt": C.DEFAULT_SYSTEM_PROMPT,
            "user_behavior": {
                "last_video_dir": "",
                "last_output_dir": str(C.OUTPUT_DIR),
                "preferred_model": C.DEFAULT_MODEL,
                "auto_save": True
            },
            "pose_settings": {
                "detection_confidence": C.POSE_DETECTION_CONFIDENCE,
                "tracking_smoothing": C.POSE_TRACKING_SMOOTHING
            },
            "ui_settings": {
                "theme": C.THEME,
                "window_width": C.APP_WIDTH,
                "window_height": C.APP_HEIGHT
            }
        }
        
        self.config_file = self.config_dir / "default_config.json"
        self.load_config()
        
        logger.info("ConfigManager initialized")
    
    def load_config(self, config_path: Optional[Path] = None) -> bool:
        """Load configuration from file."""
        try:
            path = config_path or self.config_file
            if path.exists():
                with open(path, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    # Merge with defaults (don't overwrite completely)
                    self._deep_update(self.config, loaded_config)
                logger.info(f"Config loaded from {path}")
                return True
            else:
                logger.info("No config file found, using defaults")
                self.save_config()  # Create default config
                return True
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            return False
    
    def save_config(self, config_path: Optional[Path] = None) -> bool:
        """Save configuration to file."""
        try:
            path = config_path or self.config_file
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            logger.info(f"Config saved to {path}")
            return True
        except Exception as e:
            logger.error(f"Failed to save config: {e}")
            return False
    
    def update_lm_settings(self, **kwargs) -> None:
        """Update LM settings (temperature, top_k, etc.)."""
        for key, value in kwargs.items():
            if key in self.config["lm_settings"]:
                self.config["lm_settings"][key] = value
                logger.debug(f"Updated LM setting: {key} = {value}")
    
    def get_lm_settings(self) -> Dict[str, Any]:
        """Get current LM settings."""
        return self.config["lm_settings"].copy()
    
    def update_system_prompt(self, prompt: str) -> None:
        """Update system prompt."""
        self.config["system_prompt"] = prompt
        logger.info("System prompt updated")
    
    def get_system_prompt(self) -> str:
        """Get current system prompt."""
        return self.config["system_prompt"]
    
    def update_user_behavior(self, **kwargs) -> None:
        """Update user behavior tracking."""
        for key, value in kwargs.items():
            if key in self.config["user_behavior"]:
                self.config["user_behavior"][key] = value
    
    def get_output_filename(self, input_filename: str, suffix: str = "") -> str:
        """Generate unique output filename with timestamp."""
        timestamp = datetime.now().strftime(C.FILENAME_TIMESTAMP_FORMAT)
        base_name = Path(input_filename).stem
        return f"{base_name}_{timestamp}{suffix}"
    
    def _deep_update(self, base_dict: Dict, update_dict: Dict) -> None:
        """Recursively update dictionary."""
        for key, value in update_dict.items():
            if key in base_dict and isinstance(base_dict[key], dict) and isinstance(value, dict):
                self._deep_update(base_dict[key], value)
            else:
                base_dict[key] = value

# Global config instance
config = ConfigManager()