import ccxt
import logging
from config import CMC_TOKEN
import requests


logging.basicConfig(level=logging.INFO)

# Инициализация клиента Binance
exchange = ccxt.binance()

async def fetch_data(symbol: str, timeframe: str = '1m', limit: int = 20):
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


async def get_volume_24h(symbol):
    ticker = exchange.fetch_ticker(symbol)
    volume_24h = ticker['quoteVolume']

    return volume_24h


async def get_cmc_info(symbol: str) -> dict:
    """
    Получает ранг и капитализацию указанной криптовалюты.

    :param symbol: Символ криптовалюты (например, 'TWT')
    :param api_key: API-ключ CoinMarketCap
    :return: Словарь с рангом и капитализацией
    """
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    headers = {"X-CMC_PRO_API_KEY": CMC_TOKEN}
    params = {"symbol": symbol}

    try:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        crypto_data = data["data"][symbol]
        rank = crypto_data["cmc_rank"]
        market_cap = crypto_data["quote"]["USD"]["market_cap"]

        return {"rank": rank, "market_cap": market_cap}

    except Exception as e:
        print(f"Ошибка при получении данных: {e}")
        return {"rank": None, "market_cap": None}