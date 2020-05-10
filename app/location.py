"""app.location"""
import datetime as dt
from typing import Dict

import pydantic

from .models import Latest
from .utils import countries
from .utils.populations import country_population


class Coordinates(pydantic.BaseModel):
    """
    A position on earth using decimal coordinates (latitude and longitude).
    """

    latitude: float = 0.0
    longitude: float = 0.0

    def __str__(self):
        return f"lat: {self.latitude}, long: {self.longitude}"


class BaseLocation(pydantic.BaseModel):
    """A location in the world affected by the coronavirus."""

    id: int
    country: str
    country_code: str = None
    country_population: int = None
    province: str = None

    # coordinates
    latitude: float = 0.0  # elide
    longitude: float = 0.0  # elide
    coordinates: Coordinates = None

    # Last update.
    last_updated: str = f"{dt.datetime.utcnow()}Z"

    # Statistics
    confirmed: int = 0  # elide
    deaths: int = 0  # elide
    recovered: int = 0  # elide
    latest: Latest = None  # Latest 'statistics'

    class Config:  # pylint: disable=too-few-public-methods
        """pydantic model settings."""

        anystr_strip_whitespace = True

    @pydantic.validator("latest", pre=True, always=True)
    @classmethod
    def set_latest(cls, v, values):
        if v:
            return v
        return {
            "confirmed": values["confirmed"],
            "deaths": values["deaths"],
            "recovered": values["recovered"],
        }

    @pydantic.validator("country_code", always=True)
    @classmethod
    def set_country_code(cls, v, values):
        """Gets the alpha-2 code represention of the country. Returns 'XX' if none is found."""
        if v:
            return v
        return countries.country_code(values.get("country", countries.DEFAULT_COUNTRY_CODE)).upper()

    @pydantic.validator("country_population", always=True)
    @classmethod
    def set_country_population(cls, v, values):
        """Gets the population of this location."""
        if v:
            return v
        return country_population(values["country_code"])

    @pydantic.validator("coordinates", always=True)
    @classmethod
    def set_coordinates(cls, v, values):
        """Sets the coordinates of the location."""
        if v:
            return v
        return {"latitude": values["latitude"], "longitude": values["longitude"]}

    def dict(self, *args, exclude=None, exclude_none=True, **kwargs):
        elided_keys = {"confirmed", "deaths", "recovered", "latitude", "longitude"}
        if exclude:
            elided_keys.update(exclude)
        return super().dict(*args, exclude=elided_keys, exclude_none=True, **kwargs)


class TimelinedLocation(BaseLocation):
    """
    A location with timelines.
    """

    timelines: Dict = {}

    @pydantic.validator("timelines", always=True)
    @classmethod
    def serialize_timelines(cls, d):
        return {k: v.serialize() for (k, v) in d.items()}

    def dict(self, timelines=False, **kwargs) -> Dict:
        """Serializes the location into a dict."""
        serialized = super().dict(**kwargs)

        if timelines is False:
            serialized.pop("timelines")

        # Return the serialized location.
        return serialized


class USLocation(BaseLocation):
    pass


class CSBSLocation(USLocation):
    """
    A CSBS (county) location.
    """

    # pylint: disable=too-many-arguments,redefined-builtin
    def __init__(self, id, state, county, coordinates, last_updated, confirmed, deaths):
        super().__init__(
            # General info.
            id,
            "US",
            state,
            coordinates,
            last_updated,
            # Statistics.
            confirmed=confirmed,
            deaths=deaths,
            recovered=0,
        )

        self.state = state
        self.county = county

    def serialize(self, timelines=False):  # pylint: disable=arguments-differ,unused-argument
        """
        Serializes the location into a dict.
        :returns: The serialized location.
        :rtype: dict
        """
        serialized = super().serialize()

        # Update with new fields.
        serialized.update(
            {"state": self.state, "county": self.county,}
        )

        # Return the serialized location.
        return serialized


class NYTLocation(TimelinedLocation):
    """
    A NYT (county) Timelinedlocation.
    """

    # pylint: disable=too-many-arguments,redefined-builtin
    def __init__(self, id, state, county, coordinates, last_updated, timelines):
        super().__init__(id, "US", state, coordinates, last_updated, timelines)

        self.state = state
        self.county = county

    def serialize(self, timelines=False):  # pylint: disable=arguments-differ,unused-argument
        """
        Serializes the location into a dict.
        :returns: The serialized location.
        :rtype: dict
        """
        serialized = super().serialize(timelines)

        # Update with new fields.
        serialized.update(
            {"state": self.state, "county": self.county,}
        )

        # Return the serialized location.
        return serialized
