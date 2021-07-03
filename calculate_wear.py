import random
import csv
from drop_check import drop_check

def calculate_wear(case_name: str, quality: str, amount: int) -> None:
    """Takes skins quality (color) and drop amount as arguments and calculates/writes skin_names_by_quality in csv file"""
    # creates a list of dictionaries with content of csv file (opened case name)
    item_list = []
    with open(case_name, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            item_list.append(row)

    # removes every dictionary from item_list which doesn't match the passed quality
    items_by_quality = [item for item in item_list if item['quality'] == quality]

    # creates a list with all skin names of quality x
    all_skin_names_by_quality = []
    for item in range(0, len(items_by_quality)):
        skin_name = items_by_quality[item]['skin_name']
        all_skin_names_by_quality.append(skin_name)

    # picks random skin names for total amount of drops of quality x
    skin_names_by_quality = []
    for i in range(amount):
        random_skin_name = random.choice(all_skin_names_by_quality)
        skin_names_by_quality.append(random_skin_name)

    # initializes dictionary with skin name and wear as key and drop count as value
    global skin_name_with_wear
    skin_name_with_wear = {}
    for skin_name in skin_names_by_quality:
        skin_name_with_wear[skin_name + " (Battle-Scarred)"] = 0
        skin_name_with_wear[skin_name + " (Well-Worn)"] = 0
        skin_name_with_wear[skin_name + " (Field-Tested)"] = 0
        skin_name_with_wear[skin_name + " (Minimal Wear)"] = 0
        skin_name_with_wear[skin_name + " (Factory New)"] = 0

    # loops through skin names, calculates wear and checks if skin name with wear exists in current csv file (case)
    # if skin exists drop count is raised by 1
    for item in skin_names_by_quality:
        float = random.uniform(0, 1)
        while True:
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

    # writes result into cache.csv 
    with open('cache.csv', 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['skin_name', 'amount_of_skin_names_by_quality']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for skin_name, amount in skin_name_with_wear.items():
            writer.writerow({'skin_name': skin_name, 'amount_of_skin_names_by_quality': amount})
