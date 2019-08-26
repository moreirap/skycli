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
#     result = live_prices_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Any, List, Optional, TypeVar, Callable, Type, cast
from datetime import datetime
from uuid import UUID
import dateutil.parser


T = TypeVar("T")


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x

def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x

def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


@dataclass
class Agent:
    id: int
    name: str
    image_url: str
    status: str
    optimised_for_mobile: str
    type: str

    @staticmethod
    def from_dict(obj: Any) -> 'Agent':
        assert isinstance(obj, dict)
        id = from_int(obj.get("Id"))
        name = from_str(obj.get("Name"))
        image_url = from_str(obj.get("ImageUrl"))
        status = from_str(obj.get("Status"))
        optimised_for_mobile = from_bool(obj.get("OptimisedForMobile"))
        type = from_str(obj.get("Type"))
        return Agent(id, name, image_url, status, optimised_for_mobile, type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Id"] = from_int(self.id)
        result["Name"] = from_str(self.name)
        result["ImageUrl"] = from_str(self.image_url)
        result["Status"] = from_str(self.status)
        result["OptimisedForMobile"] = from_bool(self.optimised_for_mobile)
        result["Type"] = from_str(self.type)
        return result


@dataclass
class Carrier:
    id: int
    code: str
    name: str
    image_url: str
    display_code: str

    @staticmethod
    def from_dict(obj: Any) -> 'Carrier':
        assert isinstance(obj, dict)
        id = from_int(obj.get("Id"))
        code = from_str(obj.get("Code"))
        name = from_str(obj.get("Name"))
        image_url = from_str(obj.get("ImageUrl"))
        display_code = from_str(obj.get("DisplayCode"))
        return Carrier(id, code, name, image_url, display_code)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Id"] = from_int(self.id)
        result["Code"] = from_str(self.code)
        result["Name"] = from_str(self.name)
        result["ImageUrl"] = from_str(self.image_url)
        result["DisplayCode"] = from_str(self.display_code)
        return result


@dataclass
class Currency:
    code: str
    symbol: str
    thousands_separator: str
    decimal_separator: str
    symbol_on_left: str
    space_between_amount_and_symbol: str
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
class BookingDetailsLink:
    uri: str
    body: str
    method: str

    @staticmethod
    def from_dict(obj: Any) -> 'BookingDetailsLink':
        assert isinstance(obj, dict)
        uri = from_str(obj.get("Uri"))
        body = from_str(obj.get("Body"))
        method = from_str(obj.get("Method"))
        return BookingDetailsLink(uri, body, method)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Uri"] = from_str(self.uri)
        result["Body"] = from_str(self.body)
        result["Method"] = from_str(self.method)
        return result


@dataclass
class PricingOption:
    agents: List[int]
    quote_age_in_minutes: int
    price: float
    deeplink_url: str

    @staticmethod
    def from_dict(obj: Any) -> 'PricingOption':
        assert isinstance(obj, dict)
        agents = from_list(from_int, obj.get("Agents"))
        quote_age_in_minutes = from_int(obj.get("QuoteAgeInMinutes"))
        price = from_float(obj.get("Price"))
        deeplink_url = from_str(obj.get("DeeplinkUrl"))
        return PricingOption(agents, quote_age_in_minutes, price, deeplink_url)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Agents"] = from_list(from_int, self.agents)
        result["QuoteAgeInMinutes"] = from_int(self.quote_age_in_minutes)
        result["Price"] = to_float(self.price)
        result["DeeplinkUrl"] = from_str(self.deeplink_url)
        return result


@dataclass
class Itinerary:
    outbound_leg_id: str
    pricing_options: List[PricingOption]
    booking_details_link: BookingDetailsLink

    @staticmethod
    def from_dict(obj: Any) -> 'Itinerary':
        assert isinstance(obj, dict)
        outbound_leg_id = from_str(obj.get("OutboundLegId"))
        pricing_options = from_list(PricingOption.from_dict, obj.get("PricingOptions"))
        booking_details_link = BookingDetailsLink.from_dict(obj.get("BookingDetailsLink"))
        return Itinerary(outbound_leg_id, pricing_options, booking_details_link)

    def to_dict(self) -> dict:
        result: dict = {}
        result["OutboundLegId"] = from_str(self.outbound_leg_id)
        result["PricingOptions"] = from_list(lambda x: to_class(PricingOption, x), self.pricing_options)
        result["BookingDetailsLink"] = to_class(BookingDetailsLink, self.booking_details_link)
        return result


@dataclass
class FlightNumber:
    flight_number: int
    carrier_id: int

    @staticmethod
    def from_dict(obj: Any) -> 'FlightNumber':
        assert isinstance(obj, dict)
        flight_number = int(from_str(obj.get("FlightNumber")))
        carrier_id = from_int(obj.get("CarrierId"))
        return FlightNumber(flight_number, carrier_id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["FlightNumber"] = from_str(str(self.flight_number))
        result["CarrierId"] = from_int(self.carrier_id)
        return result


@dataclass
class Leg:
    id: str
    segment_ids: List[int]
    origin_station: int
    destination_station: int
    departure: datetime
    arrival: datetime
    duration: int
    journey_mode: str
    stops: List[int]
    carriers: List[int]
    operating_carriers: List[int]
    directionality: str
    flight_numbers: List[FlightNumber]

    @staticmethod
    def from_dict(obj: Any) -> 'Leg':
        assert isinstance(obj, dict)
        id = from_str(obj.get("Id"))
        segment_ids = from_list(from_int, obj.get("SegmentIds"))
        origin_station = from_int(obj.get("OriginStation"))
        destination_station = from_int(obj.get("DestinationStation"))
        departure = from_datetime(obj.get("Departure"))
        arrival = from_datetime(obj.get("Arrival"))
        duration = from_int(obj.get("Duration"))
        journey_mode = from_str(obj.get("JourneyMode"))
        stops = from_list(from_int, obj.get("Stops"))
        carriers = from_list(from_int, obj.get("Carriers"))
        operating_carriers = from_list(from_int, obj.get("OperatingCarriers"))
        directionality = from_str(obj.get("Directionality"))
        flight_numbers = from_list(FlightNumber.from_dict, obj.get("FlightNumbers"))
        return Leg(id, segment_ids, origin_station, destination_station, departure, arrival, duration, journey_mode, stops, carriers, operating_carriers, directionality, flight_numbers)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Id"] = from_str(self.id)
        result["SegmentIds"] = from_list(from_int, self.segment_ids)
        result["OriginStation"] = from_int(self.origin_station)
        result["DestinationStation"] = from_int(self.destination_station)
        result["Departure"] = self.departure.isoformat()
        result["Arrival"] = self.arrival.isoformat()
        result["Duration"] = from_int(self.duration)
        result["JourneyMode"] = from_str(self.journey_mode)
        result["Stops"] = from_list(from_int, self.stops)
        result["Carriers"] = from_list(from_int, self.carriers)
        result["OperatingCarriers"] = from_list(from_int, self.operating_carriers)
        result["Directionality"] = from_str(self.directionality)
        result["FlightNumbers"] = from_list(lambda x: to_class(FlightNumber, x), self.flight_numbers)
        return result


@dataclass
class Place:
    id: int
    code: str
    type: str
    name: str
    parent_id: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Place':
        assert isinstance(obj, dict)
        id = from_int(obj.get("Id"))
        code = from_str(obj.get("Code"))
        type = from_str(obj.get("Type"))
        name = from_str(obj.get("Name"))
        parent_id = from_union([from_int, from_none], obj.get("ParentId"))
        return Place(id, code, type, name, parent_id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Id"] = from_int(self.id)
        result["Code"] = from_str(self.code)
        result["Type"] = from_str(self.type)
        result["Name"] = from_str(self.name)
        result["ParentId"] = from_union([from_int, from_none], self.parent_id)
        return result


@dataclass
class Query:
    country: str
    currency: str
    locale: str
    adults: int
    children: int
    infants: int
    origin_place: int
    destination_place: int
    outbound_date: datetime
    location_schema: str
    cabin_class: str
    group_pricing: str

    @staticmethod
    def from_dict(obj: Any) -> 'Query':
        assert isinstance(obj, dict)
        country = from_str(obj.get("Country"))
        currency = from_str(obj.get("Currency"))
        locale = from_str(obj.get("Locale"))
        adults = from_int(obj.get("Adults"))
        children = from_int(obj.get("Children"))
        infants = from_int(obj.get("Infants"))
        origin_place = int(from_str(obj.get("OriginPlace")))
        destination_place = int(from_str(obj.get("DestinationPlace")))
        outbound_date = from_datetime(obj.get("OutboundDate"))
        location_schema = from_str(obj.get("LocationSchema"))
        cabin_class = from_str(obj.get("CabinClass"))
        group_pricing = from_bool(obj.get("GroupPricing"))
        return Query(country, currency, locale, adults, children, infants, origin_place, destination_place, outbound_date, location_schema, cabin_class, group_pricing)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Country"] = from_str(self.country)
        result["Currency"] = from_str(self.currency)
        result["Locale"] = from_str(self.locale)
        result["Adults"] = from_int(self.adults)
        result["Children"] = from_int(self.children)
        result["Infants"] = from_int(self.infants)
        result["OriginPlace"] = from_str(str(self.origin_place))
        result["DestinationPlace"] = from_str(str(self.destination_place))
        result["OutboundDate"] = self.outbound_date.isoformat()
        result["LocationSchema"] = from_str(self.location_schema)
        result["CabinClass"] = from_str(self.cabin_class)
        result["GroupPricing"] = from_bool(self.group_pricing)
        return result


@dataclass
class Segment:
    id: int
    origin_station: int
    destination_station: int
    departure_date_time: datetime
    arrival_date_time: datetime
    carrier: int
    operating_carrier: int
    duration: int
    flight_number: int
    journey_mode: str
    directionality: str

    @staticmethod
    def from_dict(obj: Any) -> 'Segment':
        assert isinstance(obj, dict)
        id = from_int(obj.get("Id"))
        origin_station = from_int(obj.get("OriginStation"))
        destination_station = from_int(obj.get("DestinationStation"))
        departure_date_time = from_datetime(obj.get("DepartureDateTime"))
        arrival_date_time = from_datetime(obj.get("ArrivalDateTime"))
        carrier = from_int(obj.get("Carrier"))
        operating_carrier = from_int(obj.get("OperatingCarrier"))
        duration = from_int(obj.get("Duration"))
        flight_number = int(from_str(obj.get("FlightNumber")))
        journey_mode = from_str(obj.get("JourneyMode"))
        directionality = from_str(obj.get("Directionality"))
        return Segment(id, origin_station, destination_station, departure_date_time, arrival_date_time, carrier, operating_carrier, duration, flight_number, journey_mode, directionality)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Id"] = from_int(self.id)
        result["OriginStation"] = from_int(self.origin_station)
        result["DestinationStation"] = from_int(self.destination_station)
        result["DepartureDateTime"] = self.departure_date_time.isoformat()
        result["ArrivalDateTime"] = self.arrival_date_time.isoformat()
        result["Carrier"] = from_int(self.carrier)
        result["OperatingCarrier"] = from_int(self.operating_carrier)
        result["Duration"] = from_int(self.duration)
        result["FlightNumber"] = from_str(str(self.flight_number))
        result["JourneyMode"] = from_str(self.journey_mode)
        result["Directionality"] = from_str(self.directionality)
        return result


@dataclass
class LivePrices:
    session_key: UUID
    query: Query
    status: str
    itineraries: List[Itinerary]
    legs: List[Leg]
    segments: List[Segment]
    carriers: List[Carrier]
    agents: List[Agent]
    places: List[Place]
    currencies: List[Currency]

    @staticmethod
    def from_dict(obj: Any) -> 'LivePrices':
        assert isinstance(obj, dict)
        session_key = UUID(obj.get("SessionKey"))
        query = Query.from_dict(obj.get("Query"))
        status = from_str(obj.get("Status"))
        itineraries = from_list(Itinerary.from_dict, obj.get("Itineraries"))
        legs = from_list(Leg.from_dict, obj.get("Legs"))
        segments = from_list(Segment.from_dict, obj.get("Segments"))
        carriers = from_list(Carrier.from_dict, obj.get("Carriers"))
        agents = from_list(Agent.from_dict, obj.get("Agents"))
        places = from_list(Place.from_dict, obj.get("Places"))
        currencies = from_list(Currency.from_dict, obj.get("Currencies"))
        return LivePrices(session_key, query, status, itineraries, legs, segments, carriers, agents, places, currencies)

    def to_dict(self) -> dict:
        result: dict = {}
        result["SessionKey"] = str(self.session_key)
        result["Query"] = to_class(Query, self.query)
        result["Status"] = from_str(self.status)
        result["Itineraries"] = from_list(lambda x: to_class(Itinerary, x), self.itineraries)
        result["Legs"] = from_list(lambda x: to_class(Leg, x), self.legs)
        result["Segments"] = from_list(lambda x: to_class(Segment, x), self.segments)
        result["Carriers"] = from_list(lambda x: to_class(Carrier, x), self.carriers)
        result["Agents"] = from_list(lambda x: to_class(Agent, x), self.agents)
        result["Places"] = from_list(lambda x: to_class(Place, x), self.places)
        result["Currencies"] = from_list(lambda x: to_class(Currency, x), self.currencies)
        return result


def live_prices_from_dict(s: Any) -> LivePrices:
    return LivePrices.from_dict(s)


def live_prices_to_dict(x: LivePrices) -> Any:
    return to_class(LivePrices, x)
