from backtesting import Strategy
from trade_bot.trading import BEARISH, BULLISH

def SIGNAL(df):
    return df.signal

class TradingStrategy(Strategy):
    def init(self):
        self.signal1 = self.I(SIGNAL, self.data)

    def next(self):
        price = self.data.Close[-1]

        if self.signal1==BULLISH:
            self.buy(tp=1.15*price, sl=0.95*price)
        elif self.signal1==BEARISH:
            self.position.close()
