import numpy as np
import pandas as pd

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