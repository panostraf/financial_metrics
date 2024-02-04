from tools.financial_metrics import CommonDividend, PreferredDividendYield
from tools._entities import Price


stock_data = {
    'TEA': {'Type': 'Common', 'Last Dividend': 0, 'Par Value': 100},
    'POP': {'Type': 'Common', 'Last Dividend': 8, 'Par Value': 100},
    'ALE': {'Type': 'Common', 'Last Dividend': 23, 'Par Value': 60},
    'GIN': {'Type': 'Preferred', 'Last Dividend': 8, 'Fixed Dividend': '2%', 'Par Value': 100},
    'JOE': {'Type': 'Common', 'Last Dividend': 13, 'Par Value': 250}
}

cd = CommonDividend(price=10, dividend_amount=1)
print(cd.common_dividend())