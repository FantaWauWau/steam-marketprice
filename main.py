import csv
import os
import random
import math
import requests
import time
import locale
import functions
import variables

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
functions.file_check()

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
except ValueError:
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

# glove cases check, stattrack needs to be removed from drops
glove_case_list = ["Glove Case", "Operation Hydra Case", "Clutch Case",
                   "Operation Broken Fang Case", "Snakebite Case"]

is_glove_case = False
for case in glove_case_list:
    if case == case_name:
        is_glove_case = True

# calculates amount of drops by quality for amount of cases to open
opened = 0
while opened < to_open:
    quality = random.uniform(0, 1)
    if 1 > quality >= 0.2007673:
        drop_amount_by_quality[functions.add_drop_for_quality("blue")] += 1
    elif 0.2007673 > quality >= 0.0409208:
        drop_amount_by_quality[functions.add_drop_for_quality("purple")] += 1
    elif 0.0409208 > quality >= 0.0089515:
        drop_amount_by_quality[functions.add_drop_for_quality("pink")] += 1
    elif 0.0089515 > quality >= 0.0025576:
        drop_amount_by_quality[functions.add_drop_for_quality("red")] += 1
    else:
        drop = functions.add_drop_for_quality("yellow")
        # gloves
        if is_glove_case and "stat_" in drop:
            drop = drop[5:]  # removes stat_
        drop_amount_by_quality[drop] += 1
    opened += 1


# loops through the dict with drop amount for qualities and calculates wear.
for quality, amount in drop_amount_by_quality.items():
    if amount != 0:
        skin_wear_dict = functions.calculate_wear(case_name, quality, amount)
        with open('cache.csv', 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['skin_name', 'amount_of_drops']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            for skin_name, amount in skin_wear_dict.items():
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
            is_vanilla, vanilla_name = functions.vanilla_check(row["skin_name"])
            if is_vanilla:
                try:
                    item_drop_dict[vanilla_name] += int(row["amount_of_drops"])
                except ValueError:
                    item_drop_dict[vanilla_name] = int(row["amount_of_drops"])
            else:
                item_drop_dict[row["skin_name"]] = int(row["amount_of_drops"])

avg_req_time = functions.calculate_avg_request_time()

# calculates how often the program will timeout, when requesting
amount_of_timeouts = math.floor(request_count / 20)
if amount_of_timeouts < 1:
    estimated_time = request_count * avg_req_time
else:
    estimated_time = (amount_of_timeouts * 60) + (request_count * avg_req_time)

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
print()

timeout_count = 0
end_request_count = request_count
fail_list = []
item_price_list = []
act_request_time = []

# loops through the dict of {item: amount} of drops and sents price request
for item_name, amount in item_drop_dict.items():
    if timeout_count == 20 and request_count != 0:
        functions.timeout()
        timeout_count = 0

    start_time = time.time()
    request_success, response_value = functions.steam_request(item_name, amount)
    if request_success:
        item_price_list.append(response_value)
    else:
        functions.append_failed_items(item_name, response_value, request_count)
        fail_list.append((item_name, amount))

    request_count -= 1
    timeout_count += 1
    percentage_remaining = round(100 - (request_count / end_request_count * 100), 2)
    print(f"{request_count} requests left ({percentage_remaining}% completed)")
    time.sleep(0.3)
    act_request_time.append((time.time() - start_time))


failed_twice_list = []
request_count = len(fail_list)
if len(fail_list) > 0:
    print(f"Failed to get item prices for {request_count} items.")
    print("Starting second attempt...")
    time.sleep(3)
    functions.timeout()
    # loops through failed items and first request and reattempts to get price
    for item_name, amount in fail_list:
        if timeout_count == 20 and request_count != 0:
            functions.timeout()
            timeout_count = 0

        start_time = time.time()
        request_success, response_value = functions.steam_request(item_name, amount)
        if request_success:
            item_price_list.append(response_value)
            print(f"Got price for {item_name} on second attempt!")
            time.sleep(1)
        else:
            functions.append_failed_items(item_name, response_value, request_count)
            failed_twice_list.append(item_name)

        request_count -= 1
        timeout_count += 1
        percentage_remaining = round(100 - (request_count / end_request_count * 100), 2)
        print(f"{request_count} requests left ({percentage_remaining}% completed)")
        time.sleep(0.3)
        act_request_time.append((time.time() - start_time))

# writes requests times for current run in csv
with open('est_time.csv', 'a', newline='') as file:
    fieldnames = ['act_request_time']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    for request_time in act_request_time:
        writer.writerow({'act_request_time': request_time})

# end results
rounded_cash = round(cash, 2)
rounded_sum = round(sum(item_price_list), 2)
rounded_result = round(sum(item_price_list) - rounded_cash, 2)
os.system('cls' if os.name == 'nt' else 'clear')
print("End Results:")
print()
print(f"You opened {to_open} cases for a total of {end_request_count} skins.")
print(f"Investment: ${rounded_cash}")
print(f"Return: ${rounded_sum}")
print(f"Return on invest: ${rounded_result}")
print(f"Actual time: {round(sum(act_request_time), 2)}")

current_results = []
results = []

with open('complete_results.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row["case_name"] != case_name:
            current_results.append(row)
        else:
            results.append(row)

# add current result for opened case to stored result of case x
total_opened = int(results[0]["total_opened"]) + to_open
total_spent = float(results[0]["total_spent"]) + rounded_cash
return_on_invest = float(results[0]["return_on_invest"]) + rounded_result
current_results.append({'case_name': case_name,
                        'total_opened': total_opened,
                        'total_spent': round(total_spent, 2),
                        'return_on_invest': round(return_on_invest, 2)
                        })
current_results.reverse()

with open('complete_results.csv', 'w') as csvfile:
    fieldnames = ["case_name", "total_opened", "total_spent", "return_on_invest"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in current_results:
        writer.writerow(row)

# prints items which failed twice to get price for
if len(failed_twice_list) > 0:
    print("Failed twice to get price for: ")
    for item in failed_twice_list:
        print(item)
