"""
Configuration module for WhatsApp Bot
=====================================
Centralizes all configuration settings and provides validation.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class with all bot settings."""
    
    # ===== WEB SCRAPING SETTINGS =====
    TARGET_URL = os.environ.get("TARGET_URL", "https://example.com")
    CHROME_DRIVER_PATH = os.environ.get("CHROME_DRIVER_PATH", "chromedriver.exe")
    SCRAPING_TIMEOUT = int(os.environ.get("SCRAPING_TIMEOUT", "30"))
    
    # ===== TWILIO API SETTINGS =====
    TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
    TWILIO_WHATSAPP_NUMBER = os.environ.get("TWILIO_WHATSAPP_NUMBER", "whatsapp:+14155238886")
    
    # ===== PERSONAL SETTINGS =====
    MY_PHONE_NUMBER = os.environ.get("MY_PHONE_NUMBER")
    
    # ===== MESSAGE SETTINGS =====
    MAX_ITEMS_PER_MESSAGE = int(os.environ.get("MAX_ITEMS_PER_MESSAGE", "20"))
    
    # ===== SELENIUM SETTINGS =====
    HEADLESS_MODE = os.environ.get("HEADLESS_MODE", "True").lower() == "true"
    WINDOW_SIZE = os.environ.get("WINDOW_SIZE", "1920,1080")
    USER_AGENT = os.environ.get("USER_AGENT", 
                               "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    @classmethod
    def validate_required_settings(cls):
        """
        Validate that all required settings are present.
        
        Returns:
            tuple: (is_valid, missing_settings)
        """
        required_settings = {
            "TWILIO_ACCOUNT_SID": cls.TWILIO_ACCOUNT_SID,
            "TWILIO_AUTH_TOKEN": cls.TWILIO_AUTH_TOKEN,
            "MY_PHONE_NUMBER": cls.MY_PHONE_NUMBER,
            "TARGET_URL": cls.TARGET_URL
        }
        
        missing = [setting for setting, value in required_settings.items() if not value]
        
        return len(missing) == 0, missing
    
    @classmethod
    def get_chrome_options(cls):
        """
        Get Chrome options for Selenium WebDriver.
        
        Returns:
            list: Chrome options as command line arguments
        """
        options = [
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-gpu",
            f"--window-size={cls.WINDOW_SIZE}",
            "--disable-blink-features=AutomationControlled",
            f"--user-agent={cls.USER_AGENT}"
        ]
        
        if cls.HEADLESS_MODE:
            options.append("--headless")
        
        return options
    
    @classmethod
    def print_configuration(cls):
        """Print current configuration (hiding sensitive data)."""
        print("🔧 Current Configuration:")
        print(f"   Target URL: {cls.TARGET_URL}")
        print(f"   Chrome Driver: {cls.CHROME_DRIVER_PATH}")
        print(f"   Headless Mode: {cls.HEADLESS_MODE}")
        print(f"   Max Items: {cls.MAX_ITEMS_PER_MESSAGE}")
        print(f"   Twilio SID: {'✅ Set' if cls.TWILIO_ACCOUNT_SID else '❌ Missing'}")
        print(f"   Auth Token: {'✅ Set' if cls.TWILIO_AUTH_TOKEN else '❌ Missing'}")
        print(f"   Phone Number: {'✅ Set' if cls.MY_PHONE_NUMBER else '❌ Missing'}")

# Create a default config instance
config = Config()
