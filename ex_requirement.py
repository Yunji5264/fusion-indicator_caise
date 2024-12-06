from class_requirement import *

def def_requirement():
    spatial_granularity = Req_Spatial_Granularity("DEPARTEMENT")

    spatial_scope = Req_Spatial_Scope("REGION", [75, 76, 44, 84,])

    space = Req_Space(spatial_granularity, spatial_scope)

    temporal_granularity = Req_Temporal_Granularity("YEAR")

    temporal_scope = Req_Temporal_Scope("YEAR", "2015", "2021")

    time = Req_Time(temporal_granularity, temporal_scope)

    space_time = Req_Space_Time(space, time)

    themes = ["Environment/Opportunities to acquire new information and skills", "Physical Health"]
    # 转换 themes 列表为 Req_Theme 对象列表
    req_themes = []

    for theme_path in themes:
        # 创建 Req_Theme 对象
        req_themes.append(Req_Theme(theme_path, theme_path))

    requirement = Requirement(space_time, req_themes)

    requirement_dict = requirement.to_dict()
    print("Requirement as dictionary:")
    print(json.dumps(requirement_dict, indent=4, ensure_ascii=False))

    # Save to JSON file
    requirement.save_to_json(r'C:\Users\ADMrechbay20\Documents\experimentation_CAiSE\requirement_metadata.json')

    # # Get Requirement from JSON file
    # loaded_requirement = Requirement.load_from_json("requirement.json")
    # print("\nLoaded Requirement from JSON:")
    # print(json.dumps(loaded_requirement.to_dict(), indent=4, ensure_ascii=False))

    return requirement
