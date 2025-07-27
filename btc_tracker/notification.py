import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import Config
import logging

logger = logging.getLogger(__name__)

def send_alert(signal_type: str, current_price: float, macd_value: float, signal_value: float, histogram_value: float):
    """Send email alert for trading signal"""
    try:
        # Validate configuration
        Config.validate()
        
        # Create email content
        subject = f"BTCUSDT Trading Signal: {signal_type}"
        body = f"""
        <h3>BTCUSDT Trading Signal</h3>
        <p><strong>Signal Type:</strong> {signal_type}</p>
        <p><strong>Price:</strong> ${current_price:.2f}</p>
        <p><strong>MACD:</strong> {macd_value:.6f}</p>
        <p><strong>Signal:</strong> {signal_value:.6f}</p>
        <p><strong>Histogram:</strong> {histogram_value:.6f}</p>
        """
        
        # Setup email message
        msg = MIMEMultipart()
        msg['From'] = Config.EMAIL_USER
        msg['To'] = Config.ALERT_EMAIL
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))
        
        # Send email
        with smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT) as server:
            server.starttls()
            server.login(Config.EMAIL_USER, Config.EMAIL_PASSWORD)
            server.send_message(msg)
            
        logger.info(f"Sent {signal_type} alert email")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send alert: {str(e)}")
        return False
