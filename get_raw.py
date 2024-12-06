import json
from class_dataset import *

def load_datasets_from_json():
    """
    Load raw datasets metadata from a JSON file.

    Parameters:
        file_path (str): Path to the JSON file.

    Returns:
        list: A list of raw dataset metadata dictionaries.
    """
    with open(r'C:\Users\ADMrechbay20\Documents\experimentation_CAiSE\raw_data_metadata.json', 'r', encoding='utf-8') as f:
        datasets = json.load(f)
    return [Dataset.from_dict(dataset) for dataset in datasets]
