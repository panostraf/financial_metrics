from stock.stock import Stock
from tools._entities import Trade
import pytest
import datetime


@pytest.fixture(scope='function')
def stock_symbol(symbol):
    return Stock(symbol)



@pytest.mark.parametrize("symbol, result", [
    ("ALE","ALE")
])
def test_initialize_stock(symbol, result):
    s = Stock(symbol=symbol)
    assert s.symbol == result

@pytest.mark.parametrize("symbol, result", [
    ("InvalidSymbol",ValueError)
])
def test_fail_initialize_stock(symbol, result):
    with pytest.raises(result):
        s = Stock(symbol=symbol)


# DIVIDEND YIELD
@pytest.mark.parametrize("symbol, price, result", [
    ("ALE", 20, 1.15),
    ("POP", 100, 0.08),
    ("TEA", 200, None),
    ("GIN", 100, 0.02)
    ])
def test_stock_dividend_yield( symbol, price, result):
    s = Stock(symbol=symbol)
    assert s.get_dividend_yield(price) == result

@pytest.mark.parametrize("symbol, price, result", [
    ("INVALID", 20, ValueError),
    ("POP", -1, ValueError),
    (None, 200, ValueError)
    ])
def test_stock_dividend_yield_fail( symbol, price, result):
    with pytest.raises(result):
        s = Stock(symbol=symbol)
        s.get_dividend_yield(price)

# PE RATIO
@pytest.mark.parametrize("symbol, price, result", [
    ("POP", 100, 12.5),
    ("TEA", 200, None),
    ])
def test_stock_pe_ratio( symbol, price, result):
    s = Stock(symbol=symbol)
    assert s.get_pe_ratio(price) == result

@pytest.mark.parametrize("symbol, price, result", [
    ("POP", -1, ValueError),
    ("Invalid", 200, ValueError)
    ])
def test_stock_pe_ratio_fail( symbol, price, result):
    with pytest.raises(result):
        s = Stock(symbol=symbol)
        s.get_pe_ratio(price)


# VOLUME WEIGTHED STOCK PRICE
def test_vol_weight_stock_price():
    trades = [{
        "price": 120,
        "quantity": 100,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "order": 1,
    },{
        "price": 200,
        "quantity": 100,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "order": 1,
    }]

    s = Stock(symbol="GIN")
    [s.record_trade(**trade) for trade in trades]
    result = s.get_weighted_stock_price() 
    assert result == 160 #  ( (120 * 100) + (200 * 100) ) / (100 + 100)

def test_vol_weight_stock_price_fail():
    trades = [{
        "price": 120,
        "quantity": 0,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "order": 1,
    },{
        "price": 200,
        "quantity": 100,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "order": 1,
    }]
    with pytest.raises(ValueError):
        s = Stock(symbol="GIN")
        [s.record_trade(**trade) for trade in trades]
        result = s.get_weighted_stock_price() 
        assert result == 160 #  ( (120 * 100) + (200 * 100) ) / (100 + 100)


