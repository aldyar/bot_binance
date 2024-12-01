import ccxt
import logging

logging.basicConfig(level=logging.INFO)

# Инициализация клиента Binance
exchange = ccxt.binance()

async def fetch_data(symbol: str, timeframe: str = '4h', limit: int = 7):
    """
    Получает данные свечей (OHLCV) для указанного символа.
    """
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        return ohlcv
    except Exception as e:
        logging.error(f"Ошибка при получении данных для {symbol}: {e}")
        return []

def check_red_candles(ohlcv):
    """
    Проверяет, являются ли последние шесть свечей красными (close < open).
    """
    if len(ohlcv) < 7:
        return False  # Недостаточно данных для проверки
    for candle in ohlcv[-7:-1]:
        open_price, close_price = candle[1], candle[4]
        if close_price >= open_price:
            return False
    return True



