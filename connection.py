import requests
from requests.exceptions import RequestException
import json
from sys import exit
from models.quotes import quotes_from_dict
from models.places import places_from_dict
from models.markets import markets_from_dict
from models.currencies import currencies_from_dict
from models.routes import routes_from_dict

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

    def _get_defaults(self, **params):
        if "country" in params and params["country"] == None:
            params["country"] = self.country
        if "currency" in params and params["currency"] == None:
            params["currency"] = self.currency
        if "locale" in params and params["locale"] == None:
            params["locale"] = self.locale
        return params

    def _send(self, url, headers, query = {}):
        try:
            response = requests.request("GET", url, headers=headers, params=query)
            response.raise_for_status() # Anything other than 2xx status generates error
            return response
        except RequestException as e: # Catch all errors -> print result and exit
            print("Error invoking API: {}".format(e))
            exit(1)

    def _invoke_api(self, url, query, **url_params):
        url_params = self._get_defaults(**url_params)
        url = self.baseurl.format(url.format(*url_params.values()))
        response = self._send(url, self.headers, query = query)
        return json.loads(response.text)

    def list_markets(self, locale = None):
        """Retrieve the market countries that we support."""
        
        json_response = self._invoke_api("reference/v1.0/countries/{}", {}, locale = locale)
        return markets_from_dict(json_response)
   
    def list_places(self, query, country = None, currency = None, locale = None):
        """Get a list of places that match a query string."""
        json_response = self._invoke_api("autosuggest/v1.0/{}/{}/{}/", 
                                    {"query": query}, 
                                    country = country, 
                                    currency = currency, 
                                    locale = locale)
        result = places_from_dict(json_response)
        return result

    def get_currencies(self):
        """Retrieve the currencies that we support."""
        
        json_response = self._invoke_api("reference/v1.0/currencies", {})
        result = currencies_from_dict(json_response)
        return result

    def browse_quotes(self, originplace, destinationplace, outboundpartialdate, country = None, currency = None, locale = None, inboundpartialdate = "anytime"):
        """Retrieve the cheapest quotes from our cache prices."""        
        
        json_response = self._invoke_api("browsequotes/v1.0/{}/{}/{}/{}/{}/{}", 
                                    {"inboundpartialdate": inboundpartialdate}, 
                                    country = country, 
                                    currency = currency, 
                                    locale = locale,
                                    originplace = originplace, 
                                    destinationplace = destinationplace, 
                                    outboundpartialdate = outboundpartialdate)
        result = quotes_from_dict(json_response)
        return result

    def browse_routes(self, originplace, destinationplace, outboundpartialdate, country = None, currency = None, locale = None, inboundpartialdate = "anytime"):
        """Retrieve the cheapest routes from our cache prices."""
        
        json_response = self._invoke_api("browseroutes/v1.0/{}/{}/{}/{}/{}/{}", 
                                    {"inboundpartialdate": inboundpartialdate}, 
                                    country = country, 
                                    currency = currency, 
                                    locale = locale,
                                    originplace = originplace, 
                                    destinationplace = destinationplace, 
                                    outboundpartialdate = outboundpartialdate)
        result = routes_from_dict(json_response)

        return result
