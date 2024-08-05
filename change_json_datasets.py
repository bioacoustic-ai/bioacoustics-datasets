from pathlib import Path
from typing import Union

from utils import load_json, write_json

JSON_FOLDER = Path().resolve() / "datasets_json"


def change_nan_to_empty_string(filepath: Union[str, Path]) -> None:
    dataset = load_json(filepath)
    for k in dataset.keys():
        if dataset[k] == "NaN":
            dataset[k] = ""
    write_json(filepath, dataset)


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
        modifier_function(dataset_path)


if __name__ == "__main__":
    change_json_datasets(JSON_FOLDER)
