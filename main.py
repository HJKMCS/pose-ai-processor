"""
Main Entry Point.
Run this file to start the application.
"""

import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

# Import main UI
from ui_main import PoseAIApp
from logger import logger
import constants as C

def main():
    """Main entry point."""
    logger.info("="*60)
    logger.info(f"Starting {C.APP_TITLE}")
    logger.info("="*60)
    
    # Create output directories
    Path(C.OUTPUT_DIR).mkdir(exist_ok=True)
    Path(C.CONFIG_DIR).mkdir(exist_ok=True)
    Path(C.LOG_DIR).mkdir(exist_ok=True)
    
    # Start application
    app = PoseAIApp()
    app.mainloop()
    
    logger.info("Application closed")

if __name__ == "__main__":
    main()