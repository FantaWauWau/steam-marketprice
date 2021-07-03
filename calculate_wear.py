import random
import csv
from drop_check import drop_check

def calculate_wear(case_name: str, quality: str, amount: int) -> None:
    """Takes skins quality (color) and drop amount as arguments and calculates/writes drops in csv file"""
    item_list = []
    with open(case_name, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            item_list.append(row)

    items_by_quality = [item for item in item_list if item['type'] == quality]
    listed = []
    for item in range(0, len(items_by_quality)):
        items_names = items_by_quality[item]['case']
        listed.append(items_names)

    drops = []
    for i in range(amount):
        dropped = random.choice(listed)
        drops.append(dropped)
    global wear
    wear = {}
    for i in drops:
        wear[i + " (Battle-Scarred)"] = 0
        wear[i + " (Well-Worn)"] = 0
        wear[i + " (Field-Tested)"] = 0
        wear[i + " (Minimal Wear)"] = 0
        wear[i + " (Factory New)"] = 0

    for item in drops:
        float = random.uniform(0, 1)
        while True:
            if 1 > float >= 0.45:
                if drop_check(case_name, item + " (Battle-Scarred)"):
                    wear[item + " (Battle-Scarred)"] += 1
                    break
                else:
                    continue
            elif 0.45 > float >= 0.38:
                if drop_check(case_name, item + " (Well-Worn)"):
                    wear[item + " (Well-Worn)"] += 1
                    break
                else:
                    continue
            elif 0.38 > float >= 0.15:
                if drop_check(case_name, item + " (Field-Tested)"):
                    wear[item + " (Field-Tested)"] += 1
                    break
                else:
                    continue
            elif 0.15 > float >= 0.07:
                if drop_check(case_name, item + " (Minimal Wear)"):
                    wear[item + " (Minimal Wear)"] += 1
                    break
                else:
                    continue
            else:
                if drop_check(case_name, item + " (Factory New)"):
                    wear[item + " (Factory New)"] += 1
                    break
                else:
                    continue

    with open('cache.csv', 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['key', 'value']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for key, value in wear.items():
            writer.writerow({'key': key, 'value': value})
