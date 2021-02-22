"""app.data"""
import enum

from ..services.location.csbs import CSBSLocationService
from ..services.location.jhu import JhuLocationService
from ..services.location.nyt import NYTLocationService


class Sources(str, enum.Enum):
    """
    A source available for retrieving data.
    """

    jhu = "jhu"
    csbs = "csbs"
    nyt = "nyt"


# Mapping of services to data-sources.
DATA_SOURCES = {
    "jhu": JhuLocationService(),
    "csbs": CSBSLocationService(),
    "nyt": NYTLocationService(),
}


def data_source(source):
    """
    Retrieves the provided data-source service.

    :returns: The service.
    :rtype: LocationService
    """
    return DATA_SOURCES.get(source.lower())
