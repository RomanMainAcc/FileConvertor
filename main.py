from abc import ABC, abstractmethod
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


class Convertor(ABC):
    @classmethod
    @abstractmethod
    def read(cls, filepath: Path) -> list[dict]:
        pass

    @classmethod
    @abstractmethod
    def write(cls, data: list[dict], filepath: Path):
        pass


class JsonConvertor(Convertor):
    @classmethod
    def read(cls, filepath: Path) -> list[dict]:
        with open(filepath, 'r') as file:
            return json.load(file)

    @classmethod
    def write(cls, data: list[dict], filepath: Path):
        with open(filepath, 'w') as file:
            json.dump(data, file, indent=4)


class CsvConvertor(Convertor):
    @classmethod
    def read(cls, filepath: Path) -> list[dict]:
        with open(filepath, 'r') as file:
            reader = csv.DictReader(file)
            return [row for row in reader]

    @classmethod
    def write(cls, data: list[dict], filepath: Path):
        try:
            headers = list(data[0].keys())
        except IndexError:
            print("Input file is empty")
            return

        with open(filepath, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            for row in data:
                writer.writerow(list(row.values()))


class YamlConvertor(Convertor):
    @classmethod
    def read(cls, filepath: Path) -> list[dict]:
        with open(filepath, 'r') as file:
            return yaml.safe_load(file)

    @classmethod
    def write(cls, data: list[dict], filepath: Path):
        with open(filepath, 'w') as file:
            yaml.dump(data, file)


CONVERTERS = {
    FileFormat.JSON: JsonConvertor(),
    FileFormat.CSV: CsvConvertor(),
    FileFormat.YAML: YamlConvertor(),
}


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.description = "Supported formats:\n     - .csv\n     - .json\n     - .yaml"

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

    input_format_convertor = CONVERTERS[input_file_extension]
    output_format_convertor = CONVERTERS[output_file_extension]

    output_format_convertor.write(input_format_convertor.read(intput_path), output_path)


if __name__ == '__main__':
    main()

