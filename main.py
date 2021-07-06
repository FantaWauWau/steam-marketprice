import csv
import os
import random
import math
import requests
import time
import locale
from functions import market_case_name, vanilla_check, is_stattrack, calculate_wear
# CSGO Case Simulator

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')


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

# creates csv file to store items names + drop amount
with open('cache.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ["skin_name", "amount_of_drops"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()


# case to open
while True:
    case_name = input("Enter Case name to open: ")
    if case_name[-4:] != ".csv":
        case_name = case_name + ".csv"

    if os.path.isfile(case_name):
        break
    else:
        print(f"File: {case_name} does not exist.")

# get current case price
formatted_case_name = market_case_name[case_name]  # formatted case name
get_case_price = requests.get("https://steamcommunity.com/market/priceoverview/?"
                              "appid=730&currency=1&market_hash_name="
                              + formatted_case_name)

if get_case_price.status_code == 200:  # 200 = successful request
    steam_response = get_case_price.json()
    case_price = float(steam_response["lowest_price"][1:])  # removes $
else:
    # case_price needs a value, program can't be executed.
    print(f"Failed to get price for {formatted_case_name}! \n"
          "Please wait 1-2 minutes or choose a different case.\n"
          "Quitting...")
    quit()


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


# loops through the dict with drop amount for qualities and calculates wear.
for quality, amount in drop_amount_by_quality.items():
    if amount != 0:
        skin_name_with_wear_dict = calculate_wear(case_name, quality, amount)
        with open('cache.csv', 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['skin_name', 'amount_of_drops']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            for skin_name, amount in skin_name_with_wear_dict.items():
                writer.writerow({'skin_name': skin_name, 'amount_of_drops': amount})

# add items into new list, for multiple drops
# if skins is a vanilla skin, the wear is removed in vanilla_check()
item_drop_dict = {}
request_count = 0
with open('cache.csv', 'r', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if int(row["amount_of_drops"]) >= 1:
            request_count += 1
            is_vanilla, vanilla_name = vanilla_check(row["skin_name"])
            if is_vanilla:
                try:
                    item_drop_dict[vanilla_name] += int(row["amount_of_drops"])
                except:
                    item_drop_dict[vanilla_name] = int(row["amount_of_drops"])
            else:
                item_drop_dict[row["skin_name"]] = int(row["amount_of_drops"])

print(f"Requesting prices for {request_count} unique skins.")
end_request_count = request_count
# remove fail list later, only for testing
fail_list = []
item_price_list = []
count = 0
for item_name, amount in item_drop_dict.items():
    count += 1
    if count == 20:
        # steam will block you after too many requests
        for i in range(60):
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"{i - 60} seconds left until next request.")
            time.sleep(1)
        os.system('cls' if os.name == 'nt' else 'clear')
        print("New requests are being sent...")
        count = 0

    response = requests.get("https://steamcommunity.com/market/priceoverview/?"
                            "appid=730&currency=1&market_hash_name=" + item_name)
    if response.status_code == 200:  # 200 == successful request
        steam_response = response.json()
        try:
            formatted_price = steam_response["lowest_price"][1:]  # removes $
            if "," in formatted_price:
                item_price_list.append(locale.atof(formatted_price))
            else:
                steam_price = float(formatted_price) * float(amount)
                item_price_list.append(steam_price)
        except:
            fail_list.append(item_name)
    else:
        fail_list.append(item_name)  # remove later, only for testing
    request_count -= 1
    print(f"{request_count} requests left.")
    time.sleep(0.3)


rounded_cash = round(cash, 2)
rounded_sum = round(sum(item_price_list), 2)
rounded_result = round(sum(item_price_list) - rounded_cash, 2)
os.system('cls' if os.name == 'nt' else 'clear')
# only for testing/debugging, remove later
if len(fail_list) > 0:
    for item in fail_list:
        print(f"Failed to get price for {item}")

print(f"You opened {to_open} cases for a total of {end_request_count} unique skins.")
print(f"Investment: ${rounded_cash}")
print(f"Return: ${rounded_sum}")
print(f"Return on invest: ${rounded_result}")

# deletes cache files
# useful for debugging
#if os.path.exists('cache.csv'):
    #os.remove('cache.csv')
