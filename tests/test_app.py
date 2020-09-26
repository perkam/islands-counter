from pathlib import Path
from typing import List

import pytest

from counter.app import _parse_arguments


@pytest.mark.parametrize("additional_argvs", [["./bla", "--additional", "--hey"]])
def test_argument_parsing_with_additional_args(additional_argvs: List):
    parsed_args = _parse_arguments(additional_argvs)
    assert parsed_args.input == Path("./bla")


@pytest.mark.parametrize("additional_argvs", [["--additional", "-ver"]])
def test_argument_parsing_without_input_fails(additional_argvs):
    with pytest.raises(SystemExit):
        _parse_arguments(additional_argvs)
