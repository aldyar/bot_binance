import ccxt
import logging

logging.basicConfig(level=logging.INFO)

# Инициализация клиента Binance
exchange = ccxt.binance()

async def fetch_data(symbol: str, timeframe: str = '1h', limit: int = 20):
    """
    Получает данные свечей (OHLCV) для указанного символа.
    """
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        return ohlcv
    except Exception as e:
        logging.error(f"Ошибка при получении данных для {symbol}: {e}")
        return []


def check_candle_pattern(ohlcv):
    """
    Проверяет, является ли 18-я свеча зелёной.
    Если да, то ищет подряд 6 и более красных свечей перед ней.
    Если таких свечей не меньше 6, возвращает True, иначе False.
    """

    # Проверяем, есть ли в списке хотя бы 19 свечей
    if len(ohlcv) < 19:
        print("Недостаточно свечей для проверки (требуется минимум 19).")
        return False

    # Получаем 18-ю свечу
    candle_18 = ohlcv[18]
    open_price_18 = candle_18[1]
    close_price_18 = candle_18[4]

    # Проверяем, что 18-я свеча зелёная (закрытие > открытие)
    if close_price_18 <= open_price_18:
        return False

    # Теперь начинаем проверку предыдущих свечей (с 17-й по 1-ю)
    red_count = 0
    for i in range(17, -1, -1):  # Идём от 17-й до 0-й свечи
        candle = ohlcv[i]
        open_price = candle[1]
        close_price = candle[4]

        # Если свеча красная (закрытие < открытие)
        if close_price < open_price:
            red_count += 1
        else:
            # Если встречаем зелёную свечу (закрытие > открытие) - пропускаем её
            if red_count >= 6:
                print(f"Найдено {red_count} красных свечей подряд.")
                return red_count
            else:
                return False

    # Если не нашли зелёной свечи после красных, значит красных было больше 6
    if red_count >= 6:
        print(f"Найдено {red_count} красных свечей подряд.")
        return red_count
    else:
        return False
