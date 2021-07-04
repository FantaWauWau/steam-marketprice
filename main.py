import csv
import os
import random
import math
import requests
import time
from calculate_wear import calculate_wear
from case_name import market_case_name
# CSGO Case Simulator

def is_stattrack() -> bool:
    """Returns True if random number <= 0.1, else False"""
    stattrack_chance = random.uniform(0, 1)
    if stattrack_chance <= 0.1:
        return True
    return False


def add_drop_for_quality(color):
    """Adds drops into drop_amount_by_quality"""
    if is_stattrack():
        drop_amount_by_quality["stat_" + color] += 1
    else:
        drop_amount_by_quality[color] += 1


# stores the amount of drops for each item quality
drop_amount_by_quality = {
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
with open('cache.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ["skin_name", "amount_of_drops"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()


# asks user for file name and checks if it exists.
while True:
    case_name = input("Enter Case name to open: ")
    if case_name[-4:] != ".csv":
        case_name = case_name + ".csv"

    if os.path.isfile(case_name):
        break
    else:
        print(f"File: {case_name} does not exist.")

# get current case price
formatted_case_name = market_case_name[case_name]
get_case_price = requests.get("https://steamcommunity.com/market/priceoverview/?"
                            "appid=730&currency=1&market_hash_name=" + formatted_case_name)

if get_case_price.status_code == 200: # 200 = successful request
    steam_response = get_case_price.json()
    case_price = float(steam_response["lowest_price"][1:]) # removes $
else:
    print(f"Failed to get price for {formatted_case_name}")


# asks for amount of cases or money amount to spend
while True:
    cases_to_open = input("Enter amount of cases or $: ")
    try:
        if "$" in cases_to_open:
            money_spent = float(cases_to_open.strip("$"))
            to_open = math.floor(money_spent / (2.59 + case_price))
            remaining_money = money_spent - (to_open * (2.59 + case_price))
            cash = money_spent - remaining_money
            print(f"{to_open} cases will be opened.")
            print(f"Remaining cash: ${round(remaining_money, 2)}")
            break
        else:
            cash = float(cases_to_open) * (2.59 + case_price)
            to_open = int(cases_to_open)
            break
    except ValueError:
        print("Something went wrong! \n"
              "Please enter amount of cases to open or for example 50$.")

# calculates amount of drops by quality for amount of cases to open
opened = 0
while opened < to_open:
    quality = random.uniform(0, 1)
    if 1 > quality >= 0.2007673:
        color = "blue"
        add_drop_for_quality(color)
    elif 0.2007673 > quality >= 0.0409208:
        color = "purple"
        add_drop_for_quality(color)
    elif 0.0409208 > quality >= 0.0089515:
        color = "pink"
        add_drop_for_quality(color)
    elif 0.0089515 > quality >= 0.0025576:
        color = "red"
        add_drop_for_quality(color)
    else:
        color = "yellow"
        add_drop_for_quality(color)
    opened += 1


# loops through the dictionary with drop amount for qualities and calculates the wear.
for quality, amount in drop_amount_by_quality.items():
    if amount != 0:
        calculate_wear(case_name, quality, amount)

# add items into new list, for multiple drops
complete_item_drop_list = []
with open('cache.csv', 'r', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if int(row["amount_of_drops"]) >= 1:
            for x in range(int(row["amount_of_drops"])):
                complete_item_drop_list.append(row["skin_name"])
                # work in progress: Anfragen für doppelte items werden mehrfach gestellt. evtl. nach Preis nach anfrage multiplizieren.


item_price_list = []
count = 0
for item in complete_item_drop_list:
    count += 1
    if count == 20:
        # steam will block you after too many requests
        print("TIMEOUT!")
        time.sleep(60)
        count = 0

    response = requests.get("https://steamcommunity.com/market/priceoverview/?"
                            "appid=730&currency=1&market_hash_name=" + item)
    if response.status_code == 200: # 200 = successful request
        steam_response = response.json()
        item_price_list.append(steam_response["lowest_price"])
    else:
        print(f"Failed to get price for {item}")

# strips currency sign ($) from steam response
item_prices = []
for price in item_price_list:
   price_without_currency = price[1:]
   item_prices.append(float(price_without_currency))

rounded_cash = round(cash, 2)
rounded_sum = round(sum(item_prices), 2)
rounded_result = round(sum(item_prices) - rounded_cash, 2)

print(f"Investment: ${rounded_cash}")
print(f"Return: ${rounded_sum}")
print(f"Return on invest: ${rounded_result}")

# deletes cache files with resuslts, no longer needed.
if os.path.exists('cache.csv'):
    os.remove('cache.csv')
