import requests

req = requests.get('https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=ethereum')
response = req.json()
print(f"REsponse: {response[0]['current_price']}")
