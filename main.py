import csv
import json
import argparse
from pathlib import Path
from enum import StrEnum


class FileFormat(StrEnum):
    CSV = '.csv'
    JSON = '.json'


def convert_csv_to_json(csv_file: Path, json_file: Path):
    with csv_file.open('r') as file:
        csv_data = csv.DictReader(file)
        data = [row for row in csv_data]

    with json_file.open('w') as file:
        json.dump(data, file, indent=4)


def import_json_to_csv(json_file_path: Path, csv_file_path: Path):
    # Loading data from a JSON file
    with json_file_path.open('r') as json_file:
        data = json.load(json_file)

    # Getting column headers from the first record
    try:
        headers = list(data[0].keys())
    except IndexError:
        print("Input file is empty")
        return

    # Writing data to a CSV file
    with csv_file_path.open('w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers)

        # Recording column headers
        writer.writeheader()

        # Data recording
        writer.writerows(data)


def main():
    parser = argparse.ArgumentParser()

    # Positional

    parser.add_argument("input", type=str, help="Path to input file")
    parser.add_argument("output", type=str, help="Path to output file")

    # Optional

    parser.add_argument(
        "-p",
        "--parents",
        type=bool,
        help="if parents is true, any missing parents of output path are created as needed",
        default=False,
    )

    args = parser.parse_args()

    intput_path = Path(args.input)
    output_path = Path(args.output)

    input_file_extension = intput_path.suffix
    output_file_extension = output_path.suffix

    if input_file_extension == output_file_extension:
        print("input file format is the same as the output file format")
        return

    output_path.parent.mkdir(parents=args.parents, exist_ok=True)

    if input_file_extension == FileFormat.CSV:
        convert_csv_to_json(intput_path, output_path)

    elif input_file_extension == FileFormat.JSON:
        import_json_to_csv(intput_path, output_path)

    else:
        print("Unsupported file format")
        return


if __name__ == '__main__':
    main()
