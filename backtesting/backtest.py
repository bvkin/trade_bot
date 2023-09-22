import numpy as np
import pandas as pd


def backtest(data, strategy):
  """
  Backtests a trading strategy on historical data.

  Args:
    data: A pandas DataFrame of historical prices.
    strategy: A function that takes a DataFrame of prices and returns a trading signal.

  Returns:
    A pandas DataFrame of the backtest results.
  """

  prices = data["Close"]
  signals = strategy(prices)

  returns = prices.pct_change()
  positions = np.where(signals > 0, 1, -1)
  trades = positions.diff()

  returns_with_fees = returns * (1 - 0.001)
  pnl = (trades * returns_with_fees).sum()

  backtest_results = pd.DataFrame({
      "Date": data.index,
      "Close": prices,
      "Signal": signals,
      "Positions": positions,
      "Returns": returns,
      "Returns with fees": returns_with_fees,
      "PnL": pnl
  })

  return backtest_results





class Backtester:
    def __init__(self, data, strategy):
        self.data = data
        self.strategy = strategy
        self.positions = []
        self.balance = 0

    def run(self):
        for i in range(len(self.data)):
            self.strategy.update(self.data.iloc[i])
            self.positions.append(self.strategy.get_position())
            self.balance += self.strategy.get_profit()

    def get_results(self):
        return self.balance, self.positions

class Strategy:
    def __init__(self):
        self.position = None

    def update(self, data):
        pass

    def get_position(self):
        return self.position

    def get_profit(self):
        pass

# Example strategy:

class BuyAndHoldStrategy(Strategy):
    def __init__(self):
        super().__init__()
        self.position = 0

    def update(self, data):
        self.position = 1

    def get_profit(self):
        return self.position * (data['close'] - data['open'])

# Example usage:

data = pd.DataFrame({
    'open': [100, 101, 102, 103],
    'close': [101, 102, 103, 104]
})

strategy = BuyAndHoldStrategy()
backtester = Backtester(data, strategy)
backtester.run()

balance, positions = backtester.get_results()

print(balance)
print(positions)