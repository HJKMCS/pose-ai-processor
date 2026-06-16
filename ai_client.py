"""
AI Client for LM Studio.
Communicates with local model using custom settings.
Supports:
- Posture analysis
- Custom system prompts
- Configurable temperature, top_k, top_p
- High penalty for delay
"""

import requests
import json
from typing import Dict, Any, Optional, Callable
from logger import logger
import constants as C
from config_manager import config

class AIClient:
    """
    Local AI client for LM Studio.
    Uses configuration from config_manager.
    """
    
    def __init__(self):
        self.base_url = C.LM_STUDIO_BASE_URL
        self.is_connected = False
        self.current_model = C.DEFAULT_MODEL
        
        logger.info("AIClient initialized")
    
    def check_connection(self) -> bool:
        """Check if LM Studio is running and accessible."""
        try:
            response = requests.get(f"{self.base_url}/models", timeout=3)
            if response.status_code == 200:
                self.is_connected = True
                logger.info("Connected to LM Studio")
                return True
            else:
                logger.warning(f"LM Studio returned status {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            logger.error(f"Cannot connect to LM Studio: {e}")
            self.is_connected = False
            return False
    
    def analyze_posture(
        self,
        pose_data: Dict[str, Any],
        custom_prompt: Optional[str] = None,
        progress_callback: Optional[Callable[[str], None]] = None
    ) -> Dict[str, Any]:
        """
        Send pose data to AI for analysis.
        
        Args:
            pose_data: Dictionary containing pose landmarks and summary
            custom_prompt: Optional custom prompt (uses system prompt if None)
            progress_callback: Optional callback for status updates
            
        Returns:
            Dictionary with AI analysis results
        """
        result = {
            "success": False,
            "analysis": None,
            "error": None,
            "model_used": None,
            "tokens_used": None
        }
        
        # Check connection
        if not self.check_connection():
            result["error"] = "Cannot connect to LM Studio. Make sure it's running on localhost:1234"
            logger.error(result["error"])
            return result
        
        try:
            if progress_callback:
                progress_callback("Preparing pose data for AI...")
            
            # Get current LM settings
            lm_settings = config.get_lm_settings()
            system_prompt = config.get_system_prompt()
            
            # Build the prompt
            if custom_prompt:
                user_prompt = custom_prompt
            else:
                user_prompt = self._build_posture_prompt(pose_data)
            
            if progress_callback:
                progress_callback(f"Sending to AI model: {lm_settings.get('model')}...")
            
            # Prepare API request
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
            
            # Build request payload with ALL custom settings
            payload = {
                "model": lm_settings.get("model", C.DEFAULT_MODEL),
                "messages": messages,
                "temperature": lm_settings.get("temperature", C.DEFAULT_TEMPERATURE),
                "top_k": lm_settings.get("top_k", C.DEFAULT_TOP_K),
                "top_p": lm_settings.get("top_p", C.DEFAULT_TOP_P),
                "max_tokens": lm_settings.get("max_tokens", C.DEFAULT_MAX_TOKENS),
                "stream": False
            }
            
            # Add penalty settings if applicable
            if "penalty_delay" in lm_settings:
                payload["frequency_penalty"] = lm_settings["penalty_delay"]
            
            logger.debug(f"Sending request to LM Studio with settings: {json.dumps(lm_settings, indent=2)}")
            
            # Send request
            if progress_callback:
                progress_callback("AI is analyzing posture...")
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                json=payload,
                timeout=60  # 60 second timeout for complex analysis
            )
            
            response.raise_for_status()
            
            # Parse response
            response_data = response.json()
            analysis = response_data["choices"][0]["message"]["content"]
            
            result["success"] = True
            result["analysis"] = analysis
            result["model_used"] = lm_settings.get("model")
            result["tokens_used"] = response_data.get("usage", {})
            
            logger.info(f"AI analysis successful. Model: {result['model_used']}")
            
            if progress_callback:
                progress_callback("Analysis complete!")
            
            return result
            
        except requests.exceptions.Timeout:
            error_msg = "AI request timed out. The model might be too slow or busy."
            logger.error(error_msg)
            result["error"] = error_msg
            return result
            
        except requests.exceptions.RequestException as e:
            error_msg = f"AI request failed: {str(e)}"
            logger.error(error_msg)
            result["error"] = error_msg
            return result
            
        except Exception as e:
            error_msg = f"Unexpected error in AI analysis: {str(e)}"
            logger.error(error_msg)
            result["error"] = error_msg
            return result
    
    def _build_posture_prompt(self, pose_data: Dict[str, Any]) -> str:
        """Build a detailed prompt from pose data."""
        prompt_parts = [
            "Analyze this posture data from a video:",
            "",
            f"Total frames analyzed: {pose_data.get('total_frames', 'N/A')}",
            f"Frames with detected pose: {pose_data.get('pose_frames', 'N/A')}",
            f"Video resolution: {pose_data.get('resolution', 'N/A')}",
            f"FPS: {pose_data.get('fps', 'N/A')}",
            ""
        ]
        
        # Add sample frame data (first 5 frames with pose)
        frame_data = pose_data.get('frame_data', [])
        samples = [f for f in frame_data if f.get('has_pose')][:5]
        
        if samples:
            prompt_parts.append("Sample frame data (first 5 frames with pose):")
            for i, frame in enumerate(samples, 1):
                if 'summary' in frame:
                    summary = frame['summary']
                    prompt_parts.append(f"Frame {i}:")
                    prompt_parts.append(f"  - Shoulder angle: {summary.get('shoulder_angle', 'N/A'):.2f}°")
                    prompt_parts.append(f"  - Hip angle: {summary.get('hip_angle', 'N/A'):.2f}°")
                    if 'head_position' in summary:
                        head = summary['head_position']
                        prompt_parts.append(f"  - Head position: x={head.get('x', 0):.3f}, y={head.get('y', 0):.3f}")
            prompt_parts.append("")
        
        prompt_parts.append("Provide:")
        prompt_parts.append("1. Overall posture quality assessment")
        prompt_parts.append("2. Specific issues detected (slouching, head forward, etc.)")
        prompt_parts.append("3. Recommendations for improvement")
        prompt_parts.append("4. Health implications if posture is maintained")
        prompt_parts.append("5. Exercises or stretches to correct issues")
        prompt_parts.append("")
        prompt_parts.append("Be concise, specific, and actionable.")
        
        return "\n".join(prompt_parts)
    
    def quick_query(
        self,
        prompt: str,
        use_system_prompt: bool = True
    ) -> Dict[str, Any]:
        """
        Send a quick query to the AI (for chat feature).
        Simpler than analyze_posture.
        """
        result = {
            "success": False,
            "response": None,
            "error": None
        }
        
        if not self.check_connection():
            result["error"] = "LM Studio not connected"
            return result
        
        try:
            lm_settings = config.get_lm_settings()
            
            messages = [{"role": "user", "content": prompt}]
            
            if use_system_prompt:
                system_prompt = config.get_system_prompt()
                messages.insert(0, {"role": "system", "content": system_prompt})
            
            payload = {
                "model": lm_settings.get("model", C.DEFAULT_MODEL),
                "messages": messages,
                "temperature": lm_settings.get("temperature", C.DEFAULT_TEMPERATURE),
                "max_tokens": lm_settings.get("max_tokens", C.DEFAULT_MAX_TOKENS)
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                json=payload,
                timeout=30
            )
            
            response.raise_for_status()
            
            result["success"] = True
            result["response"] = response.json()["choices"][0]["message"]["content"]
            
            return result
            
        except Exception as e:
            result["error"] = str(e)
            logger.error(f"Quick query failed: {e}")
            return result