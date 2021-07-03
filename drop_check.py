import csv


def drop_check(case_name: str, item: str) -> bool:
    """Checks if item exists. Because not every item has all wears."""
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
        print("Error in item name")

    item_wear = ""
    with open(case_name, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['skin_name'] == item_without_wear.strip():
                item_wear = row["wear"]

    wear_list = item_wear.split(",")

    full_item_names = []
    for wear in wear_list:
        full_item_name = item_without_wear + wear.lstrip()
        full_item_names.append(full_item_name)

    if item in full_item_names:
        return True
    return False
