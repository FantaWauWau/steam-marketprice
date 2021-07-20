import csv
import os
import random
import math
import requests
import time
import locale

import variables
import functions as func

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

func.clear_terminal()
func.file_check()

drops_by_quality = {
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

# case to open
while True:
    case_name = input("Enter Case name to open: ").casefold()
    if case_name in variables.case_name_into_csv:
        case_name = variables.case_name_into_csv[case_name]
        break
    if case_name[-4:] != ".csv":
        case_name = case_name + ".csv"
    if os.path.isfile(f"Cases/{case_name}"):
        break
    else:
        print(f"File: {case_name} does not exist.")

# get current case price
formatted_case_name = variables.market_case_name[case_name]  # market name
case_price = requests.get("https://steamcommunity.com/market/priceoverview/?"
                          "appid=730&currency=1&market_hash_name="
                          + formatted_case_name)

try:
    steam_response = case_price.json()
    case_price = float(steam_response["lowest_price"][1:])  # removes $
except TypeError:
    print(f"Failed to get price for {formatted_case_name}! \n"
          "Please wait 1-2 minutes or choose a different case.")
    quit()


while True:
    cases_to_open = input("Enter amount of cases or $: ")
    try:
        if "$" in cases_to_open:
            money_spent = float(cases_to_open.strip("$"))
            to_open = math.floor(money_spent / (2.59 + case_price))
            remaining_money = money_spent - (to_open * (2.59 + case_price))
            money = money_spent - remaining_money
            print(f"{to_open} cases will be opened.")
            print(f"Remaining money: ${round(remaining_money, 2)}")
            break
        else:
            money = float(cases_to_open) * (2.59 + case_price)
            to_open = int(cases_to_open)
            break
    except ValueError:
        print("Something went wrong! \n"
              "Please enter amount of cases to open or for example 50$.")


glove_case_list = ["Glove Case", "Operation Hydra Case", "Clutch Case",
                   "Operation Broken Fang Case", "Snakebite Case"]
# checks if current case is a case with gloves
is_glove_case = False
for case in glove_case_list:
    if case == case_name:
        is_glove_case = True

# amount of drops by quality, including stattracks. For amount of cases to open
opened = 0
while opened < to_open:
    quality = random.uniform(0, 1)
    if 1 > quality >= 0.2007673:
        drops_by_quality[func.stattrack_check("blue")] += 1
    elif 0.2007673 > quality >= 0.0409208:
        drops_by_quality[func.stattrack_check("purple")] += 1
    elif 0.0409208 > quality >= 0.0089515:
        drops_by_quality[func.stattrack_check("pink")] += 1
    elif 0.0089515 > quality >= 0.0025576:
        drops_by_quality[func.stattrack_check("red")] += 1
    else:
        drop = func.stattrack_check("yellow")
        if is_glove_case and "stat_" in drop:
            drop = drop[5:]  # removes stat_
        drops_by_quality[drop] += 1
    opened += 1


# loops through the dict with drop amount for qualities and drops random skin.
for quality, amount in drops_by_quality.items():
    if amount != 0:
        skin_wear_dict = func.calculate_drops(case_name, quality, amount)
        with open('cache.csv', 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['skin', 'amount']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            for skin, amount in skin_wear_dict.items():
                writer.writerow({'skin': skin, 'amount': amount})

# items in csv are checked for vanilla skins
# if skins is a vanilla skin, the wear is removed in vanilla_check()
item_drop_dict = {}
with open('cache.csv', 'r', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if int(row["amount"]) >= 1:
            is_vanilla, vanilla_name = func.vanilla_check(row["skin"])
            if is_vanilla:
                try:
                    item_drop_dict[vanilla_name] += int(row["amount"])
                except ValueError:
                    item_drop_dict[vanilla_name] = int(row["amount"])
            else:
                item_drop_dict[row["skin"]] = int(row["amount"])

request_count = len(item_drop_dict)
request_time = func.calculate_avg_request_time()

# calculates how often the program will timeout, depending on total requests
amount_of_timeouts = math.floor(request_count / 20)
if amount_of_timeouts < 1:
    estimated_time = request_count * request_time
else:
    estimated_time = (amount_of_timeouts * 60) + (request_count * request_time)

print(f"Requesting prices for {request_count} unique skins.")
# calculates estimated time to sent all requests and process them
if estimated_time > 60:
    minutes = estimated_time // 60
    seconds = round(estimated_time - minutes * 60, 2)
    print(f"Estimated Time: {int(minutes)} mins and {int(seconds)}s")
elif estimated_time == 60:
    print("Estimated time is 1 minute.")
else:
    print(f"Estimated time is {math.ceil(estimated_time)} seconds.")

timeout_count = 0
total_case_amount = request_count
fail_list = []
item_price_list = []
request_times = []

# loops through the dict of {item: amount} of drops and sents price request
for item_name, amount in item_drop_dict.items():
    if timeout_count == 20 and request_count != 0:
        func.timeout()
        timeout_count = 0

    start_time = time.time()
    request_success, response_value = func.steam_request(item_name, amount)
    if request_success:
        item_price_list.append(response_value)
    else:
        func.append_failed_items(item_name, request_count, response_value)
        fail_list.append((item_name, amount))

    request_count -= 1
    timeout_count += 1
    func.print_request_status(request_count, total_case_amount)
    time.sleep(0.3)
    request_times.append((time.time() - start_time))


failed_twice_list = []
request_count = len(fail_list)
if len(fail_list) > 0:
    print(f"Failed to get item prices for {request_count} items.")
    print("Starting second attempt...")
    time.sleep(3)
    func.timeout()
    # loops through failed items and first request and reattempts to get price
    for item_name, amount in fail_list:
        if timeout_count == 20 and request_count != 0:
            func.timeout()
            timeout_count = 0

        start_time = time.time()
        request_success, response_value = func.steam_request(item_name, amount)
        if request_success:
            item_price_list.append(response_value)
            print(f"Got price for {item_name} on second attempt!")
            time.sleep(1)
        else:
            func.append_failed_items(item_name, request_count, response_value)
            failed_twice_list.append(item_name)

        request_count -= 1
        timeout_count += 1
        func.print_request_status(request_count, total_case_amount)
        time.sleep(0.3)
        request_times.append((time.time() - start_time))

# appends request times for current run into csv
with open('est_time.csv', 'a', newline='') as file:
    fieldnames = ['request time']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    for request_time in request_times:
        writer.writerow({'request time': request_time})

# end results
rounded_cash = round(money, 2)
rounded_sum = round(sum(item_price_list), 2)
rounded_result = round(sum(item_price_list) - rounded_cash, 2)
func.clear_terminal()
print("End Results:")
print(f"You opened {to_open} cases for a total of {total_case_amount} skins.")
print(f"Investment: ${rounded_cash}")
print(f"Return: ${rounded_sum}")
print(f"Return on invest: ${rounded_result}")

current_results = []
results = []
with open('complete_results.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row["case"] != case_name:
            current_results.append(row)
        else:
            results.append(row)

# add current result to stored result of case x
total_opened = int(results[0]["total opened"]) + to_open
total_spent = float(results[0]["total spent"]) + rounded_cash
return_on_invest = float(results[0]["return on invest"]) + rounded_result
current_results.append({'case': case_name,
                        'total opened': total_opened,
                        'total spent': round(total_spent, 2),
                        'return on invest': round(return_on_invest, 2)
                        })

with open('complete_results.csv', 'w') as csvfile:
    fieldnames = ["case", "total opened", "total spent", "return on invest"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    current_results.reverse()
    for row in current_results:
        writer.writerow(row)

# prints items which failed twice to get price
if len(failed_twice_list) > 0:
    print("Failed twice to get price for: ")
    for item in failed_twice_list:
        print(item)
