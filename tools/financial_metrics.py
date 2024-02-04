from ._entities import Price, DividendAmount, DividendPct, ParValue, Trade
from pydantic import ValidationError
import math
from collections import deque
import datetime

class CommonDividend(Price, DividendAmount):
    '''
    Common dividend is meant to be used directly in a service. 
    It is responsible to validate the inputs via inherited classes or inside
    its methods. But it will not raise an exception. If the dividend cannot be 
    calculated it will return None
    (eg zerodivision errors or none type inputs etc)
    '''
    def __init__(self, price, dividend_amount):
        super().__init__(price=price, dividend_amount=dividend_amount)

    def common_dividend(self):
        return self.dividend_amount / self.price

    @classmethod
    def calculate_common_dividend(cls, price, dividend_amount):
        try:
            cd = cls(price=price, dividend_amount=dividend_amount)
            return cd.common_dividend()
        except ValidationError as e:
            return None
        except (ZeroDivisionError, TypeError) as e:
            # Due to division this will handle the denominator of None or 0
            return None

class PreferredDividendYield(Price, DividendPct, ParValue):

    def __init__(self, price, dividend_pct, par_value):
        super().__init__(price=price, dividend_pct=dividend_pct, par_value=par_value)

    def prefered_dividend(self):
        return self.dividend_pct * self.par_value / self.price / 100

    @classmethod
    def calculate_prefered_dividend(cls, price, dividend_pct, par_value):
        try:
            cd = cls(price=price, dividend_pct=dividend_pct, par_value=par_value)
            return cd.prefered_dividend()
        except ValidationError as e:
            return None
        except (ZeroDivisionError, TypeError) as e:
            # Due to division this will handle the denominator of None or 0
            return None

class PERatio(Price, DividendAmount):
    def __init__(self, price, dividend_amount):
        super().__init__(price=price, dividend_amount=dividend_amount)

    def pe_ratio(self):
        return self.price / self.dividend_amount
    
    @classmethod
    def calculate_pe_ratio(cls, price, dividend_amount):
        try:
            cpe = cls(price=price, dividend_amount = dividend_amount)
            return cpe.pe_ratio()
        except ValidationError as e:
            return None
        except (ZeroDivisionError, TypeError) as e:
            return None 
        
class GeometricMean:
    def __init__(self, prices = None):
        self.prices = [Price(price=p) for p in prices] if prices else []
        
    def geometric_mean_log(self):
        # For large arrays use this as it avoids overflow error
        log_sum , length = 0,0
        for p in self.prices:
            _p = p.price
            if _p == 0:
                return 0
            log_sum += math.log(_p)
            length +=1
        return math.exp(log_sum/length) if length > 0 else None
    
    def geometric_mean(self):
        product , length = 0,0
        for p in self.prices:
            _p = p.price
            if _p == 0:
                return 0
            product *= _p
            length +=1
        return product ** (1 / length) if length > 0 else None

    @classmethod
    def calculate_geometric_mean_log(cls, prices):
        try:
            lgm = cls(prices = prices)
            return lgm.geometric_mean_log()
        except (ZeroDivisionError, TypeError) as e:
            return None
        except ValidationError as e:
            return None
        
    @classmethod
    def calculate_geometric_mean(cls, prices):
        try:
            lgm = cls(prices = prices)
            return lgm.geometric_mean_log()
        except (ZeroDivisionError, TypeError) as e:
            return None
        except ValidationError as e:
            return None
        except OverflowError as e:
            return lgm.geometric_mean_log()

class VolWeightedPrice:
    def __init__(self):
        self.mkt_value = 0
        self.ttl_shares = 0

    def add_trade(self, trade: Trade):
        self.mkt_value += trade.price * trade.quantity
        self.ttl_shares += trade.quantity

    def current_vol_weighted_price(self):
        if self.ttl_shares >0:
            return self.mkt_value / self.ttl_shares
        return None
    
    def calculate(self, trades: [Trade]):
        for trade in trades:
            self.add_trade(Trade(**trade))
        return self.current_vol_weighted_price()
    
class TradeManager:
    def __init__(self):
        self.trades = deque()

    def add_trade(self, trade: Trade):
        self.trades.append(trade)

    def sliced_trades(self, period = 15):
        current_time = datetime.datetime.now()
        while self.trades[0].timestamp < current_time - datetime.timedelta(minutes=period):
            self.trades.popleft()
        return self.trades


gm = GeometricMean(prices=[0,10,20])
gm.geometric_mean()

import random
import datetime

def generate_trades(nrecords = 100):
    i = 0
    while i < nrecords:
        yield {
            "price": random.randint(1, 250),
            "quantity": random.randint(1, 500),
            "timestamp": (datetime.datetime.now() - datetime.timedelta(minutes=14)).strftime("%Y-%m-%d %H:%M:%S"),
            "order": random.choice(['BUY', 'SELL'])
        }
        i +=1


# How to calculate VWP assuming the prices are in the last 15 min
trades = generate_trades()

trade_manager = TradeManager()
for trade in trades:
    trade_manager.add_trade(trade)

vwp = VolWeightedPrice()
for trade in trades:
    vwp.add_trade(Trade(**trade))
print(vwp.current_vol_weighted_price())






# prices = [10, 20, 100, 5]
# result = GeometricMean.calculate_log_geometric_mean(prices)
# print(result)
# result = GeometricMean.calculate_geometric_mean(prices)
# print(result)
# # Example usage
# price_value = 100
# dividend_amount_value = 2.4

# result = CommonDividend.calculate_common_dividend(price=price_value, dividend_amount=dividend_amount_value)
# print(result)

# price_value = 100
# dividend_pct = "2%"
# par_value = 120

# result = PreferredDividendYield.calculate_prefered_dividend(price=price_value, dividend_pct=dividend_pct, par_value=par_value)
# print(result)
# result = PERatio.calculate_pe_ratio(price=price_value, dividend_amount=dividend_amount_value)
# print("pe",result)















# class CommonDividend(Price, DividendAmount):

#     def dividend_handler(func):
#         def wrapper(*args, **kwargs):
#             try:
#                 return func(*args, **kwargs)
#             except (ZeroDivisionError, TypeError):
#                 # Due to division this will handle the denominator of None or 0
#                 return None
#         return wrapper

#     @dividend_handler
#     def common_dividend(self):
#         return self.dividend_amount / self.price


# def common_dividend(price, dividend_amount):
#     try:
#         cd = CommonDividend(price=price, dividend_amount=dividend_amount)
#         return cd.common_dividend()
#     except ValidationError as e:
#         print(e)
#         return None
    

# try:
#     cd = CommonDividend(price=None, dividend_amount=2)
# except ValidationError:
#     exit(-1)
# a = cd.common_dividend()

# print(a)
