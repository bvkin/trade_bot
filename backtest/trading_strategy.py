from backtesting import Strategy
from core.models.trade_signal import TradeSignal
from core.trading.moving_averages import MovingAverages

def SIGNAL(df):
    return df.signal

class TradingStrategy(Strategy):
    def init(self):
        self.ma = MovingAverages(self.data.Close)
        self.short_window_ma = self.I(self.ma.gen_moving_average, 5)
        self.long_window_ma = self.I(self.ma.gen_moving_average, 20)

    def next(self):
        price = self.data.Close[-1]
        signal = self.ma.signal(self.short_window_ma, self.long_window_ma)

        if signal == TradeSignal.BULLISH:
            self.buy(tp=1.15*price, sl=0.95*price)
        elif signal==TradeSignal.BEARISH:
            self.position.close()
