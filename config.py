"""
Configuration settings for the Smart Inventory Management System (SIMS)
"""
import os
from datetime import timedelta

class Config:
    """Base configuration class"""
    
    # Basic Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'sims-secret-key-change-in-production'
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///sims.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Application settings
    APP_NAME = "Smart Inventory Management System"
    APP_VERSION = "1.0.0"
    
    # Business settings for Moroccan context
    DEFAULT_CURRENCY = "MAD"
    DEFAULT_LANGUAGE = "fr"  # French is commonly used in Moroccan business
    TIMEZONE = "Africa/Casablanca"
    
    # Inventory management settings
    DEFAULT_REORDER_LEVEL = 10
    DEFAULT_SAFETY_STOCK = 5
    DEFAULT_LEAD_TIME_DAYS = 7
    
    # Alert settings
    LOW_STOCK_THRESHOLD = 0.2  # 20% of reorder level
    CRITICAL_STOCK_THRESHOLD = 0.1  # 10% of reorder level
    
    # File upload settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv', 'xlsx'}
    
    # Session configuration
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)
    
    # Pagination
    ITEMS_PER_PAGE = 20
    
    # Analytics settings
    FORECAST_PERIODS = 30  # Days to forecast
    ABC_ANALYSIS_PERIODS = 90  # Days to analyze for ABC classification
    
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///sims_dev.db'

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///sims_prod.db'
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        
        # Log to syslog in production
        import logging
        from logging.handlers import SysLogHandler
        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(logging.WARNING)
        app.logger.addHandler(syslog_handler)

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
