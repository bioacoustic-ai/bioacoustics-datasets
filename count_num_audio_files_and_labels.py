from typing import Tuple
import soundfile as sf

import argparse
import csv
import datetime

from utils import list_files


def extract_info_audio_files(root_dir: str, suffix=".wav") -> Tuple[int, float]:
    """
    TODO: add docstring.
    """
    total_duration_in_sec = 0
    audio_paths = list_files(root_dir, suffix)
    num_audio_files = len(audio_paths)
    for audio_path in audio_paths:
        total_duration_in_sec += sf.info(audio_path).duration
    return num_audio_files, total_duration_in_sec


def count_num_labels(root_dir: str) -> int:
    """
    TODO: add docstring. Supposes that the labels are in csv files
    """
    num_labels = 0
    csv_file_paths = list_files(root_dir, suffix=".csv")
    num_csv_files = len(csv_file_paths)

    for csv_path in csv_file_paths:
        reader = csv.reader(open(csv_path))
        num_lines = len(list(reader))  # assumes that we have one label per line
        num_labels += num_lines

    num_labels -= (
        num_csv_files  # Because the first line of the csv files are for headers
    )
    return num_labels


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dir",
        type=str,
        help="root directory where to perform the search",
        required=True,
    )
    args = parser.parse_args()
    root_dir = args.dir
    num_audio_files, duration_in_sec = extract_info_audio_files(root_dir)
    num_labels = count_num_labels(root_dir)
    print(
        f"Number of audio files in directory {root_dir} is {num_audio_files} with a total duration of {str(datetime.timedelta(seconds=duration_in_sec))} hours and {num_labels} labels"
    )
