from backtesting import Strategy
from core.models.trade_signal import TradeSignal

def SIGNAL(df):
    return df.signal

class TradingStrategy(Strategy):
    def init(self):
        self.signal1 = self.I(SIGNAL, self.data)

    def next(self):
        price = self.data.Close[-1]

        if self.signal1==TradeSignal.BULLISH.value:
            self.buy(tp=1.15*price, sl=0.95*price)
        elif self.signal1==TradeSignal.BEARISH.value:
            self.position.close()
