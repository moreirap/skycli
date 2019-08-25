# This code parses date/times, so please
#
#     pip install python-dateutil
#
# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = routes_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Any, List, TypeVar, Callable, Type, cast
from datetime import datetime
import dateutil.parser


T = TypeVar("T")


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x

def from_float(x: Any) -> float:
    assert isinstance(x, float) and not isinstance(x, bool)
    return x

def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class Carrier:
    carrier_id: int
    name: str

    @staticmethod
    def from_dict(obj: Any) -> 'Carrier':
        assert isinstance(obj, dict)
        carrier_id = from_int(obj.get("CarrierId"))
        name = from_str(obj.get("Name"))
        return Carrier(carrier_id, name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["CarrierId"] = from_int(self.carrier_id)
        result["Name"] = from_str(self.name)
        return result


@dataclass
class Currency:
    code: str
    symbol: str
    thousands_separator: str
    decimal_separator: str
    symbol_on_left: bool
    space_between_amount_and_symbol: bool
    rounding_coefficient: int
    decimal_digits: int

    @staticmethod
    def from_dict(obj: Any) -> 'Currency':
        assert isinstance(obj, dict)
        code = from_str(obj.get("Code"))
        symbol = from_str(obj.get("Symbol"))
        thousands_separator = from_str(obj.get("ThousandsSeparator"))
        decimal_separator = from_str(obj.get("DecimalSeparator"))
        symbol_on_left = from_bool(obj.get("SymbolOnLeft"))
        space_between_amount_and_symbol = from_bool(obj.get("SpaceBetweenAmountAndSymbol"))
        rounding_coefficient = from_int(obj.get("RoundingCoefficient"))
        decimal_digits = from_int(obj.get("DecimalDigits"))
        return Currency(code, symbol, thousands_separator, decimal_separator, symbol_on_left, space_between_amount_and_symbol, rounding_coefficient, decimal_digits)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Code"] = from_str(self.code)
        result["Symbol"] = from_str(self.symbol)
        result["ThousandsSeparator"] = from_str(self.thousands_separator)
        result["DecimalSeparator"] = from_str(self.decimal_separator)
        result["SymbolOnLeft"] = from_bool(self.symbol_on_left)
        result["SpaceBetweenAmountAndSymbol"] = from_bool(self.space_between_amount_and_symbol)
        result["RoundingCoefficient"] = from_int(self.rounding_coefficient)
        result["DecimalDigits"] = from_int(self.decimal_digits)
        return result


@dataclass
class Place:
    place_id: int
    iata_code: str
    name: str
    type: str
    skyscanner_code: str
    city_name: str
    city_id: str
    country_name: str

    @staticmethod
    def from_dict(obj: Any) -> 'Place':
        assert isinstance(obj, dict)
        place_id = from_int(obj.get("PlaceId"))
        iata_code = from_str(obj.get("IataCode"))
        name = from_str(obj.get("Name"))
        type = from_str(obj.get("Type"))
        skyscanner_code = from_str(obj.get("SkyscannerCode"))
        city_name = from_str(obj.get("CityName"))
        city_id = from_str(obj.get("CityId"))
        country_name = from_str(obj.get("CountryName"))
        return Place(place_id, iata_code, name, type, skyscanner_code, city_name, city_id, country_name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["PlaceId"] = from_int(self.place_id)
        result["IataCode"] = from_str(self.iata_code)
        result["Name"] = from_str(self.name)
        result["Type"] = from_str(self.type)
        result["SkyscannerCode"] = from_str(self.skyscanner_code)
        result["CityName"] = from_str(self.city_name)
        result["CityId"] = from_str(self.city_id)
        result["CountryName"] = from_str(self.country_name)
        return result


@dataclass
class OutboundLeg:
    carrier_ids: List[int]
    origin_id: int
    destination_id: int
    departure_date: datetime

    @staticmethod
    def from_dict(obj: Any) -> 'OutboundLeg':
        assert isinstance(obj, dict)
        carrier_ids = from_list(from_int, obj.get("CarrierIds"))
        origin_id = from_int(obj.get("OriginId"))
        destination_id = from_int(obj.get("DestinationId"))
        departure_date = from_datetime(obj.get("DepartureDate"))
        return OutboundLeg(carrier_ids, origin_id, destination_id, departure_date)

    def to_dict(self) -> dict:
        result: dict = {}
        result["CarrierIds"] = from_list(from_int, self.carrier_ids)
        result["OriginId"] = from_int(self.origin_id)
        result["DestinationId"] = from_int(self.destination_id)
        result["DepartureDate"] = self.departure_date.isoformat()
        return result


@dataclass
class Quote:
    quote_id: int
    min_price: int
    direct: bool
    outbound_leg: OutboundLeg
    quote_date_time: datetime

    @staticmethod
    def from_dict(obj: Any) -> 'Quote':
        assert isinstance(obj, dict)
        quote_id = from_int(obj.get("QuoteId"))
        min_price = from_float(obj.get("MinPrice"))
        direct = from_bool(obj.get("Direct"))
        outbound_leg = OutboundLeg.from_dict(obj.get("OutboundLeg"))
        quote_date_time = from_datetime(obj.get("QuoteDateTime"))
        return Quote(quote_id, min_price, direct, outbound_leg, quote_date_time)

    def to_dict(self) -> dict:
        result: dict = {}
        result["QuoteId"] = from_int(self.quote_id)
        result["MinPrice"] = from_float(self.min_price)
        result["Direct"] = from_bool(self.direct)
        result["OutboundLeg"] = to_class(OutboundLeg, self.outbound_leg)
        result["QuoteDateTime"] = self.quote_date_time.isoformat()
        return result


@dataclass
class Routes:
    routes: List[Any]
    quotes: List[Quote]
    places: List[Place]
    carriers: List[Carrier]
    currencies: List[Currency]

    @staticmethod
    def from_dict(obj: Any) -> 'Routes':
        assert isinstance(obj, dict)
        routes = from_list(lambda x: x, obj.get("Routes"))
        quotes = from_list(Quote.from_dict, obj.get("Quotes"))
        places = from_list(Place.from_dict, obj.get("Places"))
        carriers = from_list(Carrier.from_dict, obj.get("Carriers"))
        currencies = from_list(Currency.from_dict, obj.get("Currencies"))
        return Routes(routes, quotes, places, carriers, currencies)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Routes"] = from_list(lambda x: x, self.routes)
        result["Quotes"] = from_list(lambda x: to_class(Quote, x), self.quotes)
        result["Places"] = from_list(lambda x: to_class(Place, x), self.places)
        result["Carriers"] = from_list(lambda x: to_class(Carrier, x), self.carriers)
        result["Currencies"] = from_list(lambda x: to_class(Currency, x), self.currencies)
        return result


def routes_from_dict(s: Any) -> Routes:
    return Routes.from_dict(s)


def routes_to_dict(x: Routes) -> Any:
    return to_class(Routes, x)
