import glob
import json
import os
from typing import List


class CroissantFieldsMetadata:
    def __init__(
        self,
        name: str = None,
        cite_as: str = None,
        creators: List[str] = None,
        url: str = None,
        date_published: str = None,
        description: str = None,
        license: str = None,
        version: str | int = None,
    ) -> None:
        self.name = name
        self.cite_as = cite_as
        self.creators = creators
        self.url = url
        self.date_published = date_published
        self.description = description
        self.license = license
        self.version = version


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
        json.dump(data, f, indent=2, sort_keys=True)
