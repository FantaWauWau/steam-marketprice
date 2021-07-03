import csv


def drop_check(file_name, item):
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
        print("Error in item name")

    item_quality = ""
    with open(file_name, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['case'] == item_without_wear.strip():
                item_quality = row["quality"]

    wear_list = item_quality.split(",")

    full_item_names = []
    for wear in wear_list:
        full_item_name = item_without_wear + wear.lstrip()
        full_item_names.append(full_item_name)

    if item in full_item_names:
        return True
    return False

print(drop_check("cs20_case.csv", "Dual Berettas | Elite 1.6 (Minimal Wear)"))