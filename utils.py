import os
import glob
from typing import List
import json


def list_files(root_dir: str, suffix: str) -> List:
    return glob.glob(
        os.path.join(root_dir, "**", f"*{suffix}"),
        recursive=True,
    ) + glob.glob(
        os.path.join(root_dir, "**", f"*{suffix.upper()}"),
        recursive=True,
    )


def load_json(path: str) -> dict:
    with open(path, "r") as f:
        data = json.load(f)
    return data


def write_json(path: str, data) -> None:
    with open(path, "w") as f:
        json.dump(data, f)
