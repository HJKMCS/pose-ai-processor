"""
All hardcoded values in one place.
Easy to modify, easy to find.
"""

# ============ PATHS ============
OUTPUT_DIR = "outputs"
CONFIG_DIR = "configs"
LOG_DIR = "logs"

# ============ LM STUDIO ============
LM_STUDIO_BASE_URL = "http://localhost:1234/v1"
DEFAULT_MODEL = "local-model"

# ============ LM SETTINGS (User can modify these) ============
DEFAULT_TEMPERATURE = 0.7
DEFAULT_TOP_K = 40
DEFAULT_TOP_P = 0.9
DEFAULT_MAX_TOKENS = 512
DEFAULT_PENALTY_DELAY = 1.0  # High penalty for delay

# ============ VIDEO ============
SUPPORTED_VIDEO_FORMATS = [".mp4", ".avi", ".mov", ".mkv", ".webm"]
DEFAULT_FPS = 30.0

# ============ POSE DETECTION ============
POSE_DETECTION_CONFIDENCE = 0.5
POSE_TRACKING_SMOOTHING = 0.5

# ============ UI ============
APP_TITLE = "Local AI Pose Processor"
APP_WIDTH = 900
APP_HEIGHT = 700
THEME = "dark"  # "dark", "light", "system"

# ============ SYSTEM PROMPT ============
DEFAULT_SYSTEM_PROMPT = """You are a posture analysis expert. 
Analyze the pose data and provide:
1. Posture quality assessment
2. Specific improvements
3. Health implications
Be concise and actionable."""

# ============ FILE NAMING ============
FILENAME_TIMESTAMP_FORMAT = "%Y%m%d_%H%M%S"