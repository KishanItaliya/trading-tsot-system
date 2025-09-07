"""
Logging configuration
"""

import logging
import os
from datetime import datetime
from ..config.settings import config


def setup_logging(log_level: str = None) -> logging.Logger:
    """
    Setup logging configuration
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        
    Returns:
        Configured logger
    """
    if log_level is None:
        log_level = config.log_level
    
    # Create logs directory if it doesn't exist
    os.makedirs(config.trading.logs_dir, exist_ok=True)
    
    # Create log filename with timestamp
    log_filename = os.path.join(
        config.trading.logs_dir, 
        f"trading_system_{datetime.now().strftime('%Y%m%d')}.log"
    )
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format=config.log_format,
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler()  # Also log to console
        ]
    )
    
    # Create logger
    logger = logging.getLogger('trading_system')
    logger.info(f"Logging initialized - Level: {log_level}")
    
    return logger
