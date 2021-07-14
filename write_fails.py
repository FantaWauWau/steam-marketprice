import csv
from http_codes import http_status_codes

# writes failed requests/items into a file
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
