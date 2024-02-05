from tools._entities import Price, DividendAmount, DividendPct, Quantity, ParValue, Trade, Order
import pytest
import datetime

### TEST PRICE
@pytest.mark.parametrize("price, expected_result", [
    (2, 2.0),
    ("20", 20.0),
    # (0, 0.0)
])
def test_price_entity_success(price, expected_result):
    p = Price(price=price)
    assert p.price == expected_result
    assert type(p.price) == float

@pytest.mark.parametrize("price, expected_exception", [
    (None, ValueError),
    ("-2.3", ValueError),
    (-1, ValueError),
    ("Invalid", ValueError),
    (0, ValueError)
])
def test_price_entity_exception(price, expected_exception):
    
    with pytest.raises(expected_exception):
        p = Price(price=price)

### TEST DIVIDEND AMOUNT
@pytest.mark.parametrize("dividend, expected_result", [
    (2, 2.0),
    ("20", 20.0),
    (0, 0.0),

])
def test_dividend_entity_success(dividend, expected_result):
    d = DividendAmount(dividend_amount=dividend)
    assert d.dividend_amount == expected_result
    assert type(d.dividend_amount) == float

@pytest.mark.parametrize("dividend, expected_exception", [
    ("-2.3", ValueError),
    (-1, ValueError),
    ("Invalid", ValueError),
    (["dfew",['fwef']], ValueError),
    (None, ValueError)
])
def test_dividend_entity_exception(dividend, expected_exception):
    with pytest.raises(expected_exception):
        d = DividendAmount(dividend_amount=dividend)

### TEST DIVIDENT PCT
@pytest.mark.parametrize("dividend, expected_result", [
    (2, 2.0),
    ("20", 20.0),
    ("2%", 2.0),
    
])
def test_dividend_pct_entity_success(dividend, expected_result):
    d = DividendPct(dividend_pct=dividend)
    assert d.dividend_pct == expected_result
    assert type(d.dividend_pct) == float
        
@pytest.mark.parametrize("dividend, expected_exception", [
    (None, ValueError),
    ("-2.3", ValueError),
    (-1, ValueError),
    ("Invalid", ValueError),
    (["dfew",['fwef']], ValueError),
    ("0%", ValueError),
    (0, ValueError),
])
def test_dividend_pct_entity_exception(dividend, expected_exception):
    with pytest.raises(expected_exception):
        d = DividendPct(dividend_pct=dividend)

### TEST QUANTITY
@pytest.mark.parametrize("quantity, expected_result", [
    (2, 2.0),
    ("20", 20.0),
    (3.0, 3.0)
])
def test_quantity_entity_success(quantity, expected_result):
    q = Quantity(quantity=quantity)
    
    assert q.quantity == expected_result
    assert type(q.quantity) == float

@pytest.mark.parametrize("quantity, expected_exception", [
    (None, ValueError),
    ("-2.3", ValueError),
    (-1, ValueError),
    ("Invalid", ValueError),
    (0, ValueError),
    ("0", ValueError)
])
def test_quantity_entity_exception(quantity, expected_exception):
    
    with pytest.raises(expected_exception):
        q = Quantity(quantity=quantity)

### TEST PAR VALUE
@pytest.mark.parametrize("par_value, expected_result", [
    (2, 2.0),
    ("20", 20.0),
    (3.0, 3.0)
])
def test_par_value_entity_success(par_value, expected_result):
    pv = ParValue(par_value=par_value)
    
    assert pv.par_value == expected_result
    assert type(pv.par_value) == float

@pytest.mark.parametrize("par_value, expected_exception", [
    (None, ValueError),
    ("-2.3", ValueError),
    (-1, ValueError),
    ("Invalid", ValueError),
    (0, ValueError),
    ("0", ValueError)
])
def test_par_value_entity_exception(par_value, expected_exception):
    
    with pytest.raises(expected_exception):
        ParValue(par_value=par_value)

### TEST ORDER
@pytest.mark.parametrize("order,expected_result,expected_literal" ,[
    ("buy", 1, "BUY"),
    ("sEll", 0, "SELL"),
    (1, 1,  "BUY")
])
def test_order(order, expected_result, expected_literal):
    o = Order(order=order)
    assert o.order.value == expected_result
    assert o.order.name == expected_literal

@pytest.mark.parametrize("order,expected_exception" ,[
    ("buy1", ValueError),
    (3,  ValueError)
])
def test_order_fail(order, expected_exception):
    with pytest.raises(expected_exception):
        o = Order(order=order)
    
### TEST TRADE
# since trade is based on price quantity and order classes it does not require any further test on these inputs
@pytest.mark.parametrize("price, quantity, order, timestamp", [
    (10, 10, 1, "2022-02-01 00:10:10"),
])
def test_trade(price, quantity, order, timestamp):
    t = Trade(price=price, quantity=quantity, order=order, timestamp=timestamp)
    t.timestamp == datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")

@pytest.mark.parametrize("price, quantity, order, timestamp", [
    (10, 10, 1, "2022-02-01 00:10:10:01"),
    (-10, 10, 1, "2022-02-01 00:10:10"),
    (10, None, 1, "2022-02-01 00:10:10")
])
def test_trade_fail(price, quantity, order, timestamp):
        with pytest.raises(ValueError):
            Trade(price=price, quantity=quantity, order=order, timestamp=timestamp)
