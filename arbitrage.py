from collections import defaultdict
from operator import itemgetter
from time import time
from datetime import datetime
import config, csv

from binance.client import Client

FEE = 0.00075       # Binance VIP0 level spot-trade transaction fee for "Taker" (limit order)
ITERATIONS = 43200   # iterations to run
PRIMARY = ['ETH', 'USDT', 'USDC', 'XRP', 'DOGE', 'LTC', 'TRX', 'BTC', 'BNB', 'ADA', 'SOL', 'DOT', 'MATIC', 'BCH', 'WBTC', 'DAI', 'SHIB', 'AVAX', 'BUSD']
tri_count = 0
profit_count = 0

def main():
    csvfile = open('triangle', 'w', newline='', encoding='UTF8')
    result = csv.writer(csvfile, delimiter=',')
    count = 0
    global tri_count
    global profit_count
    
    while count < ITERATIONS:            #replaced with interations
        prices = get_prices()
        triangles = list(find_triangles(prices))
        if triangles:
            tri_count +=1
            for triangle in sorted(triangles, key=itemgetter('profit'), reverse=True):
                describe_triangle(prices, triangle, result, csvfile)
            print(f'> 0.05% trades = {(profit_count/tri_count)*100}%')
        count +=1
    
    # for primary, secondaries in prices.items():
    #     for secondary, price in secondaries.items():
    #         result.writerow([primary, secondary, price])

    csvfile.close()
    
def get_prices():
    client = Client(config.API_KEY, config.API_SECRET)
    prices = client.get_orderbook_tickers()
    dic = defaultdict(dict)
    # print(prices)
    
    for ticker in prices:
        symbol = ticker['symbol']
        ask = float(ticker['askPrice'])
        bid = float(ticker['bidPrice'])
        ask_qty = float(ticker['askQty'])
        bid_qty = float(ticker['bidQty'])
        
        if ask == 0.0 or bid_qty == 0.0 or ask_qty == 0.0:
            continue
        for primary_cur in PRIMARY:                            # USDT
            if symbol.endswith(primary_cur):
                secondary_cur = symbol[:-len(primary_cur)]     # BTC
                dic[primary_cur][secondary_cur] = {
                    'price': 1 / ask,      # USDT: BTC, ETH    
                    'ask_qty': ask_qty,
                    'bid_qty': bid_qty
                }
                dic[secondary_cur][primary_cur] = {
                    'price': bid,          # BTC: USDT, BNB
                    'ask_qty': ask_qty,
                    'bid_qty': bid_qty
                }
    return dic
    
def find_triangles(prices):
    triangles = []
    starting_coin = 'USDT'
    for triangle in recurse_triangle(prices, starting_coin, starting_coin):
        coins = set(triangle['coins'])
        if not any(prev_triangle == coins for prev_triangle in triangles):
            yield triangle
            triangles.append(coins)
    
    starting_coin = 'BUSD'
    for triangle in recurse_triangle(prices, starting_coin, starting_coin):
        coins = set(triangle['coins'])
        if not any(prev_triangle == coins for prev_triangle in triangles):
            yield triangle
            triangles.append(coins)

    starting_coin = 'USDC'
    for triangle in recurse_triangle(prices, starting_coin, starting_coin):
        coins = set(triangle['coins'])
        if not any(prev_triangle == coins for prev_triangle in triangles):
            yield triangle
            triangles.append(coins)

def recurse_triangle(prices, current_coin, starting_coin, depth_left = 3, amount = 1.0):
    if depth_left > 0:
        pairs = prices[current_coin]
        for coin,pair_data in pairs.items():
            price = pair_data['price']
            new_price = (amount * price) * (1.0 - FEE)
            for triangle in recurse_triangle(prices, coin, starting_coin, depth_left -1, new_price):
                triangle['coins'] = triangle['coins'] + [current_coin]
                yield triangle
    elif current_coin == starting_coin and amount > 1.0:
        yield{
            'coins': [current_coin],
            'profit': amount
        }
        

def describe_triangle(prices, triangle, result_writer, csvfile):
    global profit_count
    coins = triangle['coins']
    price_percentage = (triangle['profit'] - 1.0) * 100
    print(f"{datetime.now()} {'->'.join(coins):26} {round(price_percentage, 4):-7}% profit")

    if price_percentage >= 0.05:
        profit_count += 1     
        
        # Create a list of the coin prices
        coin_prices = []
        for i in range(len(coins) - 1):
            first = coins[i]
            second = coins[i + 1]
            coin_prices.append(f"{second:4} / {first:4}: \n{prices[second][first]['price']:-17.8f} \nask_qty: {prices[second][first]['ask_qty']} | bid_qty: {prices[second][first]['bid_qty']} \n")

        # Write all data to CSV in one row
        result_writer.writerow([datetime.now(), '->'.join(coins), str(round(price_percentage, 4))+'%\n', ''.join(coin_prices)+'\n------------------\n'])
        csvfile.flush()  # Flush the buffer to disk
        print('')


if __name__ == '__main__':
    main()