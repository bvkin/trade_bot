from backtesting import Strategy
from trade_bot.trading import BEARISH, BULLISH

def SIGNAL(df):
    return df.signal

class TradingStrategy(Strategy):
    def init(self):
        self.signal1 = self.I(SIGNAL, self.data)

    def next(self):
        super().next() 
        if self.signal1==BULLISH:
            self.position.close()
            self.buy(size=0.05)
        elif self.signal1==BEARISH:
            self.position.close()
            self.sell()
