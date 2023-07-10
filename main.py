import csv
import json

with open('csv_data.csv', 'r') as file:
    csv_data = csv.DictReader(file)

    data = []
    for row in csv_data:
        data.append(row)
    # print(data)

with open('json_data.json', 'w') as file:
    json.dump(data, file, indent=4)
