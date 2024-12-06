from class_predefine import *
from load_file import *
from class_indicator import *

def filter_datasets(requirement, datasets):
    """
    Filters raw datasets based on the given requirement.

    Parameters:
        requirement (Requirement): The requirement specifying the filtering criteria.
        datasets (list): List of raw dataset metadata dictionaries loaded from a JSON file.

    Returns:
        list: A list of datasets that match the requirement.
    """

    # Initialize the result set
    result = []

    # Extract conditions from the Requirement
    req_spatial_granularity = requirement.space_time.space.spatialGranularity.spatialGranularity
    req_spatial_scope_level = requirement.space_time.space.spatialScope.spatialScopeLevel
    req_spatial_scope = set(requirement.space_time.space.spatialScope.spatialScope)
    req_temporal_granularity = requirement.space_time.time.temporalGranularity.temporalGranularity
    req_temporal_scope_level = requirement.space_time.time.temporalScope.temporalScopeLevel
    req_temporal_start = pd.to_datetime(requirement.space_time.time.temporalScope.temporalScopeStart).date()
    req_temporal_end = pd.to_datetime(requirement.space_time.time.temporalScope.temporalScopeEnd).date()
    req_themes = {theme.themeCode for theme in requirement.themes}

    # Iterate through each dataset
    for ds in datasets:
        # Extract metadata from the dataset
        ds_filepath = ds.ingestion.sourceAddress
        print(ds_filepath)
        df= find_type(ds_filepath)
        sp_select = None
        tp_select = None
        is_date = False
        ds_ei_themes = []
        ds_ei = []

        ds_spatial_granularity = ds.space_time.space.spatialGranularity.spatialGranularity
        ds_temporal_granularity = ds.space_time.time.temporalGranularity.temporalGranularity

        for d in ds.data_content:
            # Get spatial parameter
            if hasattr(d, "spatialLevel") and d.spatialLevel == req_spatial_scope_level:
                sp_select = d.dataName
            #     Get temporal parameter
            if hasattr(d, "temporalLevel") :
                if d.temporalLevel == "DATE":
                    tp_select = d.dataName
                    is_date = True
                elif d.temporalLevel == req_temporal_scope_level:
                    tp_select = d.dataName
            if hasattr(d, "indicatorTheme"):
                ds_ei_themes.append(d.indicatorTheme)
                ds_ei.append(d)

        ds_spatial_scope = set(df[sp_select].dropna().unique())
        ds_temporal_scope = df[tp_select].dropna().unique()
        if is_date:
            # Convert temporal scope to datetime format
            ds_temporal_scope = pd.to_datetime(ds_temporal_scope, errors='coerce')  # Convert numeric/int to datetime
            ds_temporal_start = ds_temporal_scope.min()
            ds_temporal_end = ds_temporal_scope.max()
        else:
            # Handle non-date temporal levels (numeric dates or categorical values)
            # ds_temporal_start = pd.to_datetime(int(ds_temporal_scope.min()).astype(str)).date()
            # ds_temporal_end = pd.to_datetime(int(ds_temporal_scope.max()).astype(str)).date()
            try:
                ds_temporal_start = pd.to_datetime(ds_temporal_scope.min().astype(str)).date()
                ds_temporal_end = pd.to_datetime(ds_temporal_scope.max().astype(str)).date()
            except:
                ds_temporal_start = pd.to_datetime(str(int(ds_temporal_scope.min())), format = '%Y').date()
                ds_temporal_end = pd.to_datetime(str(int(ds_temporal_scope.max())), format="%Y").date()
            # match req_temporal_scope_level:
            #     case "YEAR":
            #         ds_temporal_start = pd.to_datetime(ds_temporal_start.astype(str) + "-01-01").date()
            #         ds_temporal_end = pd.to_datetime(ds_temporal_end.astype(str) + "-12-31").date()
            #     case "MONTH":
            #         ds_temporal_start = pd.to_datetime(ds_temporal_start.astype(str) + "-01").date()
            #         ds_temporal_end = pd.to_datetime(ds_temporal_end.astype(str) + "-31").date()
        ds_temporal_start = ds_temporal_start.date() if isinstance(ds_temporal_start,pd.Timestamp) else ds_temporal_start
        ds_temporal_end = ds_temporal_end.date() if isinstance(ds_temporal_end, pd.Timestamp) else ds_temporal_end
        ds_theme = ds.theme.themeCode

        # Check granularity condition
        if (spatial_granularity_mapping[ds_spatial_granularity] >= spatial_granularity_mapping[req_spatial_granularity]
                and temporal_granularity_mapping[ds_temporal_granularity] >= temporal_granularity_mapping[req_temporal_granularity]
                and ds_spatial_scope & req_spatial_scope
                and not (ds_temporal_start > req_temporal_end or ds_temporal_end < req_temporal_start)
                and (ds_theme in req_themes or set(ds_ei_themes) & req_themes)):

            for ei in ds_ei:
                # Construct Ind_Identification
                ind_identification = Ind_Identification(
                    title=ei.dataName,
                    description=ei.dataDescription
                )

                # Construct Ind_Space
                ind_space = Ind_Space(
                    spatialGranularity=Ind_Spatial_Granularity(ds_spatial_granularity),
                    spatialScope=Ind_Spatial_Scope(
                        spatialScopeLevel=ds.space_time.space.spatialScope.spatialScopeLevel,
                        spatialScope=ds.space_time.space.spatialScope.spatialScope
                    )
                )

                # Construct Ind_Time
                ind_time = Ind_Time(
                    temporalGranularity=Ind_Temporal_Granularity(ds_temporal_granularity),
                    temporalScope=Ind_Temporal_Scope(
                        temporalScopeLevel=ds.space_time.time.temporalScope.temporalScopeLevel,
                        temporalScopeStart=ds.space_time.time.temporalScope.temporalScopeStart,
                        temporalScopeEnd=ds.space_time.time.temporalScope.temporalScopeEnd
                    )
                )

                # Combine Ind_Space and Ind_Time into Ind_Space_Time
                ind_space_time = Ind_Space_Time(
                    space=ind_space,
                    time=ind_time
                )

                # Construct themes for the indicator
                ind_themes = [
                    Ind_Theme(
                        themeCode=ei.indicatorTheme,
                        themeDescription=ei.indicatorTheme
                    )
                ]

                # Construct Existing_Indicator
                existing_indicator = Existing_Indicator(
                    identification=ind_identification,
                    space_time=ind_space_time,
                    themes=ind_themes,
                    sourceDataset=ds  # Assuming dataset title is the source
                )
                result.append(existing_indicator)


    return result

