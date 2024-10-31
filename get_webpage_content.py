import json
import urllib
from typing import Dict

import requests


def _get_metadata_from_url(url: str) -> Dict:
    r = requests.get(url)
    # Load the metadata as JSON
    if r.status_code != 200:
        print("Something is wrong:", r.content)
    else:
        metadata = json.loads(r.text)
    return metadata


def retrieve_figshare_content(url: str) -> Dict:
    base_api_url = "https://api.figshare.com/v2"
    url_parts = url.split("/")
    data_type = None
    if "articles" in url_parts:
        item_id = (
            url_parts[-2] if url_parts[-2].isnumeric() else url_parts[-1]
        )  # because url has shape ../item_id/version_id if the version is greater than 1
        data_type = "/articles/"
    elif "collections" in url_parts:
        data_type = "/collections/"
        item_id = url_parts[-2] if url_parts[-2].isnumeric() else url_parts[-1]

    url = base_api_url + data_type + str(item_id)
    dataset_info = _get_metadata_from_url(url)
    return dataset_info


def retrieve_zenodo_content(
    url: str,
) -> Dict:
    base_url = "https://zenodo.org"
    item_id = url.split("/")[-1]
    item_url_path = "/records/" + str(item_id)
    url_api = base_url + "/api/" + item_url_path
    dataset_info = _get_metadata_from_url(url_api)
    return dataset_info


def retrieve_dryad_content(url: str) -> Dict:
    base_api_url = "https://datadryad.org/api/v2/datasets/"
    doi = url[url.rfind("doi:") :]
    encoded_doi = urllib.parse.quote(doi, safe="")
    dataset_info = _get_metadata_from_url(base_api_url + encoded_doi)
    return dataset_info


def retrieve_osf_content(url: str) -> Dict:
    base_api_url = "https://api.osf.io/v2/nodes/"
    item_id = url.split("/")[3]
    dataset_info = _get_metadata_from_url(base_api_url + item_id)["data"]
    return dataset_info
