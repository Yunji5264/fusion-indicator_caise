import json

def save_indicators_to_json(indicators, file_path):
    """
    Save a list of indicators to a JSON file.

    Parameters:
        indicators (list): List of Existing_Indicator objects.
        file_path (str): Path to the JSON file to save the data.
    """
    # Convert each indicator to a dictionary
    indicators_data = [indicator.to_dict() for indicator in indicators]

    # Write the list of dictionaries to a JSON file
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(indicators_data, f, ensure_ascii=False, indent=4)


