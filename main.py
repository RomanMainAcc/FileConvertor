import csv
import json


def convert_csv_to_json(csv_file, json_file):
    with open(csv_file, 'r') as file:
        csv_data = csv.DictReader(file)

        # data = []
        # for row in csv_data:
        #     data.append(row)
        # print(data)
        data = [row for row in csv_data]

    with open(json_file, 'w') as file:
        json.dump(data, file, indent=4)


csv_file = 'csv_data.csv'
json_file = 'json_data.json'

convert_csv_to_json(csv_file, json_file)