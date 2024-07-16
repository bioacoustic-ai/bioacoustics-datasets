import json
import mlcroissant as mlc
import requests
import urllib.parse


def _get_metadata_from_url(url: str) -> dict:
    r = requests.get(url)
    # Load the metadata as JSON
    if r.status_code != 200:
        print("Something is wrong:", r.content)
    else:
        metadata = json.loads(r.text)
    return metadata


def retrieve_figshare_content(
    url: str, croissant_metadata: mlc.Metadata
) -> mlc.Metadata:
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
    # croissant_metadata.name = html2text.html2text(dataset_info["title"])
    croissant_metadata.cite_as = dataset_info["citation"]
    croissant_metadata.creators = [
        mlc.Person(name=dataset_info["authors"][i]["full_name"])
        for i in range(len(dataset_info["authors"]))
    ]
    croissant_metadata.url = dataset_info.get("figshare_url", url)
    croissant_metadata.date_published = dataset_info["created_date"]
    croissant_metadata.description = dataset_info["description"]
    license_info = dataset_info.get("license")
    if license_info:
        croissant_metadata.license = license_info["url"]
    croissant_metadata.version = dataset_info["version"]
    return croissant_metadata


def retrieve_zenodo_content(
    url: str,
    croissant_metadata: mlc.Metadata,
) -> mlc.Metadata:
    base_url = "https://zenodo.org"
    item_id = url.split("/")[-1]
    item_url_path = "/records/" + str(item_id)
    url_api = base_url + "/api/" + item_url_path
    dataset_info = _get_metadata_from_url(url_api)
    dataset_metadata = dataset_info["metadata"]
    # croissant_metadata.name = html2text.html2text(dataset_metadata["title"])
    croissant_metadata.creators = [
        mlc.Person(name=dataset_metadata["creators"][i]["name"])
        for i in range(len(dataset_metadata["creators"]))
    ]
    croissant_metadata.url = base_url + item_url_path
    croissant_metadata.date_published = dataset_info[
        "created"
    ]  # because each record is linked to one version in zenodo
    croissant_metadata.description = dataset_metadata.get("description", None)
    croissant_metadata.license = dataset_metadata["license"][
        "id"
    ]  # TODO: put url instead as recommended by croissant
    croissant_metadata.version = (
        dataset_metadata["relations"]["version"][0]["index"] + 1
    )  # versions are indexed starting from 0
    return croissant_metadata


def retrieve_dryad_content(url: str, croissant_metadata: mlc.Metadata) -> mlc.Metadata:
    base_api_url = "https://datadryad.org/api/v2/datasets/"
    doi = url[url.rfind("doi:") :]
    encoded_doi = urllib.parse.quote(doi, safe="")
    dataset_info = _get_metadata_from_url(base_api_url + encoded_doi)
    authors = dataset_info["authors"]
    croissant_metadata.creators = [
        mlc.Person(name=authors[i]["firstName"] + authors[i]["lastName"])
        for i in range(len(authors))
    ]
    croissant_metadata.date_published = dataset_info["publicationDate"]
    croissant_metadata.description = dataset_info["abstract"]
    croissant_metadata.version = dataset_info["versionNumber"]
    croissant_metadata.url = dataset_info["sharingLink"]
    croissant_metadata.license = dataset_info["license"]
    return croissant_metadata


# no version number for osf content
def retrieve_osf_content(url: str, croissant_metadata: mlc.Metadata) -> mlc.Metadata:
    base_api_url = "https://api.osf.io/v2/nodes/"
    item_id = url.split("/")[3]
    dataset_info = _get_metadata_from_url(base_api_url + item_id)["data"]
    croissant_metadata.description = dataset_info["attributes"]["description"]
    croissant_metadata.date_published = dataset_info["attributes"]["date_created"]
    license_data = dataset_info["relationships"].get("license")
    if license_data:
        license_info = _get_metadata_from_url(license_data["links"]["related"]["href"])
        croissant_metadata.license = license_info["data"]["attributes"]["url"]
    authors_info = _get_metadata_from_url(
        dataset_info["relationships"]["contributors"]["links"]["related"]["href"]
    )["data"]

    croissant_metadata.creators = [
        mlc.Person(
            name=authors_info[i]["embeds"]["users"]["data"]["attributes"]["full_name"]
        )
        for i in range(len(authors_info))
    ]
    croissant_metadata.url = dataset_info["links"]["html"]
    return croissant_metadata
