import json
from pathlib import Path
from typing import Dict, List, Union

from get_webpage_content import (
    retrieve_dryad_content,
    retrieve_figshare_content,
    retrieve_osf_content,
    retrieve_zenodo_content,
)

JSON_FOLDER = Path().resolve() / "datasets_json"


def load_json(path: str) -> Dict:
    with open(path, "r") as f:
        data = json.load(f)
    return data


def write_json(path: str, data) -> None:
    with open(path, "w") as f:
        json.dump(data, f, indent=2, sort_keys=True)


def change_nan_to_empty_string(filepath: Union[str, Path]) -> Dict:
    dataset = load_json(filepath)
    for k in dataset.keys():
        if dataset[k] == "NaN":
            dataset[k] = ""
    return dataset


def delete_keys(
    filepath: Path, keys_to_delete: List[str] = ["citeAs", "species"]
) -> Dict:
    dataset = load_json(filepath)
    for k in keys_to_delete:
        dataset.pop(k)
    return dataset


def add_complete_title(filepath: Path) -> Dict:
    dataset = load_json(filepath)
    url = dataset["url"]
    field_name = "title"
    if "zenodo" in url:
        metadata = retrieve_zenodo_content(url)
        dataset[field_name] = metadata["title"]
    elif "figshare" in url:
        metadata = retrieve_figshare_content(url)
        dataset[field_name] = metadata["resource_title"]
    elif "osf.io" in url:
        metadata = retrieve_osf_content(url)
        dataset[field_name] = metadata["attributes"]["title"]
    elif "dryad" in url:
        metadata = retrieve_dryad_content(url)
        dataset[field_name] = metadata["title"]
    else:
        dataset[field_name] = ""
    return dataset


def change_json_datasets(
    datasets_folder: Path, modifier_function=change_nan_to_empty_string
) -> None:
    """
    :param datasets_folder: folder where the datasets are located
    :param modifier_function: function that will be applied to each dataset file path. This function should take a dataset
    file path as input, and modify it and write it in its body.
    """
    file_paths = list(datasets_folder.glob("*.json"))
    for dataset_path in file_paths:
        dataset = modifier_function(dataset_path)
        write_json(
            dataset_path,
            dataset,
        )


if __name__ == "__main__":
    change_json_datasets(JSON_FOLDER, modifier_function=add_complete_title)
