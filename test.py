import config, csv
from binance.client import Client
from binance.enums import *


client = Client(config.API_KEY, config.API_SECRET )
client.API_URL = 'https://api.binance.com/api'

# get balance of account
def get_balance():
    account_info = client.get_account()
    non_zero_balances = [asset for asset in account_info['balances'] if float(asset['free']) + float(asset['locked']) > 0]
    print('\n----------------Balences----------------')
    for asset in non_zero_balances:
        print(f"{asset['asset']}, Free: {asset['free']}, Locked: {asset['locked']}")
    print('-------------------------------------------')
    
# get info
def get_info(symbol):
        info = client.get_symbol_info(symbol)
        print(info)
        # filters = info['filters']
        # min_notional_filter = [x for x in filters if x['filterType'] == 'NOTIONAL'][0]
        # min_notional = min_notional_filter['minNotional']
        # print(f"min qty = {min_notional}")
    
# make order
def make_order(coinpair, quoteQty):
    order = client.create_order(
        symbol = coinpair,
        side = SIDE_BUY,
        type = ORDER_TYPE_MARKET,
        quoteOrderQty = quoteQty
    )
    print(order)

# test trade
# get_balance()

    
def direction_check(list):
    print(list)
    coinpairs = [list[i]+list[i+1] for i in range(len(list)-1)]

    info = client.get_exchange_info()
    all_pairs = [symbol['symbol'] for symbol in info['symbols']]
    count = 0
    for pair in coinpairs:
        if pair in all_pairs: count +=1
        print(f"{pair}: {pair in all_pairs}")
        get_info(pair)
        
    if count == 3: 
        print('all work')
    else:
        print('some are broken')
    print('----------------------------')
    
coins = ['USDT','BTC','ETH','USDT']
direction_check(coins)
coins.reverse()
direction_check(coins)

# for i in coinpairs:
#     get_info(i)


# print('\nafter trading...')
# make_order('BTCUSDT', 10)
# get_balance()

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
