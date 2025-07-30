import logging

logger = logging.getLogger(__name__)

def send_alert(signal_type: str, current_price: float, macd_value: float, signal_value: float, histogram_value: float):
    """Display in-app notification for trading signal"""
    message = (
        f"\n=== BTC/USDT TRADING SIGNAL DETECTED ===\n"
        f"Signal: {signal_type}\n"
        f"Price: ${current_price:.2f}\n"
        f"MACD: {macd_value:.6f}\n"
        f"Signal Line: {signal_value:.6f}\n"
        f"Histogram: {histogram_value:.6f}\n"
        f"========================================"
    )
    print(message)
    logger.info(message)
