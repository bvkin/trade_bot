from backtesting import Strategy
from core.models.trade_signal import TradeSignal
from core.trading.moving_averages import MovingAverages

class MovingAveragesStrategy(Strategy):
    short_window = 5
    long_window  = 20

    def init(self):
        self.strat = MovingAverages(self.data.df, self.short_window, self.long_window)
        self.close = self.I(self.strat.get_indicator, "close", plot=False, name="close")
        self.short_window_ma = self.I(self.strat.get_indicator, "short_window_ma", name="short_window_ma")
        self.long_window_ma  = self.I(self.strat.get_indicator, "long_window_ma", name="long_window_ma")
        self.window_ma_200  = self.I(self.strat.get_indicator, "window_ma_200", name="window_ma_200")

    def next(self):
        price = self.data.Close[-1]
        indicators = {
            "close": self.close.s,
            "short_window_ma": self.short_window_ma.s,
            "long_window_ma": self.long_window_ma.s,
            "window_ma_200": self.window_ma_200.s
        }
        signal = self.strat.signal(indicators)

        if signal == TradeSignal.BULLISH:
            self.buy(tp=1.15*price, sl=0.95*price)
        elif signal==TradeSignal.BEARISH:
            self.position.close()
