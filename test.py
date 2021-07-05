import json
import requests
import locale

locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )
x = 100.50
print(locale.atof(x))
item = "StatTrak™ AWP | Lightning Strike (Minimal Wear)"
response = requests.get("https://steamcommunity.com/market/priceoverview/?"
                            "appid=730&currency=1&market_hash_name=" + item)
if response.status_code == 200: # 200 == successful request
        steam_response = response.json()
        formatted_price = steam_response["lowest_price"][1:]
        print(locale.atof(formatted_price))
else:
    print("FAIL")
