import csv
import json
import argparse
import os

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

def import_json_to_csv(json_file_path, csv_file_path):
    # Завантаження даних з файлу JSON
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    # Отримання заголовків стовпців з першого запису
    headers = list(data[0].keys())

    # Запис даних у файл CSV
    with open(csv_file_path, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers)

        # Запис заголовків стовпців
        writer.writeheader()

        # Запис даних
        writer.writerows(data)

# csv_file = 'csv_data.csv'
# json_file = 'json_data.json'

# convert_csv_to_json(csv_file, json_file)

parser = argparse.ArgumentParser()

# Positional

parser.add_argument("input", type=str, help="Path to input file")
# C:\Users\roman\PycharmProjects\FileConvertor\csv_data.csv
parser.add_argument("output", type=str, help="Path to output file")
# C:\Users\roman\PycharmProjects\FileConvertor\json_data.json

# Optional

parser.add_argument("-p", "--parents", type=bool, help="if parents is true, any missing parents of output path are created as needed", default=False)

args = parser.parse_args()

intput_path = args.input
output_path = args.output

input_file_extension = intput_path.split('.')[-1].lower()
output_file_extension = output_path.split('.')[-1].lower()

if input_file_extension == output_file_extension:
    raise ValueError("input file format is the same as the output file format")

if args.parents == True:
    # Створення відсутніх батьківських каталогів
    os.makedirs(os.path.dirname(output_path))

if input_file_extension == "csv":
    convert_csv_to_json(intput_path, output_path)

elif input_file_extension == "json":
    import_json_to_csv(intput_path, output_path)

else:
    print("Unsupported file format")

# python main.py csv_data.csv D:\Trash\JsonTrash\result.json
# python main.py json_data.json D:\Trash\result.csv
# python main.py json_data.json D:\Trash\TrashCsv\result.csv
# python main.py json_data.json D:\Trash\TrashCsv\result.json
# python main.py csv_data.csv D:\Trash\JsonTrash\DeleteMe\result.json -p True

# print(args)