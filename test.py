def steam_request(item_name, amount):
    """Sents request to steam for item price.

    Returns:
        True, price * amount
        False, http response code.
    """
    response = requests.get("https://steamcommunity.com/market/priceoverview/?"
                            "appid=730&currency=1&market_hash_name=" + item_name)

    try:
        steam_response = response.json()
    except:
        return False, response.status_code

    try:
        if "lowest_price" in steam_response:
            formatted_price = steam_response["lowest_price"][1:]  # remove $
        elif "median_price" in steam_response:
            formatted_price = steam_response["median_price"][1:]
        if "," in formatted_price:
            return True, float(locale.atof(formatted_price) * float(amount))
        else:
            return True, float(formatted_price) * float(amount)
    except:
        return False, response.status_code