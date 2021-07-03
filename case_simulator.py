import csv
import random
import requests
import time
from calculate_wear import calculate_wear
# CSGO Case Simulator

def is_stattrack() -> bool:
    """Returns True if random number <= 0.1, else False"""
    stattrack_chance = random.uniform(0, 1)
    if stattrack_chance <= 0.1:
        return True
    else:
        return False

dropped = {
    "blue": 0,
    "purple": 0,
    "pink": 0,
    "red": 0,
    "yellow": 0,

    "stat_blue": 0,
    "stat_purple": 0,
    "stat_pink": 0,
    "stat_red": 0,
    "stat_yellow": 0
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
        if is_stattrack():
            dropped["stat_blue"] += 1
        else:
            dropped["blue"] += 1
    elif 0.2007673 > rarity >= 0.0409208:
        if is_stattrack():
            dropped["stat_purple"] += 1
        else:
            dropped["purple"] += 1
    elif 0.0409208 > rarity >= 0.0089515:
        if is_stattrack():
            dropped["stat_pink"]
        else:
            dropped["pink"] += 1
    elif 0.0089515 > rarity >= 0.0025576:
        if is_stattrack():
            dropped["stat_red"] += 1
        else:
            dropped["red"] += 1
    else:
        if is_stattrack():
            dropped["stat_yellow"] += 1
        else:
            dropped["yellow"] += 1
    opened += 1

# values of item quality drops into variables
blue = dropped["blue"]
purple = dropped["purple"]
pink = dropped["pink"]
red = dropped["red"]
yellow = dropped["yellow"]

stat_blue = dropped["stat_blue"]
stat_purple = dropped["stat_purple"]
stat_pink = dropped["stat_pink"]
stat_red = dropped["stat_red"]
stat_yellow = dropped["stat_yellow"]

drop_dict = {"blue": blue, "purple": purple, "pink": pink, "red": red, "yellow": yellow,
            "stat_blue": stat_blue, "stat_purple": stat_purple, "stat_pink": stat_pink,
            "stat_red": stat_red, "stat_yellow": stat_yellow}

for key, value in drop_dict.items():
    if value != 0:
        calculate_wear(case_name, key, value)

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
