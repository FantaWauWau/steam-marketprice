import requests
import csv

#creates a list of all item names in the csvfile
item_names = []
with open("IEM_Stickerprice.csv", newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        item_names.append(row["Sticker"])

data_list = []
for item_name in item_names:
    response = requests.get('https://steamcommunity.com/market/priceoverview/?appid=730&currency=3&market_hash_name='+item_name)
    data = response.json()
    data_list.append(data["lowest_price"])
print(data_list)
