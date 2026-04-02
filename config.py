"""
Configuration for Lightweight AgenticCyber Framework
"""
import os
from pathlib import Path

# API Configuration
API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyAPVSneOGMZv7Lqfg1YKAEZmvDlJggzRM8")

# Model Configuration
# Available models (with models/ prefix):
# - models/gemini-2.5-flash (recommended, fast)
# - models/gemini-2.5-pro (more capable)
# - models/gemini-2.0-flash (alternative)
# - models/gemini-2.5-flash-lite (lightweight)
DEFAULT_MODEL = "models/gemini-2.5-flash"
VISION_MODEL = "models/gemini-2.5-flash"  # Vision models use same API
LITE_MODEL = "models/gemini-2.5-flash-lite"

# Path Configuration
BASE_DIR = Path(__file__).parent
INPUT_DIR = BASE_DIR / "input"
INPUT_LOGS_DIR = INPUT_DIR / "logs"
INPUT_VIDEOS_DIR = INPUT_DIR / "videos"
INPUT_NETWORK_DIR = INPUT_DIR / "network"
OUTPUT_DIR = BASE_DIR / "output"

# Legacy paths (for backward compatibility)
VIDEO_DIR = BASE_DIR
LOG_DIR = BASE_DIR / "archive"

# Create directories if they don't exist
OUTPUT_DIR.mkdir(exist_ok=True)
INPUT_DIR.mkdir(exist_ok=True)
INPUT_LOGS_DIR.mkdir(exist_ok=True)
INPUT_VIDEOS_DIR.mkdir(exist_ok=True)
INPUT_NETWORK_DIR.mkdir(exist_ok=True)

# Agent Configuration
AGENT_TIMEOUT = 30  # seconds
MAX_RETRIES = 3