# Description:
A scalable and easy to use financial application that performs various stock-related calculations for a given set of stocks. The application is capable of calculating the dividend yield, P/E Ratio, recording trades, calculating the Volume Weighted Stock Price based on trades in the past 15 minutes, and computing the GBCE All Share Index.


# Installation

Version 
```
python==3.10.6
```
Clone repo
```
git clone https://github.com/panostraf/financial_metrics.git
cd financial_metrics
```
Create a virtual enviroment
```python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
Examples
```
python examples.py
```
Also you can use pytest to run the unit test with the following command

```
pytest unit_test/ -v
```

# Formulas:

- Dividend Yield (Common): Last Dividend / Price
- Dividend Yield (Preferred): (Fixed Dividend * Par Value) / Price
- P/E Ratio: Price / Dividend
- Geometric Mean: √(p1 * p2 * p3 * ... * pn) / n
- Volume Weighted Stock Price: ∑ (Traded Price * Quantity) / ∑ Quantity


Structure:
 - tools/
    - entitities.py
    - financial_metrics.py
  - stock/
    - cfg.py
    - stock.py
  - unit_test/
  

# Entities

Classes that define basic variables. They create constrains that will automatically executed when they initialised. Its purpose is to restrict data types and inputs. These classes are meant to be used across the project indipedently or via inheritance to provide a predictable and consistent output. Also they help to avoid code duplication and coding errors.

If the value does not match the requirements a ValueError will be raised. 

Entities have been build with pydantic, although custom classes that achieve similar functionallity can be created.

Available classes:
 - Price : float positive
 - DividendAmount : float zero or positive
 - DividendPct : float positive
 - Quantity : float positive
 - ParValue : float positive
 - Order : bool or str [BUY, SELL]
 - Trade : 
   - inherites (Price, Quantity, Order)
   - timestamp : datetime


# Financial Metrics

Classes for financial calculations related to stocks. It includes functionalities for calculating common and preferred dividends, P/E ratio, geometric mean, volume-weighted stock price, and managing trades. The module ensures error handling and uses Pydantic for data validation, offering a flexible and robust solution for financial computations.

Available classes:

- CommonDividend
- PreferredDividendYield
- PERatio
- GeometricMean
- WeigthedPrice

## CommonDividend Class

Represents a common dividend calculator for a stock.

Attributes:
  - price : Price
  - dividend_amount : DividendAmount

Returns:
  - float or None if dividend cannot be calculated

Raises:
  - ValidationError if invalid input is provided

Usage:

    CommonDividend.calculate_common_dividend(price=price, dividend_amount = dividend_amount)


## PreferredDividendYield Class

Attributes:
  - price Price
  - dividend_pct : DividendPct
  - par_value : ParValue

Returns:
  - float or None: Preferred dividend yield, or None if the calculation is not possible.

Raises:
    ValidationError: If input validation fails.

Usage:

    PreferredDividendYield.calculate_prefered_dividend(
        price=price_value,
        dividend_pct=dividend_pct_value,
        par_value=par_value_value
    )

## PERatio

Attributes:
  - price : Price
  - dividend_amount : DividendAmount

Returns:
  float or None: pe ratio (float) or (None) if the calculation is not possible.

Raises: ValidationError If input validation fails.

Usage: 

    financial_metrics.PERatio.calculate_pe_ratio(
                price=price,
                dividend_amount=dividend_amount
            )


## VolWeightedPrice

Calculated the volume weighted price of a set of trades for a given stock. 

Attributes: 
  No Attributes

Methods:
  - calculate(self, trades: [Trade]) -> float | None
  
Returns: 
  float | None (None if the list has empty)

Raises:
  No exceptions are raised

Usage:

This class can be used with 2 different ways: 
- Option 1

  ```
  VolWeightedPrice.calculate(trades = Trade(**trade))
  ```

- Option 2 : This method does the same proccess as Option1 but can be used in cases you don't have access to the trades in a form of a list. One each add_trade() it adds in the properties market value (quantity * price ) and total shares of the class. 
Then current_vol_weigthed_price() returns the result based on the current state.

  Essentially it acts like a map-reduce but sequentially
  ```
    vwp = VolWeightedPrice()
    for trade in trades:
      vwp.add_trade(Trade(**trade))
    result = vwp.current_vol_weighted_price()
  ```

# Stock

This is the exposed class that contains some logic besides validation and calulations.


Attributes:
  - symbol (str): Required parameter - The symbol of the stock.
  - MINUTES (int): Default = 15 Time interval for recent trades calculation
  - stock_data (dict): Stock information from the stock_data configuration.

Returns: 

float or None: Calculated financial metrics, or None if the calculation is not possible.

Raises:

 ValueError: If the stock symbol is not found in the stock_data configuration.


Methods:
- get_symbol_info(): Retrieves stock information based on the symbol.
- get_dividend_yield(price: float) -> Optional[float]: Calculates and returns the dividend yield for the stock.
  ```
  SYMBOL = "ALE"
  PRICE = 100

  try:
      stock_symbol = Stock(SYMBOL)
  except ValueError:
      print(f"Symbol {SYMBOL} not found")
      exit()

  #Calculate dividend yield
  dividend_yield = stock_symbol.get_dividend_yield(price=PRICE)
  print("Dividend:" , round(dividend_yield,2) * 100 if dividend_yield else "NA")
  ```

- get_pe_ratio(price: float) -> Optional[float]: Calculates and returns the P/E ratio for the stock.

  ```
  SYMBOL = "ALE"
  PRICE = 100

  try:
      stock_symbol = Stock(SYMBOL)
  except ValueError:
      print(f"Symbol {SYMBOL} not found")
      exit()

  pe_ratio = stock_symbol.get_pe_ratio(price=PRICE)
  print("PE Ratio:", round(pe_ratio, 2) if pe_ratio else "NA")
  ```

- record_trade(price: float, quantity: int, timestamp: datetime, order: str): Records a trade for the stock.
  ```
  SYMBOL = "ALE"
  PRICE = 100

  try:
      stock_symbol = Stock(SYMBOL)
  except ValueError:
      print(f"Symbol {SYMBOL} not found")
      exit()

  # demo trade
  trade = {
      "price": PRICE,
      "quantity": random.randint(1, 500),
      "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
      "order": random.choice(['BUY', 'SELL'])
  }

  stock_symbol.record_trade(**trade)
  t = stock_symbol.trades[0].trade
  print("Trade: ", t if t else "NA")
  ```

- get_weighted_stock_price() -> Optional[float]: Calculates and returns the volume-weighted stock price for the last 15 minutes.

  ```
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

  SYMBOL = "ALE"
  try:
      stock_symbol = Stock(SYMBOL)
  except ValueError:
      print(f"Symbol {SYMBOL} not found")
      exit()

  for ticker,trade in trade_generator():
      if ticker == SYMBOL:
          stock_symbol.record_trade(**trade)

  vwp = stock_symbol.get_weighted_stock_price()
  print("Volume weigthed price:", round(vwp, 2) if vwp else "NA")
  ```


#### You can see and run examples in example.py



