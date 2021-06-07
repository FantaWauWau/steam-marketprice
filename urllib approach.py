import csv
import urllib.request
import urllib.parse
import json
import time
from datetime import date


#creates a list of all item names in the csvfile
item_names = []
with open("IEM_Stickerprice.csv", newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        item_names.append(row["Sticker"])

#merges the link with the item name
url_list = []
for item in item_names:
    name = urllib.parse.quote(item)
    print(name)
    item_url = ('https://steamcommunity.com/market/priceoverview/?appid=730&currency=3&market_hash_name='+name)
    url_list.append(item_url)
print(url_list)

"""
def url_builder(item_name):
    name_item = []
    for item in item_name:
        name = urllib.parse.quote(item)

    item_url = 'https://steamcommunity.com/market/priceoverview/?appid=730&currency=3&market_hash_name='+name
    print(item_url)
    request_item_url = urllib.request.urlopen(item_url)
    read_item_url = request_item_url.read().decode()
    item_data = json.loads(read_item_url)
    return item_data["lowest_price"]


today = date.today()
date = today.strftime("%m/%d/%y")
with open("IEM2_nice.csv", "a", newline="") as csvfile:
    fieldnames = ["Sticker", date]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    dict_list = []
    for item in item_names:
        item_dict = {
            "Sticker": item,
            "Price": url_builder(item)
        }
        writer.writerow({"Sticker": item, date: url_builder(item)})"""

