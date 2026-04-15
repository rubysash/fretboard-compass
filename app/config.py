"""
Configuration settings for Fretboard Compass.
Controls DEBUG mode and logging levels.
"""
import os
from pathlib import Path

class Config:
    """Base configuration."""
    VERSION = "0.1.2"
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-for-local-use')
    DEBUG = True
    APP_DIR = Path(__file__).parent
    ROOT_DIR = APP_DIR.parent
    
    # Logging
    LOG_LEVEL = 'DEBUG' if DEBUG else 'INFO'
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    LOG_LEVEL = 'INFO'
