from tools.financial_metrics import CommonDividend, PreferredDividendYield, PERatio, GeometricMean,VolWeightedPrice
import pytest


### TEST COMMON DIVIDEND YIELD
@pytest.mark.parametrize("price, dividend_amount, result", [
    (10,10, 1),
    ("10", "10", 1),
    (1,0,0),
    (0,0,None)
])
def test_common_dividend(price, dividend_amount, result):
    assert CommonDividend.calculate_common_dividend(price, dividend_amount) == result
    if not (price == 0 and dividend_amount == 0):
        assert type(CommonDividend.calculate_common_dividend(price, dividend_amount)) == float


### TEST PREFERED DIVIDEND YIELD
@pytest.mark.parametrize("price, dividend_pct, par_value, result", [
    (10,10, 10, .1),
    ("10", "2%", "120" , 0.24),
    ("0", "0%", "250", None),
    ("0", "-10%", "250", None),
    (None, "0%", "250", None),
])
def test_prefered_dividend(price, dividend_pct, par_value, result):
    assert PreferredDividendYield.calculate_prefered_dividend(
        price = price,
        dividend_pct = dividend_pct,
        par_value = par_value
    ) == result

### TEST PE RATIO
@pytest.mark.parametrize("price, dividend_amount, result", [
    (100, 2, 50),
    ("100", 2, 50),
    ("-1", 1, None),
    (None, 1, None)
])
def test_pe_ratio(price, dividend_amount, result):
    assert PERatio.calculate_pe_ratio(price=price, dividend_amount=dividend_amount) == result

### TEST GEOMETRIC MEAN
@pytest.mark.parametrize("prices, result", [
    ([10,20,2.5,"1"], 4.728708045016),
    ([ 0, 10, 10], 0),
    (None, None),
    ([None, 10,20,30], None)
])
def test_geometric_mean(prices, result):
    assert GeometricMean.calculate_geometric_mean(prices=prices) == pytest.approx(result)
    assert GeometricMean.calculate_geometric_mean_log(prices=prices) == pytest.approx(result)

### TEST VOLUME WEIGHTED AVERAGE
@pytest.mark.parametrize("market_value, quantity, result", [
    (20000, 150, 133.333333),
    (0, 100, 0),
    (100, 0 , None)
])
def test_volume_weigthed_average(market_value, quantity, result):
    vwp = VolWeightedPrice()
    vwp.mkt_value = market_value
    vwp.ttl_shares = quantity
    assert vwp.current_vol_weighted_price() == pytest.approx(result)