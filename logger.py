"""
Safe, file-based logging.
No terminal needed.
Isolated in one file.
"""

import logging
import os
from datetime import datetime
from pathlib import Path

class AppLogger:
    """Centralized logging system."""
    
    _instance = None
    _logger = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AppLogger, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._logger is not None:
            return
            
        # Create logs directory
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # Create unique log file for this session
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = log_dir / f"app_{timestamp}.log"
        
        # Setup logger
        self._logger = logging.getLogger("PoseAI")
        self._logger.setLevel(logging.DEBUG)
        
        # File handler
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        
        # Console handler (optional, can be disabled)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers
        self._logger.addHandler(file_handler)
        self._logger.addHandler(console_handler)
        
        self._logger.info("="*50)
        self._logger.info(f"Application started - Log file: {log_file}")
        self._logger.info("="*50)
    
    def get_logger(self):
        """Get the logger instance."""
        return self._logger
    
    def info(self, message):
        self._logger.info(message)
    
    def debug(self, message):
        self._logger.debug(message)
    
    def warning(self, message):
        self._logger.warning(message)
    
    def error(self, message):
        self._logger.error(message)
    
    def critical(self, message):
        self._logger.critical(message)

# Global logger instance
logger = AppLogger()