import csv

# writes failed requests/items into a file
def append_failed_items(skin_name, response_code, request_count):
    to_write = {}
    with open('failed_items.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if str(skin_name) == row['skin_name'] and str(response_code) == row['response_code']:
                return None
        to_write["skin_name"] = skin_name
        to_write["response_code"] = response_code
        to_write["request_count"] = request_count

    with open('failed_items.csv', 'a', newline='', encoding='utf-8') as file:
        fieldnames = ['skin_name', 'response_code', 'request_count']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow({'skin_name': to_write['skin_name'], 'response_code': to_write['response_code'], 'request_count': to_write['request_count']})
