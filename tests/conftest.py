import os
from pathlib import Path
from tempfile import NamedTemporaryFile

import pytest


@pytest.fixture
def file(request):
    f = NamedTemporaryFile(delete=False, mode="w", encoding="ascii", newline="\r\n")
    f.write(request.param)
    f.close()
    yield f.name
    os.unlink(f.name)


@pytest.fixture
def huge_file():
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
    f = NamedTemporaryFile(delete=False, mode="w", encoding="ascii", newline="\r\n")
    for i in range(120):
        for k in range(len(section)):
            for j in range(120):
                f.write(section[k])
            f.write("\n")
    f.close()
    p = Path(f.name)
    print(p.stat().st_size)
    print(f.name)
    yield f.name
    os.unlink(f.name)
