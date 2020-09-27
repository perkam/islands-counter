import abc
from abc import ABC
from dataclasses import dataclass
from enum import Enum
from io import TextIOWrapper
from typing import List


class FieldType(Enum):
    WATER = 0
    LAND = 1


@dataclass(frozen=True)
class MapField:
    """
    Class for holding information about map field.
    """

    x: int
    y: int
    type: FieldType


class MapContent(ABC):
    """
    MapContent holds all the fields in the map
    """

    @abc.abstractmethod
    def seek(self, x: int, y: int):
        """
        Seek map field at position (x, y)
        :param x: row index starting at 0
        :param y: column index starting at 0
        :return: Found MapField
        :raises: ColumnIndexError - when trying ro read out of bounds of the row
        :raises: RowIndexError - when trying to read after the last row
        """

    @abc.abstractmethod
    def write(self, x: int, y: int, field: FieldType):
        """
        Write value of field type at given position
        :param x: row index starting at 0
        :param y: column index starting at 0
        :param field: FieldType which value should be written at given position
        """


class ColumnIndexError(Exception):
    """
    Thrown when trying ro read out of bounds of the row
    """


class RowIndexError(Exception):
    """
    Thrown when trying to read after the last row
    """


class FileContent(MapContent):
    def __init__(self, file: TextIOWrapper):
        """
        Create new FileContent object using open file.
        :param file: Open file
        """
        self.__file = file
        self.__row_length = self.__find_row_length()

    def seek(self, x: int, y: int):
        """
        Find and return MapField at given position.
        :param x: row
        :param y: column
        :return: Found MapField
        :raises: ColumnIndexError, RowIndexError
        """
        # if y is equal to row length it is either new line character or empty string because we got to the end of a line
        #
        if y > self.__row_length:
            raise ColumnIndexError
        offset = x * self.__row_length + y
        self.__file.seek(offset)
        c = self.__file.read(1)
        self.__file.seek(0)
        # If EOF raise seek to the beginning and raise RowIndexError
        if c == "":
            raise RowIndexError
        # If end of row raise ColumnIndexError
        elif c == "\n" or c == "\r":
            raise ColumnIndexError
        else:
            return MapField(x=x, y=y, type=FieldType(int(c)))

    def write(self, x: int, y: int, type: FieldType):
        """
        Write given FieldType at given (x,y) position
        """
        # We can only write ONE CHARACTER
        offset = x * self.__row_length + y
        self.__file.seek(offset)
        self.__file.write(str(type.value))

    def __find_row_length(self):
        i = 0
        newline_found = False
        # Find newline position
        while True:
            c = self.__file.read(1)
            if c == "\n" or c == "\r":
                # We have found newline characters. Now we only need to count all of them and break.
                newline_found = True
            elif c == "":
                return i
            else:

                if newline_found:
                    break
            i += 1
        return i


class Map(object):
    def __init__(self, content: MapContent):
        self.__x = 1
        self.__y = 1
        self.__content = content

    @staticmethod
    def from_file(file: TextIOWrapper) -> "Map":
        """
        Create map from given file
        :param file: open file
        :return: new Map
        """
        if file.closed:
            raise ValueError("Creation of Map from closed file.")
        if "r+" not in file.mode:
            raise ValueError(
                "File used for map creation has to be open in 'r+' mode in order to write and read, and not in"
                " '%s' mode" % file.mode
            )
        # Because \r\n is automatically converted to \n if using translation of the newline (that is the default mode)
        # we have to reconfigure the stream in order not to use the translation. Otherwise \r\n will be treated as ONE
        # CHARACTER when using file.read() but TWO BYTES when using file.seek()
        file.reconfigure(newline="")
        return Map(FileContent(file))

    def at(self, x: int, y: int) -> MapField:
        """
        Return map field at given position.
        :param x: index x
        :param y: index y
        :return: MapField with given position
        """
        try:
            return self.__content.seek(x, y)
        except (RowIndexError, ColumnIndexError):
            raise IndexError("Index out of bounds.")

    def get_neighbours(self, field: MapField) -> List[MapField]:
        """
        Find all neighbours of given field. Neighbour is a field next to the one given.
        N N N
        N x N <-- x is given field and N are neighbours
        N N N
        :return: List of neighbours
        """
        x = field.x
        y = field.y
        neighbours_indices = [
            (x - 1, y - 1),
            (x - 1, y),
            (x - 1, y + 1),
            (x, y - 1),
            (x, y + 1),
            (x + 1, y - 1),
            (x + 1, y),
            (x + 1, y + 1),
        ]

        def __get_neighbour(x, y):
            if x < 0 or y < 0:
                return None
            try:
                return self.at(x, y)
            except IndexError:
                return None

        neighbours = [__get_neighbour(x, y) for (x, y) in neighbours_indices]
        return [n for n in neighbours if n is not None]

    def __iter__(self):
        return self

    def __next__(self):
        try:
            f = self.__content.seek(x=(self.__x - 1), y=(self.__y - 1))
            self.__y += 1
            return f
        except ColumnIndexError:
            self.__x += 1
            self.__y = 1
            return self.__next__()
        except RowIndexError:
            self.__x = 1
            self.__y = 1
            raise StopIteration

    def change_field_type(self, field: MapField, type: FieldType):
        self.__content.write(field.x, field.y, type)
