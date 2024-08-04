import json
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List

import html2text
import mlcroissant as mlc
import openpyxl
import pandas as pd
from tqdm import tqdm

from constants import DATASETS_LIST_PATH, OUTPUT_FOLDER
from retrieve_data_from_url import (
    retrieve_dryad_content,
    retrieve_figshare_content,
    retrieve_osf_content,
    retrieve_zenodo_content,
)
from utils import CroissantFieldsMetadata, load_json, write_json


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


def write_croissant_metadata(croissant_metadata: mlc.Metadata, file_path: str) -> None:
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


def create_datasets_metadata_from_table(
    datasets_path: str, output_folder: str, use_croissant_format: bool = False
) -> str:
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.mkdir(output_folder)
    datasets: List[Dict] = create_datasets_df(datasets_path).to_dict("records")
    datasets_not_available_with_api = {}

    for dataset in tqdm(datasets):
        print(dataset["Name"])
        del dataset["Paper"]
        metadata = CroissantFieldsMetadata(
            name=dataset.pop("Name"),
            url=dataset.pop("Name_link"),
            license=dataset.pop("License"),
        )
        url_without_redirection = metadata.url.removeprefix(
            "https://www.google.com/url?q="
        ).split("&")[0]

        if "zenodo" in url_without_redirection:
            metadata = retrieve_zenodo_content(url_without_redirection, metadata)
        elif "figshare" in url_without_redirection:
            metadata = retrieve_figshare_content(url_without_redirection, metadata)
        elif "osf.io" in url_without_redirection:
            metadata = retrieve_osf_content(url_without_redirection, metadata)
        elif "dryad" in url_without_redirection:
            metadata = retrieve_dryad_content(url_without_redirection, metadata)
        else:
            datasets_not_available_with_api[metadata.name] = metadata.url

        metadata.description = (
            html2text.html2text(metadata.description) if metadata.description else None
        )
        metadata_output_file_path = os.path.join(output_folder, f"{metadata.name}.json")

        if use_croissant_format:
            croissant_metadata = mlc.Metadata(
                name=metadata.name,
                cite_as=metadata.cite_as,
                creators=(
                    [
                        mlc.Person(name=creator_name)
                        for creator_name in metadata.creators
                    ]
                    if metadata.creators
                    else None
                ),
                url=metadata.url,
                date_published=metadata.date_published,
                description=metadata.description,
                license=metadata.license,
                version=metadata.version,
            )
            croissant_metadata.date_published = (
                datetime.isoformat(croissant_metadata.date_published)
                if croissant_metadata.date_published
                else None
            )  # the croissant package automatically converts the published date to datetime.datetime, which is not json serialisable
            write_croissant_metadata(
                croissant_metadata=croissant_metadata,
                file_path=metadata_output_file_path,
            )
            metadata = load_json(metadata_output_file_path)
        else:
            metadata = vars(metadata)

        # more readable in the final JSON
        dataset = dict((k.lower(), v) for k, v in dataset.items())

        metadata.update(dataset)
        write_json(data=metadata, path=metadata_output_file_path)

    write_json(
        path=os.path.join(OUTPUT_FOLDER, "datasets_without_croissant_fields.json"),
        data=datasets_not_available_with_api,
    )


if __name__ == "__main__":
    create_datasets_metadata_from_table(
        datasets_path=DATASETS_LIST_PATH,
        output_folder=OUTPUT_FOLDER,
        use_croissant_format=False,
    )
