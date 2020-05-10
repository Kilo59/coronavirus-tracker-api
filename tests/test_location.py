import datetime as dt
from pprint import pformat as pf
from unittest import mock

import pytest

from app import coordinates, location, timeline


def mocked_timeline(*args, **kwargs):
    class TestTimeline:
        def __init__(self, latest):
            self.latest = latest

    return TestTimeline(args[0])


@pytest.mark.skip
@pytest.mark.parametrize(
    "test_id, country, country_code, province, latitude, longitude, confirmed_latest, deaths_latest, recovered_latest",
    [
        (0, "Thailand", "TH", "", 15, 100, 1000, 1111, 22222),
        (1, "Deutschland", "DE", "", 15, 100, 1000, 1111, 22222),
        (2, "Cruise Ship", "XX", "", 15, 100, 1000, 1111, 22222),
    ],
)
@mock.patch("app.timeline.Timeline", side_effect=mocked_timeline)
def test_location_class(
    mocked_timeline,
    test_id,
    country,
    country_code,
    province,
    latitude,
    longitude,
    confirmed_latest,
    deaths_latest,
    recovered_latest,
):
    # id, country, province, coordinates, confirmed, deaths, recovered
    coords = coordinates.Coordinates(latitude=latitude, longitude=longitude)

    # Timelines
    confirmed = timeline.Timeline(confirmed_latest)
    deaths = timeline.Timeline(deaths_latest)
    recovered = timeline.Timeline(recovered_latest)

    # Date now.
    now = dt.datetime.utcnow().isoformat() + "Z"

    # Location.
    location_obj = location.TimelinedLocation(
        test_id,
        country,
        province,
        coords,
        now,
        {"confirmed": confirmed, "deaths": deaths, "recovered": recovered,},
    )

    assert location_obj.country_code == country_code
    assert not location_obj.serialize() == None


@pytest.mark.parametrize(
    "test_id, country, kwargs",
    [
        (
            0,
            "Thailand",
            {
                "country_code": "TH",
                "latitude": 15,
                "longitude": 100,
                "confirmed": 1000,
                "deaths": 1111,
                "recovered": 22222,
            },
        ),
        (
            1,
            "Deutschland",
            {
                "country_code": "DE",
                "latitude": 15,
                "longitude": 100,
                "latest": {"confirmed": 1000, "deaths": 1111, "recovered": 22222,},
            },
        ),
        (
            2,
            "Cruise Ship",
            {
                "country_code": "XX",
                "province": None,
                "latitude": 15,
                "longitude": 100,
                "confirmed": 1000,
                "deaths": 1111,
                "recovered": 22222,
            },
        ),
    ],
)
def test_base_location(test_id, country, kwargs):
    kwargs["last_updated"] = dt.datetime.utcnow().isoformat() + "Z"
    print(f"   {test_id} {country}\n{pf(kwargs)}")
    location_instance = location.BaseLocation(id=test_id, country=country, **kwargs)

    print(f"\n   {location.BaseLocation.__name__}.dict()\n{pf(location_instance.dict())}")

    assert location_instance.country_code
    if location_instance.country_code != "XX":
        assert location_instance.country_population
