import csv

# dictionary for formatting case name for price request to steam
market_case_name = {
    "cs20_case.csv": "CS20 Case",
    "csgo_weapon_case.csv": "CS:GO Weapon Case"
}

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
        print(f"Failed to format {item}! \n"
              "Script can't be executed anymore...")
        quit()

    item_wear = ""
    try:
        with open(case_name, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['skin_name'] == item_without_wear.strip():
                    item_wear = row["wear"]
    except FileNotFoundError:
        print(FileNotFoundError)
        quit()
    wear_list = item_wear.split(",")
    # builds item_name with all availables wears and adds them into a list
    full_item_names = []
    for wear in wear_list:
        full_item_name = item_without_wear + wear.lstrip()
        full_item_names.append(full_item_name)

    # function paramater (item) is checked if it exists in list with all available item + wears.
    if item in full_item_names:
        return True
    return False


def vanilla_check(skin_name: str):
    """Checks if skins is a vanilla knife.

    Args:
        skin_name: name of skin to check, with wear.
    Returns:
        Tuple of True and skin name without wear if skin is vanilla.
        False if the skin is not a vanilla.
    """
    with open("vanilla_knife.csv", "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if skin_name == row["skin_name"]:
                vanilla_name = row["vanilla_name"]
                return True, vanilla_name # wear is removed from string
        return False
