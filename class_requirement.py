import json

class Req_Spatial_Granularity:
    def __init__(self, spatialGranularity):
        self.spatialGranularity = spatialGranularity

    def to_dict(self):
        return {"spatialGranularity": self.spatialGranularity}

    @classmethod
    def from_dict(cls, data):
        return cls(data["spatialGranularity"])


class Req_Temporal_Granularity:
    def __init__(self, temporalGranularity):
        self.temporalGranularity = temporalGranularity

    def to_dict(self):
        return {"temporalGranularity": self.temporalGranularity}

    @classmethod
    def from_dict(cls, data):
        return cls(data["temporalGranularity"])


class Req_Spatial_Scope:
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


class Req_Temporal_Scope:
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


class Req_Space:
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
        spatial_granularity = Req_Spatial_Granularity.from_dict(data["spatialGranularity"])
        spatial_scope = Req_Spatial_Scope.from_dict(data["spatialScope"])
        return cls(spatial_granularity, spatial_scope)


class Req_Time:
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
        temporal_granularity = Req_Temporal_Granularity.from_dict(data["temporalGranularity"])
        temporal_scope = Req_Temporal_Scope.from_dict(data["temporalScope"])
        return cls(temporal_granularity, temporal_scope)


class Req_Space_Time:
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
        space = Req_Space.from_dict(data["space"])
        time = Req_Time.from_dict(data["time"])
        return cls(space, time)


class Req_Theme:
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


class Requirement:
    def __init__(self, space_time, themes):
        """
        Represents a Requirement with space-time and multiple themes.

        :param space_time: Req_Space_Time object
        :param themes: List of Req_Theme objects
        """
        self.space_time = space_time  # Req_Space_Time object
        self.themes = themes  # List of Req_Theme objects

    def to_dict(self):
        """
        Serialize the Requirement object into a dictionary format.
        """
        return {
            "space_time": self.space_time.to_dict(),
            "themes": [theme.to_dict() for theme in self.themes]  # Convert each theme to a dictionary
        }

    @classmethod
    def from_dict(cls, data):
        """
        Deserialize a dictionary into a Requirement object.

        :param data: Dictionary containing the requirement structure.
        """
        space_time = Req_Space_Time.from_dict(data["space_time"])
        themes = [Req_Theme.from_dict(theme) for theme in data["themes"]]  # Deserialize each theme

        return cls(space_time, themes)

    def save_to_json(self, file_path):
        """
        Save the Requirement object to a JSON file.

        :param file_path: Path where the JSON file will be saved.
        """
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=4)

    @classmethod
    def load_from_json(cls, file_path):
        """
        Load a Requirement object from a JSON file.

        :param file_path: Path to the JSON file.
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls.from_dict(data)

