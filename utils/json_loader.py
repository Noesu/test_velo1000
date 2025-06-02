import json
from pathlib import Path
import pytest


def load_testdata_json(filename: str) -> dict | list:
    """
    Loads a JSON file from the testdata directory.
    Skips the test if the file does not exist.

    :param filename: JSON file name located in testdata/
    :return: Parsed JSON data (dict or list)
    """
    filepath = Path("testdata") / filename
    if not filepath.exists():
        pytest.skip(f"File {filepath} not found!")
    with filepath.open(encoding="utf-8") as f:
        return json.load(f)