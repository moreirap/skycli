import requests
import click
import os
from json import dumps
from collections import defaultdict

from connection import Connection
from skyscanner_datetime import SkyScannerDateTime

class RapidApi(object):
    def __init__(self, key, country , currency, locale):
        self.country = country
        self.currency = currency
        self.locale = locale
        self.key = key

    def con(self):
        if self.key is None:
            raise ConnectionError("API key not provided")
        return Connection(key = self.key, country = self.country, currency = self.currency, locale=self.locale) 

    def log_json_response(self,response):
        click.secho(dumps(response.to_dict()), fg="cyan")

@click.group(name="skycli")
@click.pass_context
@click.option('--key',
              default=lambda: os.environ.get('SKYSCANNER_API_KEY', ''),
              show_default='env[''SKYSCANNER_API_KEY'']',
              type=click.STRING, help="RapidApi key.")
@click.option("--country", help="The market/country your user is in", show_default="UK", default="UK")
@click.option("--currency", help="The currency you want the prices in", show_default="GBP", default="GBP")
@click.option("--locale", help="The locale you want the results in (ISO locale)", show_default="en-GBP", default="en-GB")
def skycli(ctx, key, country, currency, locale):
    ctx.ensure_object(defaultdict)
    ctx.obj['KEY'] = key
    ctx.obj['country'] = country
    ctx.obj['currency'] = currency
    ctx.obj['locale'] = locale
    if key == "":
        print("Rapid Key not set and not available from environment. Set SKYSCANNER_API_KEY environment variable\n")
        print(ctx.get_usage())
        exit(1)

@click.command(name="places")
@click.argument("query")
@click.pass_context
def get_places(ctx, query = None):
    """Get a list of places that match a query string."""
    
    api = RapidApi(ctx.obj['KEY'], ctx.obj['country'], ctx.obj['currency'], ctx.obj['locale'])
    response = api.con().list_places(query)
    api.log_json_response(response)

@click.command(name="markets")
@click.pass_context
def get_markets(ctx):
    """Retrieve the market countries that we support."""

    api = RapidApi(ctx.obj['KEY'], ctx.obj['country'], ctx.obj['currency'], ctx.obj['locale'])
    response = api.con().list_markets()
    api.log_json_response(response)

@click.command(name="currencies")
@click.pass_context
def get_currencies(ctx):
    """Retrieve the currencies that we support."""
    
    api = RapidApi(ctx.obj['KEY'], ctx.obj['country'], ctx.obj['currency'], ctx.obj['locale'])
    response = api.con().get_currencies()
    api.log_json_response(response)

@click.command(name="quotes")
@click.pass_context
@click.argument('origin')
@click.argument('destination')
@click.argument('outbounddate', type=SkyScannerDateTime())
@click.argument('inbounddate', type=SkyScannerDateTime(), required=False)
def get_quotes(ctx, origin, destination, outbounddate, inbounddate):
    """Retrieve the cheapest quotes from our cache prices."""

    api = RapidApi(ctx.obj['KEY'], ctx.obj['country'], ctx.obj['currency'], ctx.obj['locale'])
    response = api.con().browse_quotes(originplace=origin, \
        destinationplace=destination, \
        outboundpartialdate=outbounddate, \
        inboundpartialdate = inbounddate)
    api.log_json_response(response)

@click.command(name="routes")
@click.pass_context
@click.argument('origin')
@click.argument('destination')
@click.argument('outbounddate', type=SkyScannerDateTime())
@click.argument('inbounddate', type=SkyScannerDateTime(), required=False)
def get_routes(ctx, origin, destination, outbounddate, inbounddate):
    """ Retrieve the cheapest routes from our cache prices. 
        Similar to the Browse Quotes API but with the routes built for you from the individual quotes."""

    api = RapidApi(ctx.obj['KEY'], ctx.obj['country'], ctx.obj['currency'], ctx.obj['locale'])
    response = api.con().browse_routes(originplace=origin, \
        destinationplace=destination, \
        outboundpartialdate=outbounddate, \
        inboundpartialdate = inbounddate)
    api.log_json_response(response)

@click.command(name="live")
@click.pass_context
@click.argument('origin')
@click.argument('destination')
@click.argument('outbounddate', type=SkyScannerDateTime())
@click.argument('adults', type=click.INT, default = 1)
def get_live_prices(ctx, origin, destination, outbounddate, adults):
    """ Retrieve iterneraries from our LIVE prices. \n
        It first invokes CreateSession to obtain a session with the Live API.\n
        
        Arguments:\n
        origin\t\tPlace of origin (see skycli places command)\n
        destination\tPlace of destination (see skycli places command)\n
        outbounddate\tDate of departure in yyy-mm-dd or yyyy-mm format or anytime\n
        adults\t\tTotal number of adults in trip\n"""

    api = RapidApi(ctx.obj['KEY'], ctx.obj['country'], ctx.obj['currency'], ctx.obj['locale'])
    response = api.con().live_search(originplace=origin,
        destinationplace=destination,
        outbounddate=outbounddate,
        adults = adults)
    # api.log_json_response(response)
    click.secho(str(response), fg="cyan")



# Add all commands to group
skycli.add_command(get_places)
skycli.add_command(get_markets)
skycli.add_command(get_currencies)
skycli.add_command(get_quotes)
skycli.add_command(get_routes)
skycli.add_command(get_live_prices)

if __name__ == "__main__":
    skycli()
    