import requests
import click


@click.group(name="skycli")
def skycli():
    pass

@click.command(name="places",short_help="Retrieve the market countries that we support.", help="Retrieve the market countries that we support. Most suppliers (airlines, travel agents and car hire dealers) set their fares based on the market (or country of purchase). It is therefore necessary to specify the market country in every query.")
def get_places():
    url = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/autosuggest/v1.0/UK/GBP/en-GB/"

    querystring = {"query":"London"}

    headers = {
        'x-rapidapi-host': "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com",
        'x-rapidapi-key': "c8fb9eb818msh85b1d2bb25885f5p1cbcb2jsnc68f5a493539"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    click.echo(click.style(response.text, fg="cyan"))

# Add all commands to group
skycli.add_command(get_places)

if __name__ == "__main__":
    skycli()