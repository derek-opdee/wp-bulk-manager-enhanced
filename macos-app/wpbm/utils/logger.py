"""
Logging configuration for WP Bulk Manager
"""
import logging
import os
from typing import Optional


def get_logger(name: str, level: Optional[str] = None) -> logging.Logger:
    """
    Get a configured logger instance
    
    Args:
        name: Logger name (typically __name__)
        level: Logging level (default from environment or INFO)
    """
    logger = logging.getLogger(name)
    
    # Only configure if not already configured
    if not logger.handlers:
        # Get level from environment or parameter
        if level is None:
            level = os.environ.get('WPBM_LOG_LEVEL', 'INFO')
            
        logger.setLevel(getattr(logging, level.upper()))
        
        # Console handler with formatting
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
    return logger