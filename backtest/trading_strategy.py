from backtesting import Strategy
from trade_bot.trading import BEARISH, BULLISH

class TadingStrategy(Strategy):
    def SIGNAL(self):
        return self.data.signal
    
    def init(self):
        super().init()
        self.signal1 = self.I(self.SIGNAL)

    def next(self):
        super().next() 
        if self.signal1==BULLISH:
            self.buy()
        elif self.signal1==BEARISH:
            self.sell()
