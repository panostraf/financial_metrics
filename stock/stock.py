from collections import deque
from tools import financial_metrics
from tools._entities import Trade
from stock.cfg import stock_data
from datetime import datetime, timedelta


class Stock:
    def __init__(self, symbol):
        self.MINUTES = 15
        self.symbol = symbol
        self.trades = []
        self.recent_trades = deque()
        self.stock_data = self.get_symbol_info()
    
    def get_symbol_info(self) -> dict:
        try:
            return stock_data[self.symbol]
        except KeyError:
            raise ValueError(f"Not symbol found with name {self.symbol}")

    def get_dividend_yield(self, price: float) -> float | None:
        if self.stock_data['Type'] == "Common":
            d = financial_metrics.CommonDividend.calculate_common_dividend(
                price=price, 
                dividend_amount=self.stock_data['Last Dividend']
                )
            return d if d else None

        if self.stock_data['Type'] == "Preferred":
            d = financial_metrics.PreferredDividendYield.calculate_prefered_dividend(
                price = price,
                dividend_pct=self.stock_data['Fixed Dividend'],
                par_value=self.stock_data['Par Value']
                )
            return d if d else None
        
    def get_pe_ratio(self, price : float) -> float | None:
        pe_ratio = financial_metrics.PERatio.calculate_pe_ratio(
            price=price,
            dividend_amount=self.stock_data['Last Dividend']
        )
        return pe_ratio if pe_ratio else None

    def record_trade(self,price :float, quantity: float, timestamp:datetime, order:bool | str):
        trade = financial_metrics.Trade(
            price=price,
            quantity=quantity,
            order = order,
            timestamp=timestamp
        )
        self.trades.append(trade)
 
    def get_weighted_stock_price(self) -> float | None:
        current_time = datetime.now()
        recent_trades_interval = current_time - timedelta(minutes=self.MINUTES)
        
        vwp = financial_metrics.VolWeightedPrice()
        number_of_trades = 0
        for record in self.trades[::-1]:
            number_of_trades += 1
            if record.timestamp >= recent_trades_interval:
                vwp.add_trade(record)
            else:
                break

        # remove every record not in 15 min from this list to offload memory
        self.trades = self.trades[-number_of_trades:]
        result = vwp.current_vol_weighted_price()
        return result if result else None
