import csv
length_list = []
with open('cs20_case.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        length_list.append(row['skin_name'])

print(len(length_list))