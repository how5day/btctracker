import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'btc_tracker', '.env'))

class Config:
    FINNHUB_API_KEY = os.getenv('FINNHUB_API_KEY')
    
    @classmethod
    def log_config(cls):
        return f"FINNHUB_API_KEY: {cls.FINNHUB_API_KEY}"
    
    @classmethod
    def validate(cls):
        if not cls.FINNHUB_API_KEY:
            raise EnvironmentError("Missing required environment variable: FINNHUB_API_KEY")
