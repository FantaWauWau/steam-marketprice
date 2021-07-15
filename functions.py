import csv
import random
import os
from http_codes import http_status_codes

# dictionary for formatting case name for price request to steam
market_case_name = {
    "bravo_case.csv": "Operation Bravo Case",
    "esports_2013_case.csv": "eSports 2013 Case",
    "esports_2013_winter_case.csv": "eSports 2013 Winter Case",
    "esports_2014_summer_case.csv": "eSports 2014 Summer Case",
    "phoenix_case.csv": "Operation Phoenix Weapon Case",
    "revolver_case.csv": "Revolver Case",
    "vanguard_case.csv": "Operation Vanguard Weapon Case",
    "weapon_case_2.csv": "CS:GO Weapon Case 2",
    "weapon_case_3.csv": "CS:GO Weapon Case 3",
    "weapon_case.csv": "CS:GO Weapon Case",
    "winter_offensive_case.csv": "Winter Offensive Weapon Case"
}


def is_stattrack() -> bool:
    """Returns True if random number <= 0.1 == stat strack skin."""
    stattrack_chance = 0.1
    random_num = random.uniform(0, 1)
    if random_num <= stattrack_chance:
        return True
    return False


def drop_check(case_name: str, item: str) -> bool:
    """Checks if item exists. Because not every item has all wears.

    Args:
        case_name: name of case which is opened. This one will be checked.
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


def vanilla_check(skin_name: str):
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


def calculate_wear(case_name: str, quality: str, amount: int) -> vars:
    """Calculates a random wear for the dropped item qualities.

    Args:
        case_name: name of case which is opened by user.
        quality: Quality of skin (e.g. "blue", "yellow").
        amount: Amount of drops for the current quality (e.g. "blue": 50).

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
    items_by_quality = [item for item in item_list if item['quality'] == quality]

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


def calculate_avg_request_time():
    """Calculates average of all response times of user"""
    try:
        total_values = -1  # -1 for header in csv
        sum_of_time = 0
        with open('est_time.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                total_values += 1
                sum_of_time += float(row['act_request_time'])

        average = sum_of_time / total_values
        return True, average
    except:
        return False

# add if csv file exists, else create them

def file_check():
    if not os.path.isfile('est_time.csv'):
        with open('est_time.csv', 'w', newline='') as file:
            fieldnames = ['act_request_time']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

    if not os.path.isfile('failed_items.csv'):
        with open('failed_items.csv', 'w', newline='') as file:
            fieldnames = [
                        'skin_name',
                        'request_count',
                        'response_code',
                        'http_status_code'
                        ]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({
                        'skin_name': 0,
                        'request_count': 0,
                        'response_code': 0,
                        'http_status_code': 0
                        })

    if not os.path.isfile('complete_results.csv'):
        with open('complete_results.csv', 'w', newline='') as file:
            fieldnames = [
                    "case_name",
                    "total_opened",
                    "total_spent",
                    "return_on_invest"
                    ]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for item in market_case_name:
                writer.writerow({
                            'case_name': item,
                            'total_opened': 0,
                            'total_spent': 0,
                            'return_on_invest': 0
                            })

    # cache.csv is created without condition, always needed empty on start.
    with open('cache.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["skin_name", "amount_of_drops"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()


def append_failed_items(skin_name, response_code, request_count):
    to_write = {}
    with open('failed_items.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if skin_name in row['skin_name'] and str(response_code) in row['response_code']:
                print("NONE")
                return None
        to_write["skin_name"] = skin_name
        to_write["response_code"] = response_code
        to_write["request_count"] = request_count

    with open('failed_items.csv', 'a', newline='', encoding='utf-8') as file:
        fieldnames = ['skin_name', 'request_count', 'response_code', 'http_status_code']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow({'skin_name': to_write['skin_name'],
                         'request_count': to_write['request_count'],
                         'response_code': to_write['response_code'],
                         'http_status_code': http_status_codes[response_code]
                    })