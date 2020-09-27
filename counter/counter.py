import collections

from counter.map import FieldType, Map, MapField


def remove_island(field: MapField, map: Map):
    """
    Remove island to which given field belongs from given map.
    :param field: Field that belongs to the island that we want to remove
    :param map: map to which given field belongs to
    """
    # field = ((x: int, y: int), type: FieldType)
    # Do BFS in order to traverse whole island
    visited = set()
    queue = collections.deque([field])
    while queue:
        current_field = queue.popleft()
        # Change land to water in place in order to not visit it anymore in the future
        map.change_field_type(field=current_field, type=FieldType.WATER)
        visited.add(current_field)
        queue.extend(
            n
            for n in map.get_neighbours(current_field)
            if n not in visited and n.type is FieldType.LAND
        )


def count_islands(map: Map) -> int:
    islands_count = 0
    for field in map:
        if field.type is FieldType.LAND:
            remove_island(field, map)
            islands_count += 1
    return islands_count
