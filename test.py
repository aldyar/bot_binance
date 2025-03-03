"""import requests
import pprint
url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
params = {"symbol": 'TWT'}
headers = {"X-CMC_PRO_API_KEY": "48037f04-95b2-436d-899c-5e2d5e514f7e"}

response = requests.get(url, headers= headers, params=params)
data = response.json()

pprint.pprint(data['data']['TWT']['cmc_rank'])"""




import requests
import pprint

def get_cmc_info(symbol: str, api_key: str) -> dict:
    """
    Получает ранг и капитализацию указанной криптовалюты.

    :param symbol: Символ криптовалюты (например, 'TWT')
    :param api_key: API-ключ CoinMarketCap
    :return: Словарь с рангом и капитализацией
    """
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
