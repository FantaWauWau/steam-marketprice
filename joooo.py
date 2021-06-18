import requests

numbers = []
item_list = []
new_list = []
page = requests.get('https://steamcommunity.com/market/search/render/?search_descriptions=Container&sort_dir=desc&appid=730&norender=1&count=1')
page_data = page.json()
data_page = page_data.get("results")
print(data_page)
items = data_page[0]["asset_description"]["descriptions"]
#item_type = data_page[0]["asset_description"]["type"]
print(items)
for number in range(0, len(items)):
    something = items[number]
    item_list.append(something)
print(item_list[:])


"""steamid = 76561198050601247

item_list = []
data = requests.get(
    f"https://steamcommunity.com/profiles/{steamid}/inventory/json/730/2?l=english&count=5000")
json_data = data.json()
print(data.json())
descriptions = json_data["rgDescriptions"]
print(descriptions)
print(type(descriptions))
print(type(data.json()))

for item in descriptions:
    items = str(descriptions[item]['market_name'])
    print(type(items))
    item_list.append(items)
print(item_list)
print(type(item_list))
"""
