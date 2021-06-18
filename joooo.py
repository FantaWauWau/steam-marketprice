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
print(item_list[4:])
