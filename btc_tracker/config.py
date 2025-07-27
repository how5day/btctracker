import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'btc_tracker', '.env'))

class Config:
    FINNHUB_API_KEY = os.getenv('FINNHUB_API_KEY')
    SMTP_SERVER = os.getenv('SMTP_SERVER')
    SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
    EMAIL_USER = os.getenv('EMAIL_USER')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
    ALERT_EMAIL = os.getenv('ALERT_EMAIL')
    
    @classmethod
    def log_config(cls):
        return f"FINNHUB_API_KEY: {cls.FINNHUB_API_KEY}"
    
    @classmethod
    def validate(cls):
        required = [
            cls.FINNHUB_API_KEY,
            cls.SMTP_SERVER,
            cls.EMAIL_USER,
            cls.EMAIL_PASSWORD,
            cls.ALERT_EMAIL
        ]
        if not all(required):
            raise EnvironmentError("Missing required environment variables")
