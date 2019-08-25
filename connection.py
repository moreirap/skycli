import requests
from requests.exceptions import RequestException
import json
from sys import exit
from models.quotes import quotes_from_dict
from models.places import places_from_dict
from models.markets import markets_from_dict
from models.currencies import currencies_from_dict


class Connection(object):
    def __init__(self, key, country, currency, locale):
        self.baseurl = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/{}"
        self.host = "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com"
        self.key  = key
        self.headers = {
            'x-rapidapi-host': self.host,
            'x-rapidapi-key': self.key
        }
        self.country = country
        self.currency = currency
        self.locale = locale

    def _get_defaults(self, country = None, currency = None, locale = None):
        country = country if country else self.country
        currency = currency if currency else self.currency
        locale = locale if locale else self.locale
        return country, currency, locale
    
    def _send(self, url, headers, params = {}):
        try:
            response = requests.request("GET", url, headers=headers, params=params)
            response.raise_for_status()
            return response
        except RequestException as e: # Catch all errors -> print result and exit
            print("Error invoking API: {}".format(e))
            exit(1)

    def list_markets(self, locale = None):
        """Retrieve the market countries that we support."""
        _,_,locale = self._get_defaults(locale = locale)
        url = self.baseurl.format("reference/v1.0/countries/{}".format(locale))
        response = self._send(url, self.headers)
        result = markets_from_dict(json.loads(response.text))
        return result
    
    def list_places(self, query, country = None, currency = None, locale = None):
        """Get a list of places that match a query string."""
        country, currency, locale = self._get_defaults(country, currency, locale)
        params = {"query": query}
        url = self.baseurl.format("autosuggest/v1.0/{}/{}/{}/".format(country, currency, locale))
        response = self._send(url, self.headers, params = params)
        result = places_from_dict(json.loads(response.text))
        return result

    def get_currencies(self):
        """Retrieve the currencies that we support."""
        url = self.baseurl.format("reference/v1.0/currencies")
        response = self._send(url, self.headers)
        result = currencies_from_dict(json.loads(response.text))
        return result

    def browse_quotes(self, originplace, destinationplace, outboundpartialdate, country = None, currency = None, locale = None, inboundpartialdate = "anytime"):
        """Retrieve the cheapest quotes from our cache prices."""
        country, currency, locale = self._get_defaults(country, currency, locale)
        querystring = {"inboundpartialdate": inboundpartialdate}
        url = self.baseurl.format("browsequotes/v1.0/{}/{}/{}/{}/{}/{}".format(country, currency, locale, originplace, destinationplace, outboundpartialdate))
        response = self._send(url, self.headers, params = querystring)
        result = quotes_from_dict(json.loads(response.text))
        return result