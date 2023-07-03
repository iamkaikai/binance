import config, csv
from binance.client import Client


client = Client(config.API_KEY, config.API_SECRET )


# place a test market buy order, to place an actual order use the create_order function
print(client.get_account())
