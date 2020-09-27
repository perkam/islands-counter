import pytest

from counter.map import FieldType, Map, MapField

WATER = FieldType.WATER
LAND = FieldType.LAND


MAPS_TO_TEST = [
    ("000\n010\n001", [WATER, WATER, WATER, WATER, LAND, WATER, WATER, WATER, LAND]),
    (
        "0101\n1111\n1111",
        [WATER, LAND, WATER, LAND, LAND, LAND, LAND, LAND, LAND, LAND, LAND, LAND],
    ),
    ("0010", [WATER, WATER, LAND, WATER]),
    ("0010\n", [WATER, WATER, LAND, WATER]),
]

NEIGHBOURS_TO_TEST = [
    ("000\n010\n001", (1, 1), [WATER, WATER, WATER, WATER, WATER, WATER, WATER, LAND]),
    ("0101\n1111\n1111", (0, 0), [LAND, LAND, LAND]),
    ("0010", (0, 1), [WATER, LAND]),
]


@pytest.mark.parametrize("file, expected_map", [*MAPS_TO_TEST], indirect=["file"])
def test_iterating_over_map(file, expected_map):
    with open(file, encoding="ascii", newline=None) as f:
        map = Map.from_file(f)
        # Extend expected map to see that the iteration is finished when elements are exhausted
        expected_map.extend([LAND, LAND, WATER, WATER])
        for expected_field, real_field in zip(expected_map, map):
            assert expected_field == real_field.type


@pytest.mark.parametrize("file", [""], indirect=True)
def test_iterating_over_empty_map(file):
    with open(file) as f:
        map = Map.from_file(f)
        for field in map:
            raise Exception("Should not be here.")


@pytest.mark.parametrize("file", ["010\n001\n110"], indirect=True)
def test_getting_one_field(file):
    with open(file) as f:
        map = Map.from_file(f)
        assert MapField(0, 0, WATER) == map.at(0, 0)
        assert MapField(1, 2, LAND) == map.at(1, 2)


@pytest.mark.parametrize("file", ["010\n001\n110"], indirect=True)
def test_getting_field_out_of_bounds_throws(file):
    with open(file) as f:
        map = Map.from_file(f)
        with pytest.raises(IndexError):
            assert map.at(0, 7)


@pytest.mark.parametrize(
    "file, xy, expected_neighbours", [*NEIGHBOURS_TO_TEST], indirect=["file"]
)
def test_neighbours_of_middle(file, xy, expected_neighbours):
    x = xy[0]
    y = xy[1]
    with open(file, "r") as f:
        map = Map.from_file(f)
        f = map.at(x, y)
        assert expected_neighbours == [n.type for n in map.get_neighbours(f)]
