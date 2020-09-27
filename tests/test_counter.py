import pytest

from counter.utils import Map, count_islands

MAPS_TO_COUNT = [
    (
        "000000000\n"
        "010000000\n"
        "111000100\n"
        "110001110\n"
        "000001100\n"
        "001000000\n"
        "110000000\n"
        "000001100\n",
        4,
    ),
    (
        "000000000\n"
        "010000000\n"
        "111000100\n"
        "110001110\n"
        "000001100\n"
        "001000000\n"
        "110000000\n"
        "000001100",
        4,
    ),
    ("000", 0),
    ("", 0),
    ("01010101", 4),
    ("110011", 2),
    ("110011\n" "110100\n" "101001", 2),
    ("00000\n" "00000\n" "00000\n", 0),
    ("1000\n" "0100\n" "0010\n" "0001", 1),
]


@pytest.mark.parametrize(
    "unix_newline_filepath, expected_islands_count",
    [*MAPS_TO_COUNT],
    indirect=["unix_newline_filepath"],
)
def test_counting_islands(unix_newline_filepath, expected_islands_count):
    with open(unix_newline_filepath, mode="r+", encoding="ascii", newline=None) as f:
        map = Map.from_file(f)
        assert expected_islands_count == count_islands(map)


@pytest.mark.parametrize("filepath_to_huge", [(30, 30)], indirect=["filepath_to_huge"])
def test_huge_map_counting(filepath_to_huge):
    with open(filepath_to_huge, mode="r+", encoding="ascii") as f:
        map = Map.from_file(f)
        assert 30 * 30 * 4 == count_islands(map)
