"""
JSON Handler for pose data.
Generates unique filenames to prevent collisions.
Stores:
- Frame-by-frame pose data
- Video metadata
- LM configuration used
- System prompt
All in one structured JSON file.
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional
from logger import logger
import constants as C
from config_manager import config

class JSONHandler:
    """
    Handles JSON output with unique filenames.
    Prevents collisions, stores complete session data.
    """
    
    def __init__(self):
        self.output_dir = Path(C.OUTPUT_DIR)
        self.output_dir.mkdir(exist_ok=True)
        logger.info("JSONHandler initialized")
    
    def generate_unique_filename(self, input_filename: str, suffix: str = "_pose_data") -> str:
        """
        Generate unique filename with timestamp.
        Format: originalname_YYYYMMDD_HHMMSS_suffix.json
        """
        timestamp = datetime.now().strftime(C.FILENAME_TIMESTAMP_FORMAT)
        base_name = Path(input_filename).stem
        unique_name = f"{base_name}_{timestamp}{suffix}.json"
        
        # Ensure uniqueness (in case of rapid processing)
        full_path = self.output_dir / unique_name
        counter = 1
        while full_path.exists():
            unique_name = f"{base_name}_{timestamp}{suffix}_{counter}.json"
            full_path = self.output_dir / unique_name
            counter += 1
        
        logger.debug(f"Generated unique filename: {unique_name}")
        return unique_name
    
    def save_pose_data(
        self,
        frame_data: List[Dict[str, Any]],
        input_video_path: str,
        output_video_path: str,
        video_metadata: Dict[str, Any]
    ) -> str:
        """
        Save complete pose analysis to JSON.
        
        Includes:
        - All frame data with landmarks
        - Video metadata
        - LM configuration (temperature, top_k, etc.)
        - System prompt
        - Processing timestamp
        """
        try:
            # Get current LM settings from config
            lm_settings = config.get_lm_settings()
            system_prompt = config.get_system_prompt()
            
            # Build complete JSON structure
            output_data = {
                "metadata": {
                    "created_at": datetime.now().isoformat(),
                    "input_file": str(input_video_path),
                    "output_file": str(output_video_path),
                    "video_metadata": video_metadata
                },
                "lm_configuration": {
                    "model": lm_settings.get("model", C.DEFAULT_MODEL),
                    "temperature": lm_settings.get("temperature", C.DEFAULT_TEMPERATURE),
                    "top_k": lm_settings.get("top_k", C.DEFAULT_TOP_K),
                    "top_p": lm_settings.get("top_p", C.DEFAULT_TOP_P),
                    "max_tokens": lm_settings.get("max_tokens", C.DEFAULT_MAX_TOKENS),
                    "penalty_delay": lm_settings.get("penalty_delay", C.DEFAULT_PENALTY_DELAY),
                    "base_url": lm_settings.get("base_url", C.LM_STUDIO_BASE_URL)
                },
                "system_prompt": system_prompt,
                "analysis": {
                    "total_frames": len(frame_data),
                    "frames_with_pose": sum(1 for f in frame_data if f.get("has_pose", False)),
                    "frame_data": frame_data
                }
            }
            
            # Generate unique filename
            filename = self.generate_unique_filename(input_video_path)
            filepath = self.output_dir / filename
            
            # Save to file
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Saved pose data to {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"Failed to save JSON: {e}")
            return ""
    
    def load_pose_data(self, json_path: str) -> Optional[Dict[str, Any]]:
        """Load pose data from JSON file."""
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            logger.info(f"Loaded pose data from {json_path}")
            return data
        except Exception as e:
            logger.error(f"Failed to load JSON: {e}")
            return None
    
    def update_lm_results(self, json_path: str, ai_analysis: Dict[str, Any]) -> bool:
        """
        Add AI analysis results to existing JSON.
        Allows re-processing with different model settings.
        """
        try:
            data = self.load_pose_data(json_path)
            if not data:
                return False
            
            # Add AI analysis
            if "ai_analysis" not in data:
                data["ai_analysis"] = []
            
            # Add timestamp and settings used
            analysis_entry = {
                "analyzed_at": datetime.now().isoformat(),
                "lm_settings_used": config.get_lm_settings(),
                "results": ai_analysis
            }
            
            data["ai_analysis"].append(analysis_entry)
            
            # Save back
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Updated JSON with AI analysis: {json_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update JSON: {e}")
            return False
    
    def get_json_files(self, directory: Optional[str] = None) -> List[Path]:
        """Get all JSON files in output directory."""
        search_dir = Path(directory) if directory else self.output_dir
        return list(search_dir.glob("*.json"))