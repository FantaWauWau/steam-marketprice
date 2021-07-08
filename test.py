from locale import setlocale
import requests
response = requests.get("https://steamcommunity.com/market/priceoverview/?appid=730"
                        "&currency=1&market_hash_name=StatTrak™ M4A1-S | Dark Water (Minimal Wear)")
steam_response = response.json()
print(steam_response)


if 'lowest_price' in steam_response:
    print("lowest")
else:
    print("Empty")

if 'median_price' in steam_response:
    print("median")
else:
    print("Empty")
