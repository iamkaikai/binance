import config, csv
from binance.client import Client
from binance.enums import *


client = Client(config.API_KEY, config.API_SECRET )
client.API_URL = 'https://api.binance.com/api'

#get balance of account
def get_balance():
    account_info = client.get_account()
    non_zero_balances = [asset for asset in account_info['balances'] if float(asset['free']) + float(asset['locked']) > 0]
    print('\n----------------Balences----------------')
    for asset in non_zero_balances:
        print(f"{asset['asset']}, Free: {asset['free']}, Locked: {asset['locked']}")
    print('-------------------------------------------')
    
    
# test trade
get_balance()

info = client.get_symbol_info('BTCUSDT')
filters = info['filters']
min_notional_filter = [x for x in filters if x['filterType'] == 'NOTIONAL'][0]
min_notional = min_notional_filter['minNotional']
print(f"min qty = {min_notional}")

order = client.create_order(
    symbol = 'BTCUSDT',
    side = SIDE_BUY,
    type = ORDER_TYPE_MARKET,
    quoteOrderQty = 10
)

print('\nafter trading...')
print(order)
get_balance()

# # set testnet

# client = Client(API_KEY_test, API_SECRET_test)
# client.API_URL = 'https://testnet.binance.vision/api'

# # define the quantity and price
# quantity = '1'  # This will need to be adjusted depending on the current price of BTC
# # you might want to get the actual price before buying:
# btc_price = client.get_symbol_ticker(symbol="BTCUSDT")
# print(f"Current BTC price is {btc_price['price']}")

# # create a test market buy order
# order = client.create_test_order(
#     symbol = 'BTCUSDT',
#     side = SIDE_BUY,
#     type = ORDER_TYPE_MARKET,
#     quantity = quantity
# )

# print(order)
