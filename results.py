import csv
case_name = "bravo_case"
current_results = []
add_result_list = []
total_opened = 300
total_spent = 1000
return_on_invest = 100000000

with open('complete_results.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row["case_name"] != case_name:
            current_results.append(row)
        else:
            add_result_list.append(row)

#for result in current_results:
    #print(result)


current_results.append({'case_name': case_name, 'total_opened': int(add_result_list[0]["total_opened"]) + total_opened,
'total_spent': float(add_result_list[0]["total_spent"]) + total_spent, 'return_on_invest': float(add_result_list[0]["return_on_invest"]) + return_on_invest })


with open('complete_results.csv', 'w') as csvfile:
    fieldnames = ["case_name", "total_opened", "total_spent", "return_on_invest"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in current_results:
        writer.writerow(row)