import argparse
from pathlib import Path

from counter.counter import count_islands


def _parse_arguments(args=None):
    parser = argparse.ArgumentParser(
        description="Program counting number of islands in an ASCII file."
    )
    parser.add_argument("input", type=Path)
    parser.add_argument(
        "--version",
        "-V",
        action="version",
    )
    # Unkown arguments will be ignored
    args, _ = parser.parse_known_args(args=args)
    return args


if __name__ == "__main__":
    parsed_arguments = _parse_arguments()
    print(count_islands(parsed_arguments.input))
