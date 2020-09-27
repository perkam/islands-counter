# Task

Python program that counts islands inside a text file.

# Requirements

To run the program:
* python 3.7+

To run the tests:
* pytest=6.1.0
* pip 20+

# Setup
In order to install `pytest` run:

`pip install -r requirements.txt`

# Usage

`count_islands.sh <path_to_input_file> <--duplicate>`

Use `--duplicate` option in order to run algorithm on a copy of input file. During the execution given file is modified so it is strongly advised if we want to reuse the file.

Example usage on small test file:
``` bash
./count_islands.sh ./tests/test_small.txt --duplicate
```

# Run tests:
`python3 -m pytest`
