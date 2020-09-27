import argparse
import os
import shutil
from pathlib import Path

from counter.map import Map
from counter.utils import count_islands


def _parse_arguments(args=None):
    parser = argparse.ArgumentParser(
        description="Program counting number of islands in a text file."
    )
    parser.add_argument("input", type=Path, help="Input path to file containing map.")
    parser.add_argument(
        "--encoding",
        type=str,
        default="ascii",
        help="Encoding of the file. Default: ASCII",
    )
    parser.add_argument(
        "--duplicate",
        action="store_true",
        help="should the file be duplicated before working on it. Without using it the file passed to the program will be modified and all the islands will be removed during the execution.",
    )
    # Unkown arguments will be ignored
    args, _ = parser.parse_known_args(args=args)
    return args


def __duplicate_file(path: Path):
    temp_path = str(path) + ".copy"
    return shutil.copy2(path, temp_path)


if __name__ == "__main__":
    parsed_arguments = _parse_arguments()
    input_filepath = parsed_arguments.input
    if parsed_arguments.duplicate:
        input_filepath = __duplicate_file(parsed_arguments.input)

    with open(input_filepath, mode="r+", encoding=parsed_arguments.encoding) as file:
        map = Map.from_file(file)  # type: ignore
        print(count_islands(map))

    if parsed_arguments.duplicate:
        os.unlink(input_filepath)
