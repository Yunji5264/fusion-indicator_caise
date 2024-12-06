import json
import os

class Ind_Spatial_Granularity:
    def __init__(self, spatialGranularity):
        self.spatialGranularity = spatialGranularity

    def to_dict(self):
        return {"spatialGranularity": self.spatialGranularity}

    @classmethod
    def from_dict(cls, data):
        return cls(data["spatialGranularity"])


class Ind_Temporal_Granularity:
    def __init__(self, temporalGranularity):
        self.temporalGranularity = temporalGranularity

    def to_dict(self):
        return {"temporalGranularity": self.temporalGranularity}

    @classmethod
    def from_dict(cls, data):
        return cls(data["temporalGranularity"])


class Ind_Spatial_Scope:
    def __init__(self, spatialScopeLevel, spatialScope):
        self.spatialScopeLevel = spatialScopeLevel
        self.spatialScope = spatialScope

    def to_dict(self):
        return {
            "spatialScopeLevel": self.spatialScopeLevel,
            "spatialScope": self.spatialScope
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["spatialScopeLevel"], data["spatialScope"])


class Ind_Temporal_Scope:
    def __init__(self, temporalScopeLevel, temporalScopeStart, temporalScopeEnd):
        self.temporalScopeLevel = temporalScopeLevel
        self.temporalScopeStart = temporalScopeStart
        self.temporalScopeEnd = temporalScopeEnd

    def to_dict(self):
        return {
            "temporalScopeLevel": self.temporalScopeLevel,
            "temporalScopeStart": self.temporalScopeStart,
            "temporalScopeEnd": self.temporalScopeEnd
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["temporalScopeLevel"],
            data["temporalScopeStart"],
            data["temporalScopeEnd"]
        )


class Ind_Space:
    def __init__(self, spatialGranularity, spatialScope):
        self.spatialGranularity = spatialGranularity
        self.spatialScope = spatialScope

    def to_dict(self):
        return {
            "spatialGranularity": self.spatialGranularity.to_dict(),
            "spatialScope": self.spatialScope.to_dict()
        }

    @classmethod
    def from_dict(cls, data):
        spatial_granularity = Ind_Spatial_Granularity.from_dict(data["spatialGranularity"])
        spatial_scope = Ind_Spatial_Scope.from_dict(data["spatialScope"])
        return cls(spatial_granularity, spatial_scope)


class Ind_Time:
    def __init__(self, temporalGranularity, temporalScope):
        self.temporalGranularity = temporalGranularity
        self.temporalScope = temporalScope

    def to_dict(self):
        return {
            "temporalGranularity": self.temporalGranularity.to_dict(),
            "temporalScope": self.temporalScope.to_dict()
        }

    @classmethod
    def from_dict(cls, data):
        temporal_granularity = Ind_Temporal_Granularity.from_dict(data["temporalGranularity"])
        temporal_scope = Ind_Temporal_Scope.from_dict(data["temporalScope"])
        return cls(temporal_granularity, temporal_scope)


class Ind_Space_Time:
    def __init__(self, space, time):
        self.space = space
        self.time = time

    def to_dict(self):
        return {
            "space": self.space.to_dict(),
            "time": self.time.to_dict()
        }

    @classmethod
    def from_dict(cls, data):
        space = Ind_Space.from_dict(data["space"])
        time = Ind_Time.from_dict(data["time"])
        return cls(space, time)


class Ind_Theme:
    def __init__(self, themeCode, themeDescription):
        self.themeCode = themeCode
        self.themeDescription = themeDescription

    def to_dict(self):
        return {
            "themeCode": self.themeCode,
            "themeDescription": self.themeDescription
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["themeCode"], data["themeDescription"])

class Indicator():
    def __init__(self, dataName, dataDescription, dataType, parameterCode):
        super().__init__(dataName, dataDescription, dataType)
        self.parameterCode = parameterCode

    def to_dict(self):
        data = super().to_dict()
        data["parameterCode"] = self.parameterCode
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["dataName"],
            data["dataDescription"],
            data["dataType"],
            data["parameterCode"]
        )


