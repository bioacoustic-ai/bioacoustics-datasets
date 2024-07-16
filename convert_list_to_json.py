import json
import os
from pathlib import Path
import shutil
from typing import Dict
import mlcroissant as mlc
import pandas as pd
import openpyxl
from tqdm import tqdm

from constants import DATASETS_LIST_PATH, OUTPUT_FOLDER
from retrieve_data_from_url import (
    retrieve_dryad_content,
    retrieve_figshare_content,
    retrieve_osf_content,
    retrieve_zenodo_content,
)
from utils import list_files, load_json, write_json


def _get_link_if_exists(cell) -> str | None:
    try:
        return cell.hyperlink.target
    except AttributeError:
        return None


def extract_hyperlinks_from_xlsx(
    file_name: str, sheet_name: str, columns_to_parse: list[str], row_header: int = 1
) -> pd.DataFrame:
    df = pd.read_excel(file_name, sheet_name)
    ws = openpyxl.load_workbook(file_name)[sheet_name]
    hyperlink_df = pd.DataFrame()
    for column in columns_to_parse:
        hyperlink_column_name = column + "_link"
        row_offset = row_header + 1
        column_index = list(df.columns).index(column) + 1
        hyperlink_df[hyperlink_column_name] = [
            _get_link_if_exists(ws.cell(row=row_offset + i, column=column_index))
            for i in range(len(df[column]))
        ]
    return hyperlink_df


def create_datasets_df(path: str = DATASETS_LIST_PATH) -> Dict:
    datasets_no_hyperlinks_df = pd.read_excel(DATASETS_LIST_PATH)
    hyperlinks_df = extract_hyperlinks_from_xlsx(
        path, sheet_name="Blad1", columns_to_parse=["Name", "Paper"]
    )
    datasets_df = pd.concat([datasets_no_hyperlinks_df, hyperlinks_df], axis=1)
    return datasets_df


def write_croissant_metadata(croissant_metadata: dict, file_path: str) -> None:
    """
    Taken from the croissant examples in https://github.com/mlcommons/croissant/blob/main/python/mlcroissant/recipes/introduction.ipynb
    """
    assert (
        Path(file_path).suffix == ".json"
    ), "Please provide a file path ending with .json"
    with open(file_path, "w") as f:
        content = croissant_metadata.to_json()
        content = json.dumps(content, indent=2)
        f.write(content)
        f.write("\n")  # Terminate file with newline


# TODO: see if I should convert html to plain text in the descriptions. Fix encoding
# test to see if possible to tinker with croissant
def add_custom_properties(croissant_folder: str) -> None:
    metadata_paths = list_files(croissant_folder, suffix=".json")
    for path in metadata_paths:
        metadata = load_json(path)
        metadata["sample_rate"] = 16000
        with open(path, "w") as f:
            content = json.dumps(metadata, indent=2)
            f.write(content)
            f.write(
                "\n"
            )  # Terminate file with newline # TODO: add that in a new function


def create_croissant_files(datasets_path: str, croissant_folder: str) -> str:
    if os.path.exists(croissant_folder):
        shutil.rmtree(croissant_folder)
    os.mkdir(croissant_folder)
    datasets = create_datasets_df(datasets_path).to_dict("records")
    datasets_not_on_zenodo_or_figshare = {}

    for dataset in tqdm(datasets):
        print(dataset["Name"])
        metadata = mlc.Metadata(
            name=dataset["Name"],
            cite_as=None,
            creators=None,
            url=dataset["Name_link"],
            date_published=None,
            description=None,
            license=dataset["License"],
            version=None,
        )
        url_without_redirection = (
            dataset["Name_link"]
            .removeprefix("https://www.google.com/url?q=")
            .split("&")[0]
        )

        if "zenodo" in url_without_redirection:
            metadata = retrieve_zenodo_content(url_without_redirection, metadata)
        elif "figshare" in url_without_redirection:
            metadata = retrieve_figshare_content(url_without_redirection, metadata)
        elif "osf.io" in url_without_redirection:
            metadata = retrieve_osf_content(url_without_redirection, metadata)
        elif "dryad" in url_without_redirection:
            metadata = retrieve_dryad_content(url_without_redirection, metadata)
        else:
            datasets_not_on_zenodo_or_figshare[dataset["Name"]] = dataset["Name_link"]
            continue

        metadata_file_path = os.path.join(croissant_folder, f"{metadata.name}.json")
        write_croissant_metadata(
            croissant_metadata=metadata, file_path=metadata_file_path
        )
    write_json(
        path=os.path.join(OUTPUT_FOLDER, "datasets_not_done.json"),
        data=datasets_not_on_zenodo_or_figshare,
    )

    add_custom_properties(
        croissant_folder=croissant_folder
    )  # do that for a path instead


if __name__ == "__main__":
    create_croissant_files(
        datasets_path=DATASETS_LIST_PATH, croissant_folder=OUTPUT_FOLDER
    )
