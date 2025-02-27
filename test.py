import requests
import pprint
url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
params = {"symbol": 'TWT'}
headers = {"X-CMC_PRO_API_KEY": "48037f04-95b2-436d-899c-5e2d5e514f7e"}

response = requests.get(url, headers= headers, params=params)
data = response.json()

pprint.pprint(data['data']['TWT']['cmc_rank'])
