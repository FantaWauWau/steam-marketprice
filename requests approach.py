import requests
import time


item_list = []
data_list = []
dict_list = []
steamid = 76561198050601247
filter = str(input("Input a filter: "))

def getInventoryPrices(steamid, filter):
    data = requests.get(
        f"https://steamcommunity.com/profiles/{steamid}/inventory/json/730/2?l=english&count=5000")
    json_data = data.json()
    descriptions = json_data.get("rgDescriptions")
    for item in descriptions:
        if int(descriptions[item]["instanceid"]) != 0:
            items = str(descriptions[item]["market_hash_name"])
            item_list.append(items)
        else:
            continue
    print(item_list)
    print(len(item_list))
    item_names = [item for item in item_list if filter in item]
    time.sleep(69)
    for item_name in item_names:
        response = requests.get("https://steamcommunity.com/market/priceoverview/?"
                                "appid=730&currency=3&market_hash_name="+item_name)
        if response.status_code == 200:
            data_market = response.json()
            data_list.append(data_market["lowest_price"])
            item_dict = {
                item_name: data_market["lowest_price"]
            }
            dict_list.append(item_dict)
        else:
            continue

    print(data_list)
    print(dict_list)


getInventoryPrices(steamid, filter)
