import csv
import json
import yaml
import argparse
from pathlib import Path
from enum import StrEnum


class FileFormat(StrEnum):
    CSV = '.csv'
    JSON = '.json'
    YAML = '.yaml'


def convert_file(input_file: Path, output_file: Path, input_format: str, output_format: str):
    # Input file format specification
    if input_format == FileFormat.JSON:
        with open(input_file, 'r') as file:
            data = json.load(file)

    elif input_format == FileFormat.CSV:
        with open(input_file, 'r') as file:
            reader = csv.DictReader(file)
            data = [row for row in reader]

    elif input_format == FileFormat.YAML:
        with open(input_file, 'r') as file:
            data = yaml.safe_load(file)

    else:
        print('Unsupported input format')
        return

    # Convert data to the original format
    if output_format == FileFormat.JSON:
        with open(output_file, 'w') as file:
            json.dump(data, file, indent=4)

    elif output_format == FileFormat.CSV:
        headers = list(data[0].keys())
        with open(output_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            for row in data:
                writer.writerow(list(row.values()))

    elif output_format == FileFormat.YAML:
        with open(output_file, 'w') as file:
            yaml.dump(data, file)

    else:
        print('Unsupported output format')
        return

    print('Conversion completed successfully')


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

    convert_file(intput_path, output_path, input_file_extension, output_file_extension)

    # if input_file_extension == FileFormat.CSV:
    #     convert_csv_to_json(intput_path, output_path)
    #
    # elif input_file_extension == FileFormat.JSON:
    #     import_json_to_csv(intput_path, output_path)
    #
    # else:
    #     print("Unsupported file format")
    #     return


if __name__ == '__main__':
    main()
