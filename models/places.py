# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = places_from_dict(json.loads(json_string))

from enum import Enum
from dataclasses import dataclass
from typing import Any, List, TypeVar, Type, Callable, cast


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class CountryID(Enum):
    CA_SKY = "CA-sky"
    UK_SKY = "UK-sky"
    ZA_SKY = "ZA-sky"


class CountryName(Enum):
    CANADA = "Canada"
    SOUTH_AFRICA = "South Africa"
    UNITED_KINGDOM = "United Kingdom"


@dataclass
class Place:
    place_id: str
    place_name: str
    country_id: CountryID
    region_id: str
    city_id: str
    country_name: CountryName

    @staticmethod
    def from_dict(obj: Any) -> 'Place':
        assert isinstance(obj, dict)
        place_id = from_str(obj.get("PlaceId"))
        place_name = from_str(obj.get("PlaceName"))
        country_id = CountryID(obj.get("CountryId"))
        region_id = from_str(obj.get("RegionId"))
        city_id = from_str(obj.get("CityId"))
        country_name = CountryName(obj.get("CountryName"))
        return Place(place_id, place_name, country_id, region_id, city_id, country_name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["PlaceId"] = from_str(self.place_id)
        result["PlaceName"] = from_str(self.place_name)
        result["CountryId"] = to_enum(CountryID, self.country_id)
        result["RegionId"] = from_str(self.region_id)
        result["CityId"] = from_str(self.city_id)
        result["CountryName"] = to_enum(CountryName, self.country_name)
        return result


@dataclass
class Places:
    places: List[Place]

    @staticmethod
    def from_dict(obj: Any) -> 'Places':
        assert isinstance(obj, dict)
        places = from_list(Place.from_dict, obj.get("Places"))
        return Places(places)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Places"] = from_list(lambda x: to_class(Place, x), self.places)
        return result


def places_from_dict(s: Any) -> Places:
    return Places.from_dict(s)


def places_to_dict(x: Places) -> Any:
    return to_class(Places, x)
