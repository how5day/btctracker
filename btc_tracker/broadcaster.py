import asyncio
import json
import logging
from btc_tracker.btc_tracker import closing_prices, last_macd, last_signal, last_histogram

logger = logging.getLogger('broadcaster')

def get_current_state():
    """Get current trading state"""
    return {
        'price': closing_prices[-1] if closing_prices else 0,
        'macd': last_macd,
        'signal': last_signal,
        'histogram': last_histogram
    }

async def broadcast_state(active_connections):
    """Broadcast current state to all active connections"""
    while True:
        try:
            state = get_current_state()
            message = json.dumps({
                'type': 'state_update',
                'data': state
            })
            
            for connection in active_connections:
                try:
                    await connection.send_text(message)
                except Exception as e:
                    logger.error(f"Error sending to connection: {e}")
                    active_connections.remove(connection)
                    
            await asyncio.sleep(1)  # Update every second
            
        except Exception as e:
            logger.error(f"Broadcast error: {e}")
            await asyncio.sleep(5)
