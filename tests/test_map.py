import pytest

from counter.map import FieldType, Map, MapField

WATER = FieldType.WATER
LAND = FieldType.LAND


MAPS_TO_TEST = [
    (
        "000\n010\n001\n" * 50,
        [WATER, WATER, WATER, WATER, LAND, WATER, WATER, WATER, LAND] * 50,
    ),
    (
        "0101\n1111\n1111",
        [WATER, LAND, WATER, LAND, LAND, LAND, LAND, LAND, LAND, LAND, LAND, LAND],
    ),
    ("0010", [WATER, WATER, LAND, WATER]),
    ("0010\n", [WATER, WATER, LAND, WATER]),
    (
        "000100000101010001\n" * 36,
        (
            [WATER] * 3
            + [LAND]
            + [WATER] * 5
            + [LAND, WATER, LAND, WATER, LAND]
            + [WATER] * 3
            + [LAND]
        )
        * 36,
    ),
]

NEIGHBOURS_TO_TEST = [
    ("000\n010\n001", (1, 1), [WATER, WATER, WATER, WATER, WATER, WATER, WATER, LAND]),
    ("0101\n1111\n1111", (0, 0), [LAND, LAND, LAND]),
    ("0010", (0, 1), [WATER, LAND]),
    ("00010\n" "01111", (0, 4), [LAND, LAND, LAND]),
    ("00010\n" "01111", (0, 3), [WATER, WATER, LAND, LAND, LAND]),
    ("00010\n" "01111", (0, 0), [WATER, WATER, LAND]),
    ("00010\n" "01111", (1, 0), [WATER, WATER, LAND]),
    ("00010\n" "01111\n" "10000", (1, 0), [WATER, WATER, LAND, LAND, WATER]),
    ("00010\n" "01111\n" "10000", (1, 4), [LAND, WATER, LAND, WATER, WATER]),
    ("00010\n" "01111\n" "10000", (2, 4), [LAND, LAND, WATER]),
]


@pytest.mark.parametrize("unix_newline_filepath", ["010\n001\n110"], indirect=True)
def test_opening_in_other_mode_fails(unix_newline_filepath):
    for mode in ("r", "w", "w+", "a+", "rb", "r+b", "wb", "w+b", "ab", "a+b"):
        with pytest.raises(
            ValueError, match="File used for map creation has to be open in"
        ):
            with open(unix_newline_filepath, mode=mode) as f:
                Map.from_file(f)


@pytest.mark.parametrize(
    "unix_newline_filepath, expected_map",
    [*MAPS_TO_TEST],
    indirect=["unix_newline_filepath"],
)
def test_iterating_over_map(unix_newline_filepath, expected_map):
    with open(unix_newline_filepath, encoding="ascii", mode="r+") as f:
        map = Map.from_file(f)
        # Extend expected map to see that the iteration is finished when elements are exhausted
        expected_map.extend([LAND, LAND, WATER, WATER])
        for expected_field, real_field in zip(expected_map, map):
            assert expected_field == real_field.type


@pytest.mark.parametrize(
    "unix_newline_filepath, expected_map",
    [*MAPS_TO_TEST],
    indirect=["unix_newline_filepath"],
)
def test_opening_with_both_utf_and_ascii_works(unix_newline_filepath, expected_map):
    for encoding in ("ascii", "utf-8"):
        with open(unix_newline_filepath, encoding=encoding, mode="r+") as f:
            map = Map.from_file(f)
            # Extend expected map to see that the iteration is finished when elements are exhausted
            expected_map.extend([LAND, LAND, WATER, WATER])
            for expected_field, real_field in zip(expected_map, map):
                assert expected_field == real_field.type


@pytest.mark.parametrize(
    "windows_newline_filepath, expected_map",
    [*MAPS_TO_TEST],
    indirect=["windows_newline_filepath"],
)
def test_iterating_over_map_with_windows_newline(
    windows_newline_filepath, expected_map
):
    with open(windows_newline_filepath, encoding="ascii", mode="r+") as f:
        map = Map.from_file(f)
        # Extend expected map to see that the iteration is finished when elements are exhausted
        expected_map.extend([LAND, LAND, WATER, WATER])
        for expected_field, real_field in zip(expected_map, map):
            assert expected_field == real_field.type


@pytest.mark.parametrize("unix_newline_filepath", [""], indirect=True)
def test_iterating_over_empty_map(unix_newline_filepath):
    with open(unix_newline_filepath, mode="r+") as f:
        map = Map.from_file(f)
        for field in map:
            raise Exception("Should not be here.")


@pytest.mark.parametrize("unix_newline_filepath", ["010\n001\n110"], indirect=True)
def test_getting_one_field(unix_newline_filepath):
    with open(unix_newline_filepath, mode="r+") as f:
        map = Map.from_file(f)
        assert MapField(0, 0, WATER) == map.at(0, 0)
        assert MapField(1, 2, LAND) == map.at(1, 2)
        assert MapField(2, 2, WATER) == map.at(2, 2)


@pytest.mark.parametrize("windows_newline_filepath", ["010\n001\n110"], indirect=True)
def test_getting_one_field_with_windows_newline(windows_newline_filepath):
    with open(windows_newline_filepath, mode="r+") as f:
        map = Map.from_file(f)
        assert MapField(0, 0, WATER) == map.at(0, 0)
        assert MapField(1, 2, LAND) == map.at(1, 2)
        assert MapField(2, 2, WATER) == map.at(2, 2)


@pytest.mark.parametrize("unix_newline_filepath", ["010\n001\n110"], indirect=True)
def test_getting_field_out_of_bounds_throws(unix_newline_filepath):
    with open(unix_newline_filepath, mode="r+") as f:
        map = Map.from_file(f)
        with pytest.raises(IndexError):
            assert map.at(0, 7)


@pytest.mark.parametrize(
    "unix_newline_filepath, xy, expected_neighbours",
    [*NEIGHBOURS_TO_TEST],
    indirect=["unix_newline_filepath"],
)
def test_neighbours_of_middle(unix_newline_filepath, xy, expected_neighbours):
    x = xy[0]
    y = xy[1]
    with open(unix_newline_filepath, mode="r+") as f:
        map = Map.from_file(f)
        f = map.at(x, y)
        assert expected_neighbours == [n.type for n in map.get_neighbours(f)]


@pytest.mark.parametrize("unix_newline_filepath", ["010\n001\n110"], indirect=True)
def test_creation_with_closed_file_fails(unix_newline_filepath):
    with pytest.raises(ValueError, match="Creation of Map from closed file."):
        f = open(unix_newline_filepath, mode="r+")
        f.close()
        Map.from_file(f)
