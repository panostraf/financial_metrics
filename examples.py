from stock.stock import Stock
from tools.financial_metrics import GeometricMean
from stock.cfg import stock_data
import datetime, random
from pydantic import ValidationError

SYMBOL = "TEA"
PRICE = 100

print("symbol:", SYMBOL)
print("price", PRICE)
print("_________________")
try:
    stock_symbol = Stock(SYMBOL)
except ValueError:
    print(f"Symbol {SYMBOL} not found")
    exit()

#Calculate dividend yield
dividend_yield = stock_symbol.get_dividend_yield(price=PRICE)
print("Dividend:" , round(dividend_yield,2) * 100 if dividend_yield else "NA")

#Calculate pe ratio
pe_ratio = stock_symbol.get_pe_ratio(price=PRICE)
print("PE Ratio:", round(pe_ratio, 2) if pe_ratio else "NA")


# Record a trade
trade = {
    "price": random.randint(1, 250),
    "quantity": random.randint(1, 500),
    "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "order": random.choice(['BUY', 'SELL'])
}
stock_symbol.record_trade(**trade)
t = stock_symbol.trades[0].trade
print("Trade: ", t if t else "NA")

# print("", stock_symbol.trades)


# Calculate Volume weighted averege of all trades in the last 15 minutes
# To do such a calculation and have a meaningfull result it means that 
# come trades occured. For demostrative purposes we will have a loop that will 
# populate the obejct with a few trades
def trade_generator():
    # Assume a trade per minute
    seconds = 1800 # 30min
    for _ in range(10000):
        yield random.choice(['TEA', 'POP', 'ALE', 'GIN', 'JOE']), {
            "price": random.randint(1, 250),
            "quantity": random.randint(1, 500),
            "timestamp": (datetime.datetime.now() - datetime.timedelta(seconds=seconds)).strftime("%Y-%m-%d %H:%M:%S"),
            "order": random.choice(['BUY', 'SELL'])
        }
        seconds -= 2
        if seconds <= 0:
            return

for ticker,trade in trade_generator():
    if ticker == SYMBOL:
        stock_symbol.record_trade(**trade)

vwp = stock_symbol.get_weighted_stock_price()
print("Volume weigthed price:", round(vwp, 2) if vwp else "NA")


### CALCULATE GBCE index
# Assume we have a key:value pair with stock symbols and prices
stock_prices = dict(zip(stock_data.keys(), [random.randint(0,250) for i in range(5)]))
try:
    gm = GeometricMean.calculate_geometric_mean_log(prices=stock_prices.values())
    print("GBCE :", round(gm,2) if gm else "NA")
except ValueError:
    print("GBCE : NA")
