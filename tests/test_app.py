from pathlib import Path

import pytest

from counter.app import _duplicate_file, _parse_arguments


@pytest.mark.parametrize("additional_argvs", [["./bla", "--additional", "--hey"]])
def test_argument_parsing_with_additional_args(additional_argvs):
    parsed_args = _parse_arguments(additional_argvs)
    assert parsed_args.input == Path("./bla")


@pytest.mark.parametrize("additional_argvs", [["--additional", "-ver"]])
def test_argument_parsing_without_input_fails(additional_argvs):
    with pytest.raises(SystemExit):
        _parse_arguments(additional_argvs)


@pytest.mark.parametrize("unix_newline_filepath", ["010\n001\n110"], indirect=True)
def test_file_duplication(unix_newline_filepath):
    new_file = _duplicate_file(Path(unix_newline_filepath))
    with open(new_file) as f:
        duplicated = f.read()
    with open(unix_newline_filepath) as f:
        original = f.read()
    assert original == duplicated
