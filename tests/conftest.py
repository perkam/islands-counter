import os
from tempfile import NamedTemporaryFile

import pytest


@pytest.fixture
def unix_newline_filepath(request):
    f = NamedTemporaryFile(delete=False, mode="w", encoding="ascii", newline="\n")
    f.write(request.param)
    f.close()
    yield f.name
    os.unlink(f.name)


@pytest.fixture
def windows_newline_filepath(request):
    f = NamedTemporaryFile(delete=False, mode="w", encoding="utf-8", newline="\r\n")
    f.write(request.param)
    f.close()
    yield f.name
    os.unlink(f.name)


@pytest.fixture
def filepath_to_huge(request):
    ROWS = request.param[0]
    COLS = request.param[1]
    section = [
        "000000000",
        "010000000",
        "111000100",
        "110001110",
        "000001100",
        "001000000",
        "110000000",
        "000001100",
    ]
    f = NamedTemporaryFile(delete=False, mode="w", encoding="ascii", newline="\n")
    for i in range(ROWS):
        for k in range(len(section)):
            for j in range(COLS):
                f.write(section[k])
            f.write("\n")
    f.close()
    yield f.name
    os.unlink(f.name)
