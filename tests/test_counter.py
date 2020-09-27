import pytest

from counter.counter import Map, count_islands

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
    "file, expected_islands_count", [*MAPS_TO_COUNT], indirect=["file"]
)
def test_counting_islands(file, expected_islands_count):
    with open(file, mode="r+", encoding="ascii", newline=None) as f:
        map = Map.from_file(f)
        assert expected_islands_count == count_islands(map)


@pytest.mark.parametrize("huge_file", [], indirect=["huge_file"])
def test_huge_map_counting(huge_file, rows, columns):
    with open(huge_file, mode="r+", encoding="ascii", newline=None) as f:
        map = Map.from_file(f)

        assert 120 * 120 * 4 == count_islands(map)
