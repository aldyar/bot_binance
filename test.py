"""import requests
import pprint
url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
params = {"symbol": 'TWT'}
headers = {"X-CMC_PRO_API_KEY": "48037f04-95b2-436d-899c-5e2d5e514f7e"}

response = requests.get(url, headers= headers, params=params)
data = response.json()

pprint.pprint(data['data']['TWT']['cmc_rank'])"""




"""import requests
import pprint

def get_cmc_info(symbol: str, api_key: str) -> dict:

    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    headers = {"X-CMC_PRO_API_KEY": api_key}
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

# Пример использования
api_key = "48037f04-95b2-436d-899c-5e2d5e514f7e"  # Заменить на свой ключ
symbol = "TWT"

crypto_info = get_cmc_info(symbol, api_key)
pprint.pprint(crypto_info)
"""


import ccxt
import asyncio

exchange = ccxt.binance()  # Используем Binance, можно поменять

async def fetch_data(symbol: str, timeframe: str = '4h', limit: int = 20):
    """
    Получает данные свечей (OHLCV) для указанного символа и выводит их.
    """
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        print(f"Получено {len(ohlcv)} свечей\n")

        for i, candle in enumerate(ohlcv):
            timestamp, open_price, high, low, close, volume = candle
            print(f"Свеча {i}:")
            print(f"  Время: {timestamp}")
            print(f"  Открытие: {open_price}")
            print(f"  Хай: {high}")
            print(f"  Лоу: {low}")
            print(f"  Закрытие: {close}")
            print(f"  Объём: {volume}\n")

        return ohlcv
    except Exception as e:
        print(f"Ошибка при получении данных для {symbol}: {e}")
        return []

def find_fibonacci_high(ohlcv):
    """
    Находит самую высокую зелёную свечу, а затем проверяет, есть ли после неё красная свеча.
    Если да — возвращает цену закрытия этой зелёной свечи.
    """

    green_candles = []  # Список всех зелёных свечей (индекс, хай, закрытие)

    print("\nНачинаем анализ свечей...\n")

    # 1. Собираем все зелёные свечи
    for i in range(len(ohlcv) - 1):  # Не включаем последнюю свечу, так как после неё не с чем сравнивать
        open_price, high, low, close, _ = ohlcv[i][1:6]
        
        if close > open_price:  # Это зелёная свеча
            print(f"Зелёная свеча {i}: Открытие={open_price}, Хай={high}, Закрытие={close}")
            green_candles.append((i, high, close))  # Сохраняем индекс, high и close

    # 2. Если не нашли ни одной зелёной свечи — выход
    if not green_candles:
        print("Не найдено ни одной зелёной свечи")
        return None

    # 3. Находим самую высокую зелёную свечу и проверяем, есть ли после неё красная
    green_candles.sort(key=lambda x: x[1], reverse=True)  # Сортируем по high (по убыванию)

    for index, high, close in green_candles:
        if index + 1 < len(ohlcv):  # Проверяем, что есть следующая свеча
            next_open, next_close = ohlcv[index + 1][1], ohlcv[index + 1][4]
            print(f"Проверяем свечу {index + 1}: Открытие={next_open}, Закрытие={next_close}")

            if next_close < next_open:  # Если следующая свеча красная
                print(f"Красная свеча найдена после зелёной на индексе {index + 1}")
                print(f"Возвращаем закрытие самой высокой зелёной свечи: {close}")
                return close  # Возвращаем закрытие найденной свечи

    print("Нет зелёной свечи, после которой идёт красная")
    return None



async def main():
    symbol = "TWT/USDT"
    ohlcv = await fetch_data(symbol)
    
    if ohlcv:
        result = find_fibonacci_high(ohlcv)
        print("\nУровень Фибоначчи:", result)
    else:
        print("Данные по свечам не получены.")

asyncio.run(main())
