import csv
import random
import os
import requests
import locale
import time
from typing import Union

from variables import http_status_codes, market_case_name


def clear_terminal():
    """Clears terminal window"""
    return os.system('cls' if os.name == 'nt' else 'clear')


def stattrack_check(color: str) -> str:
    """Modifies parameter 'color' based on if the drop is stattrack (10%).

    Args:
        color: The color of the skin e.g. 'blue'

    Returns:
        If stattrack, returns "stat_" + 'color'.

        If regular skin, it returns the unmodified passed parameter.
    """
    if random.uniform(0, 1) <= 0.1:
        return "stat_" + color
    else:
        return color


def drop_check(case_name: str, item: str) -> bool:
    """Checks if item exists. Not every item has all wears.

    Args:
        case_name: name of opened case, this csv is checked.
        item: item name with wear to be checked, whether it exists in csv.

    Returns:
        True, if skin + wear exists.

        False, if skin + wear doesn't exist.
    """
    # removes wear from item name
    item_without_wear = ""
    if "Factory New" in item:
        item_without_wear = item[:-13]
    elif "(Minimal Wear)" in item:
        item_without_wear = item[:-14]
    elif "(Field-Tested)" in item:
        item_without_wear = item[:-14]
    elif "(Well-Worn)" in item:
        item_without_wear = item[:-11]
    elif "(Battle-Scarred)" in item:
        item_without_wear = item[:-16]
    else:
        print(f"Failed to format {item}! \n"
              "Script can't be executed anymore...")
        quit()

    item_wear = ""
    try:
        with open(f"Cases/{case_name}", 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['skin_name'] == item_without_wear.strip():
                    item_wear = row["wear"]
    except FileNotFoundError:
        print(f"Couldn't find file: {case_name}!")
        print("Quitting...")
        quit()

    wear_list = item_wear.split(",")
    # builds item_name with all availables wears and adds them into a list
    full_item_names = []
    for wear in wear_list:
        full_item_name = item_without_wear + wear.lstrip()
        full_item_names.append(full_item_name)

    # function paramater (item) is checked if it exists in list
    # with all available item + wears.
    if item in full_item_names:
        return True
    return False


def vanilla_check(skin_name: str) -> Union[bool, str]:
    """Checks if skins is a vanilla knife.

    Args:
        skin_name: name of skin to check, with wear.
    Returns:
        Tuple of True, skin name without wear if skin is vanilla.

        False if the skin is not a vanilla, original skin name.
    """
    with open("Cases/vanilla_knife.csv", 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if skin_name == row["skin_name"]:
                vanilla_name = row["vanilla_name"]
                return True, vanilla_name  # returns skin name without wear
        return False, skin_name  # returns unformatted skin name


def calculate_drops(case_name: str, quality: str, amount: int) -> dict:
    """Picks a random skin from items of 'quality' of 'case_name' and
    calculates a random wear for it.

    Args:
        case_name: name of case which is opened by user
        quality: Quality of skin (e.g. "blue", "yellow")

        amount: Amount of drops for the current quality (e.g. "blue": 50)

    Returns:
        Dictionary with all skin names + wear with amount of drops for each.
    """
    # creates a list of dicts with content of csv file (opened case name)
    item_list = []
    with open(f"Cases/{case_name}", 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            item_list.append(row)

    # removes every dict from item_list which doesn't match the passed quality
    items_by_quality = [item for item in item_list
                        if item['quality'] == quality]

    # creates a list with all skin names of quality x (e.g. "blue")
    all_skin_names_by_quality = []
    for item in range(0, len(items_by_quality)):
        skin_name = items_by_quality[item]['skin_name']
        all_skin_names_by_quality.append(skin_name)

    # picks random skin names for total amount of drops of quality x
    skin_names_by_quality = []
    for i in range(int(amount)):
        random_skin_name = random.choice(all_skin_names_by_quality)
        skin_names_by_quality.append(random_skin_name)

    # initializes dict with skin name + wear as key and drop count as value
    skin_name_with_wear = {}
    for skin_name in skin_names_by_quality:
        skin_name_with_wear[skin_name + " (Battle-Scarred)"] = 0
        skin_name_with_wear[skin_name + " (Well-Worn)"] = 0
        skin_name_with_wear[skin_name + " (Field-Tested)"] = 0
        skin_name_with_wear[skin_name + " (Minimal Wear)"] = 0
        skin_name_with_wear[skin_name + " (Factory New)"] = 0

    # loops through skin names and calculates wear,
    # then checks if skin name with wear exists in current case (csvfile),
    # if skin exists drop count is raised by 1
    for item in skin_names_by_quality:
        while True:
            float = random.uniform(0, 1)
            if 1 > float >= 0.45:
                if drop_check(case_name, item + " (Battle-Scarred)"):
                    skin_name_with_wear[item + " (Battle-Scarred)"] += 1
                    break
                continue
            elif 0.45 > float >= 0.38:
                if drop_check(case_name, item + " (Well-Worn)"):
                    skin_name_with_wear[item + " (Well-Worn)"] += 1
                    break
                continue
            elif 0.38 > float >= 0.15:
                if drop_check(case_name, item + " (Field-Tested)"):
                    skin_name_with_wear[item + " (Field-Tested)"] += 1
                    break
                continue
            elif 0.15 > float >= 0.07:
                if drop_check(case_name, item + " (Minimal Wear)"):
                    skin_name_with_wear[item + " (Minimal Wear)"] += 1
                    break
                continue
            else:
                if drop_check(case_name, item + " (Factory New)"):
                    skin_name_with_wear[item + " (Factory New)"] += 1
                    break
                continue

    return skin_name_with_wear


def calculate_avg_request_time() -> float:
    """Calculates average of all response times for the user.

    Returns:
        average: average of locally saved request times of user.

        0.7: 0.7s is used as default request time if calculation fails,
        or has no values, because of first run.
    """
    try:
        total_values = -1  # -1 for header in csv
        sum_of_time = 0
        with open('est_time.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                total_values += 1
                sum_of_time += float(row['request time'])
        average = sum_of_time / total_values
        return average

    except ZeroDivisionError:
        print("Using 0.7s as default request time for first run.\n"
              "With more runs, estimated time will be more accurate.")
        time.sleep(4)
        clear_terminal()
        return 0.7


def file_check() -> None:
    """Checks if neccessary files exist. If not they are created.
       Some files are created without condition, as they need to be empty
       on execution.
    """
    if not os.path.isfile('est_time.csv'):
        with open('est_time.csv', 'w', newline='') as file:
            fieldnames = ['request time']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

    if not os.path.isfile('complete_results.csv'):
        with open('complete_results.csv', 'w', newline='') as file:
            fieldnames = ["case", "total opened", "total spent",
                          "return on invest"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for item in market_case_name:
                writer.writerow({'case': item,
                                 'total opened': 0,
                                 'total spent': 0,
                                 'return on invest': 0
                                 })

    # cache.csv & failed_items.csv are always created new on start.
    with open('cache.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["skin", "amount"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

    with open('failed_items.csv', 'w', newline='') as file:
        fieldnames = ['skin', 'request_count', 'response', 'http_status_code']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({'skin': 0,
                         'request_count': 0,
                         'response': 0,
                         'http_status_code': 0
                         })


def append_failed_items(name: str, response: int, request_count: int) -> None:
    """Writes failed items with additional info into a file for debugging.

    Args:
        name: name of skin.
        response: The http code returned by steam on failed request.
        request_count: Position in loop when it received an invalid response.
    """
    with open('failed_items.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if name in row['skin'] and str(response) in row['response']:
                return None

    with open('failed_items.csv', 'a', newline='', encoding='utf-8') as file:
        fieldnames = ['skin', 'request_count', 'response', 'http_status_code']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow({'skin': name,
                         'request_count': request_count,
                         'response': response,
                         'http_status_code': http_status_codes[response]
                         })


def steam_request(name: str, amount: int) -> Union[bool, float]:
    """Sends request to steam market to get price for an 'item_name'.
       If steam returns a price its multiplied by the dropped 'amount'.

    Returns:
        A Tuple, consisting of (bool, value)

        True, price * amount

        False, http response code.
    """
    response = requests.get("https://steamcommunity.com/market/priceoverview/?"
                            "appid=730&currency=1&market_hash_name=" + name)

    try:
        formatted_response = response.json()
    except Exception:
        return False, response.status_code

    try:
        if "lowest_price" in formatted_response:
            formatted_price = formatted_response["lowest_price"][1:]
        elif "median_price" in formatted_response:
            formatted_price = formatted_response["median_price"][1:]
        if "," in formatted_price:
            return True, float(locale.atof(formatted_price) * amount)
        else:
            return True, float(formatted_price) * amount
    except Exception:
        return False, response.status_code


def timeout() -> None:
    """Stops program execution for 60s. Too many request to steam without
       timeouts will result in temporary ban from sending new requests.
    """
    for i in range(60):
        clear_terminal()
        print(f"{i - 60} seconds left until next request.")
        time.sleep(1)
        clear_terminal()
        print("New requests are being sent...")


def print_request_status(request_count: int, total_case_amount: int) -> None:
    """Prints current status of completed requests as int and in % completed"""
    percentage = round(100 - (request_count / total_case_amount * 100), 2)
    print(f"{request_count} requests left ({percentage}% completed)")
