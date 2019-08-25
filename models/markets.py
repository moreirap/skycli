# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = markets_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Any, List, TypeVar, Callable, Type, cast


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class Country:
    code: str
    name: str

    @staticmethod
    def from_dict(obj: Any) -> 'Country':
        assert isinstance(obj, dict)
        code = from_str(obj.get("Code"))
        name = from_str(obj.get("Name"))
        return Country(code, name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Code"] = from_str(self.code)
        result["Name"] = from_str(self.name)
        return result


@dataclass
class Markets:
    countries: List[Country]

    @staticmethod
    def from_dict(obj: Any) -> 'Markets':
        assert isinstance(obj, dict)
        countries = from_list(Country.from_dict, obj.get("Countries"))
        return Markets(countries)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Countries"] = from_list(lambda x: to_class(Country, x), self.countries)
        return result


def markets_from_dict(s: Any) -> Markets:
    return Markets.from_dict(s)


def markets_to_dict(x: Markets) -> Any:
    return to_class(Markets, x)
