from ._entities import Price, DividendAmount, DividendPct, ParValue, Trade
from pydantic import ValidationError
import math


class CommonDividend(Price, DividendAmount):
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
            raise e
        except (ZeroDivisionError, TypeError) as e:
            # Due to division this will handle the denominator of None or 0
            return None
        except Exception as e:
            raise e

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
            raise e
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
            raise e
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
            raise None
        except ValidationError as e:
            raise e
        
    @classmethod
    def calculate_geometric_mean(cls, prices):
        try:
            lgm = cls(prices = prices)
            return lgm.geometric_mean_log()
        except (ZeroDivisionError, TypeError) as e:
            raise None
        except ValidationError as e:
            raise e
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
    
    def reset(self):
        self.mkt_value = 0
        self.ttl_shares = 0