class Ind_Identification:
    def __init__(self, title, description):
        self.title = title
        self.description = description

    def to_dict(self):
        return {"title": self.title, "description": self.description}

    @classmethod
    def from_dict(cls, data):
        return cls(data["title"], data["description"])

class Indicator:
    def __init__(self, identification, space_time, themes):
        self.identification = identification  # Ind_Identification
        self.space_time = space_time  # Ind_Space_Time
        self.themes = themes  # List of Ind_Theme

    def to_dict(self):
        return {
            "identification": self.identification.to_dict(),
            "space_time": self.space_time.to_dict(),
            "themes": [theme.to_dict() for theme in self.themes]
        }

    def from_dict(cls, data):
        identification = Ind_Identification.from_dict(data["identification"])
        space_time = Ind_Space_Time.from_dict(data["space_time"])
        themes = [Ind_Theme.from_dict(theme) for theme in data["themes"]]
        return cls(identification, space_time, themes)

    def save_to_json(self, file_path):
        """
        Save the Indicator object to a JSON file.

        If the file already exists, the method will append the new indicator to the
        existing data in the file. Otherwise, it will create a new JSON file.
        """
        try:
            # Check if the file exists
            if os.path.exists(file_path):
                # Read the existing content of the file
                with open(file_path, 'r', encoding='utf-8') as f:
                    try:
                        existing_data = json.load(f)  # Load the existing JSON content
                        if not isinstance(existing_data, list):
                            # If the existing data is not a list, wrap it in a list
                            existing_data = [existing_data]
                    except json.JSONDecodeError:
                        # If the file is empty or invalid, start with an empty list
                        existing_data = []
            else:
                existing_data = []

            # Add the current object to the list of indicators
            existing_data.append(self.to_dict())

            # Write the updated content back to the file
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(existing_data, f, ensure_ascii=False, indent=4)

        except Exception as e:
            print(f"Error saving to JSON: {e}")
            raise

    def load_from_json(cls, file_path):
        """
        Load a Requirement object from a JSON file.

        :param file_path: Path to the JSON file.
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls.from_dict(data)


# 扩展类：现有指标
class Existing_Indicator(Indicator):
    """
    Represents an existing indicator that inherits from the Indicator class.
    Includes additional information such as the source dataset.
    """
    def __init__(self, identification, space_time, themes, sourceDataset):
        """
        Initialize the Existing_Indicator class.

        Args:
            identification (Ind_Identification): Identification details of the indicator.
            space_time (Ind_Space_Time): Spatial and temporal details of the indicator.
            themes (list of Ind_Theme): Associated themes for the indicator.
            sourceDataset (Dataset or str): The source dataset of the indicator.
        """
        super().__init__(identification, space_time, themes)
        self.sourceDataset = sourceDataset

    def to_dict(self):
        """
        Convert the Existing_Indicator instance to a dictionary.

        Returns:
            dict: Dictionary representation of the indicator.
        """
        data = super().to_dict()  # Call the parent class's to_dict method
        data["sourceDataset"] = (
            self.sourceDataset.to_dict() if hasattr(self.sourceDataset, "to_dict") else str(self.sourceDataset)
        )
        return data

    @classmethod
    def from_dict(cls, data):
        """
        Create an Existing_Indicator instance from a dictionary.

        Args:
            data (dict): Dictionary containing indicator data.

        Returns:
            Existing_Indicator: The created instance.
        """
        base = super().from_dict(data)  # Call the parent class's from_dict method
        return cls(
            base.identification,
            base.space_time,
            base.themes,
            data.get("sourceDataset")
        )

# 扩展类：跨主题指标
class CrossTheme_Indicator(Indicator):
    def __init__(self, identification, space_time, themes, baseIndicators):
        super().__init__(identification, space_time, themes)
        self.baseIndicators = baseIndicators  # List of Indicator

    def to_dict(self):
        data = super().to_dict()
        data["baseIndicators"] = [indicator.to_dict() for indicator in self.baseIndicators]
        return data

    @classmethod
    def from_dict(cls, data):
        base = super().from_dict(data)
        base_indicators = [Indicator.from_dict(ind) for ind in data["baseIndicators"]]
        return cls(base.identification, base.space_time, base.themes, base_indicators)

