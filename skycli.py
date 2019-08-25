import requests
import click
import os
from json import dumps

from connection import Connection
from skyscanner_datetime import SkyScannerDateTime

class RapidApi(object):
    def __init__(self, country = "UK", currency = "GBP", locale = "en-GB"):
        self.country = country
        self.currency = currency
        self.locale = locale

    def con(self, key = None):
        if key is None:
            raise ConnectionError("API key not provided")
        return Connection(key = key, country = self.country, currency = self.currency, locale=self.locale) 

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
    ctx.ensure_object(dict)
    ctx.obj['KEY'] = key

@click.command(name="places")
@click.argument("query")
@click.pass_context
def get_places(ctx, query = None):
    """Get a list of places that match a query string."""
    
    key = ctx.obj['KEY']
    api = RapidApi()
    response = api.con(key).list_places(query)
    api.log_json_response(response)

@click.command(name="markets")
@click.pass_context
def get_markets(ctx):
    """Retrieve the market countries that we support."""

    key = ctx.obj['KEY']
    api = RapidApi()
    response = api.con(key).list_markets()
    api.log_json_response(response)

@click.command(name="currencies")
@click.pass_context
def get_currencies(ctx):
    """Retrieve the currencies that we support."""
    
    key = ctx.obj['KEY']
    api = RapidApi()
    response = api.con(key).get_currencies()
    api.log_json_response(response)

@click.command(name="quotes")
@click.pass_context
@click.argument('origin')
@click.argument('destination')
@click.argument('outbounddate', type=SkyScannerDateTime())
@click.argument('inbounddate', type=SkyScannerDateTime(), required=False)
def get_quotes(ctx, origin, destination, outbounddate, inbounddate):
    """Retrieve the cheapest quotes from our cache prices."""

    key = ctx.obj['KEY']
    api = RapidApi()
    response = api.con(key).browse_quotes(originplace=origin, \
        destinationplace=destination, \
        outboundpartialdate=outbounddate, \
        inboundpartialdate = inbounddate)
    api.log_json_response(response)

# Add all commands to group
skycli.add_command(get_places)
skycli.add_command(get_markets)
skycli.add_command(get_currencies)
skycli.add_command(get_quotes)

if __name__ == "__main__":
    skycli()