# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = currencies_from_dict(json.loads(json_string))

from enum import Enum
from dataclasses import dataclass
from typing import Any, List, TypeVar, Type, Callable, cast


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
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


class DecimalSeparator(Enum):
    DECIMAL_SEPARATOR = ","
    EMPTY = "."
    FLUFFY = "-"
    PURPLE = "/"


class ThousandsSeparator(Enum):
    EMPTY = ","
    FLUFFY = "'"
    PURPLE = " "
    THOUSANDS_SEPARATOR = "."


@dataclass
class Currency:
    code: str
    symbol: str
    thousands_separator: ThousandsSeparator
    decimal_separator: DecimalSeparator
    symbol_on_left: bool
    space_between_amount_and_symbol: bool
    rounding_coefficient: int
    decimal_digits: int

    @staticmethod
    def from_dict(obj: Any) -> 'Currency':
        assert isinstance(obj, dict)
        code = from_str(obj.get("Code"))
        symbol = from_str(obj.get("Symbol"))
        thousands_separator = ThousandsSeparator(obj.get("ThousandsSeparator"))
        decimal_separator = DecimalSeparator(obj.get("DecimalSeparator"))
        symbol_on_left = from_bool(obj.get("SymbolOnLeft"))
        space_between_amount_and_symbol = from_bool(obj.get("SpaceBetweenAmountAndSymbol"))
        rounding_coefficient = from_int(obj.get("RoundingCoefficient"))
        decimal_digits = from_int(obj.get("DecimalDigits"))
        return Currency(code, symbol, thousands_separator, decimal_separator, symbol_on_left, space_between_amount_and_symbol, rounding_coefficient, decimal_digits)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Code"] = from_str(self.code)
        result["Symbol"] = from_str(self.symbol)
        result["ThousandsSeparator"] = to_enum(ThousandsSeparator, self.thousands_separator)
        result["DecimalSeparator"] = to_enum(DecimalSeparator, self.decimal_separator)
        result["SymbolOnLeft"] = from_bool(self.symbol_on_left)
        result["SpaceBetweenAmountAndSymbol"] = from_bool(self.space_between_amount_and_symbol)
        result["RoundingCoefficient"] = from_int(self.rounding_coefficient)
        result["DecimalDigits"] = from_int(self.decimal_digits)
        return result


@dataclass
class Currencies:
    currencies: List[Currency]

    @staticmethod
    def from_dict(obj: Any) -> 'Currencies':
        assert isinstance(obj, dict)
        currencies = from_list(Currency.from_dict, obj.get("Currencies"))
        return Currencies(currencies)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Currencies"] = from_list(lambda x: to_class(Currency, x), self.currencies)
        return result


def currencies_from_dict(s: Any) -> Currencies:
    return Currencies.from_dict(s)


def currencies_to_dict(x: Currencies) -> Any:
    return to_class(Currencies, x)
