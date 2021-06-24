import csv
import random
import requests
import time

# CSGO Case Simulator

def calculate_wear(quality: str, amount: int):
    """Takes skins quality (color) and drop amount as arguments and calculates/writes drops in csv file"""
    item_list = []
    with open(case_name, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            item_list.append(row)

    new_list = [item for item in item_list if item['type'] == quality]
    listed = []
    for item in range(0, len(new_list)):
        items_names = new_list[item]['case']
        listed.append(items_names)

    drops = []
    for i in range(amount):
        dropped = random.choice(listed)
        drops.append(dropped)
    global wear
    wear = {}
    for i in drops:
        wear[i + " (Well-Worn)"] = 0
        wear[i + " (Battle-Scarred)"] = 0
        wear[i + " (Field-Tested)"] = 0
        wear[i + " (Minimal Wear)"] = 0
        wear[i + " (Factory New)"] = 0

    for i in drops:
        rarity = random.uniform(0, 1)
        if 1 > rarity >= 0.45:
            wear[i + " (Battle-Scarred)"] += 1
        elif 0.45 > rarity >= 0.38:
                wear[i + " (Well-Worn)"] += 1
        elif 0.38 > rarity >= 0.15:
            wear[i + " (Field-Tested)"] += 1
        elif 0.15 > rarity >= 0.07:
            wear[i + " (Minimal Wear)"] += 1
        else:
            wear[i + " (Factory New)"] += 1

    with open('cache.csv', 'a', newline='') as csvfile:
        fieldnames = ['key', 'value']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for key, value in wear.items():
            writer.writerow({'key': key, 'value': value})


dropped = {
    "blue": 0,
    "purple": 0,
    "pink": 0,
    "red": 0,
    "yellow": 0
    }

# create csv file to store items names and drop amount later
with open('cache.csv', 'w', newline='') as csvfile:
    fieldnames = ["key", "value"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

# open case csv file
while True:
    case_name = input("Enter Case name to open: ")
    if case_name[-4:] != ".csv":
        case_name = case_name + ".csv"
    try:
        skin_names = []
        with open(case_name, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                skin_names.append(row['case'])
        break
    except OSError as error:
        print(error)

# open case for amount, € or $
while True:
    cases_to_open = input("Enter amount of cases or $: ")
    try:
        if "$" in cases_to_open:
            cash = float(cases_to_open[:-1])
            cases_formatted = cases_to_open.replace("$", "")
            to_open = round(int(cases_formatted) / 2.59)
            break
        else:
            cash = float(cases_to_open) * 2.59
            to_open = int(cases_to_open)
            break
    except ValueError:
        print("Something went wrong! \n"
              "Please enter amount of cases to open or for example 50$.")

# calculate dropped item quality
opened = 0
while opened < to_open:
    rarity = random.uniform(0, 1)
    if 1 > rarity >= 0.2007673:
        dropped["blue"] += 1
    elif 0.2007673 > rarity >= 0.0409208:
        dropped["purple"] += 1
    elif 0.0409208 > rarity >= 0.0089515:
        dropped["pink"] += 1
    elif 0.0089515 > rarity >= 0.0025576:
        dropped["red"] += 1
    else:
        dropped["yellow"] += 1
    opened += 1

# values of item quality drops into variables
blue = dropped["blue"]
purple = dropped["purple"]
pink = dropped["pink"]
red = dropped["red"]
yellow = dropped["yellow"]

drop_dict = {"blue": blue, "purple": purple, "pink": pink, "red": red, "yellow": yellow}

for key, value in drop_dict.items():
    if value != 0:
        calculate_wear(key, value)

# add items into new list, for multiple drops
dropped_items = []
with open('cache.csv', 'r', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if int(row["value"]) >= 1:
            for x in range(int(row["value"])):
                dropped_items.append(row["key"])


data_list = []
count = 0
for item in dropped_items:
    count += 1
    if count == 20:
        # timeout, steam will block new requests after some time
        print("TIMEOUT!")
        time.sleep(60)
        count = 0

    response = requests.get("https://steamcommunity.com/market/priceoverview/?"
                            "appid=730&currency=1&market_hash_name=" + item)
    if response.status_code == 200:
        data_market = response.json()
        data_list.append(data_market["lowest_price"])
    else:
        print(f"Failed to get price for {item}")


int_list = []
for price in data_list:
   remove = price[1:]
   int_list.append(float(remove))

rounded_cash = round(cash, 2)
rounded_sum = round(sum(int_list), 2)
rounded_result = round(sum(int_list) - rounded_cash, 2)

print(f"Investment: ${rounded_cash}")
print(f"Return: ${rounded_sum}")
print(f"Return on invest: ${rounded_result}")
