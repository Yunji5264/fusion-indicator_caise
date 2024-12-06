from ex_requirement import *
from filter_raw import filter_datasets
from get_raw import *

if __name__ == "__main__":
    requirement = def_requirement()
    raw_datasets = load_datasets_from_json()
    existing_indicators = filter_datasets(requirement, raw_datasets)
    for ei in existing_indicators:
        ei.save_to_json(r'C:\Users\ADMrechbay20\Documents\experimentation_CAiSE\indicators_metadata.json')

    # relevant_datasets = [ei.sourceDataset for ei in existing_indicator]



    # print("Relevant Datasets:")
    # print(json.dumps([ds.to_dict() for ds in relevant_datasets], indent=4, ensure_ascii=False))