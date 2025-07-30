import asyncio
import websockets
import json
import finnhub
import numpy as np
import pandas as pd
from ta.trend import MACD
import logging
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from btc_tracker.config import Config
from btc_tracker.notification import send_alert

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('btc_tracker.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('btc_tracker')

# Global variables for state management
last_macd = None
last_signal = None
last_histogram = None
closing_prices = []
WINDOW_SIZE = 26  # Number of periods to keep for MACD calculation

def calculate_macd(close_prices):
    """Calculate MACD indicators"""
    if len(close_prices) < WINDOW_SIZE:
        logger.warning(f"Not enough data points for MACD calculation ({len(close_prices)}/{WINDOW_SIZE})")
        return None, None, None
    
    # Convert to pandas Series which has ewm method
    close_series = pd.Series(close_prices)
    macd_indicator = MACD(close_series, window_slow=26, window_fast=12, window_sign=9)
    
    # Check if we have valid MACD values
    if not macd_indicator.macd().any() or not macd_indicator.macd_signal().any():
        logger.error("MACD calculation failed - no valid values returned")
        return None, None, None
    macd_line = macd_indicator.macd()
    signal_line = macd_indicator.macd_signal()
    histogram = macd_indicator.macd_diff()
    
    # Return the last values using iloc for positional indexing
    return macd_line.iloc[-1], signal_line.iloc[-1], histogram.iloc[-1]

def check_signals(current_price):
    """Check for trading signals and send alerts"""
    global last_macd, last_signal, last_histogram, closing_prices
    
    if len(closing_prices) < WINDOW_SIZE:
        logger.info(f"Collecting data: {len(closing_prices)}/{WINDOW_SIZE}")
        return
    
    # Calculate MACD values
    macd, signal, histogram = calculate_macd(closing_prices)
    if macd is None:
        return
    
    logger.info(f"MACD: {macd:.6f}, Signal: {signal:.6f}, Histogram: {histogram:.6f}")
    
    # Check for Golden Cross (MACD crosses above Signal)
    if last_macd is not None and last_signal is not None:
        if macd > signal and last_macd <= last_signal:
            logger.info("Golden Cross detected!")
            send_alert("Golden Cross Buy Signal", current_price, macd, signal, histogram)
    
    # Check for Zero Line Crossover (Histogram crosses zero)
    if last_histogram is not None:
        # Bullish crossover (negative to positive)
        if histogram > 0 and last_histogram <= 0:
            logger.info("Zero Line Bullish Crossover detected!")
            send_alert("Zero Line Bullish Crossover", current_price, macd, signal, histogram)
        # Bearish crossover (positive to negative)
        elif histogram < 0 and last_histogram >= 0:
            logger.info("Zero Line Bearish Crossover detected!")
            send_alert("Zero Line Bearish Crossover", current_price, macd, signal, histogram)
    
    # Update global state
    last_macd = macd
    last_signal = signal
    last_histogram = histogram

async def handle_websocket():
    """Handle WebSocket connection and process messages"""
    global closing_prices
    
    Config.validate()
    api_key = Config.FINNHUB_API_KEY
    
    # Connect to Finnhub WebSocket
    uri = f"wss://ws.finnhub.io?token={api_key}"
    logger.info("Connecting to Finnhub WebSocket...")
    
    async with websockets.connect(uri) as websocket:
        # Subscribe to BTC/USDT trades
        subscribe_message = {
            "type": "subscribe",
            "symbol": "BINANCE:BTCUSDT"
        }
        await websocket.send(json.dumps(subscribe_message))
        logger.info("Subscribed to BTC/USDT trades")
        
        # Process messages
        while True:
            message = await websocket.recv()
            data = json.loads(message)
            
            if data.get('type') == 'trade':
                trades = data['data']
                for trade in trades:
                    # Process each trade
                    price = trade['p']
                    timestamp = trade['t']
                    
                    # Add closing price (each trade is a potential closing price)
                    closing_prices.append(price)
                    
                    # Keep only the most recent WINDOW_SIZE * 2 prices
                    if len(closing_prices) > WINDOW_SIZE * 2:
                        closing_prices.pop(0)
                    
                    # Check for signals
                    check_signals(price)
            elif data.get('type') == 'ping':
                # Respond to keep-alive ping
                await websocket.send(json.dumps({'type': 'pong'}))
            elif data.get('type') == 'error':
                logger.error(f"WebSocket error: {data['msg']}")

from flask import Flask, render_template
import threading

app = Flask(__name__)

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

def run_flask():
    app.run(port=5000, host='0.0.0.0')

def main():
    """Main application entry point"""
    logger.info("Starting BTC/USDT Tracker with WebSocket")
    
    # Start Flask in a separate thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    # Start WebSocket event loop
    asyncio.get_event_loop().run_until_complete(handle_websocket())

if __name__ == "__main__":
    main()
