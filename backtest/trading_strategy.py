from backtesting import Strategy
from core.models.trade_signal import TradeSignal
from core.trading.moving_averages import MovingAverages

class TradingStrategy(Strategy):
    short_window = 5
    long_window  = 20

    def init(self):
        self.strat = MovingAverages(self.data.Close, self.short_window, self.long_window)
        self.short_window_ma = self.I(self.strat.get_short_window_ma)
        self.long_window_ma = self.I(self.strat.get_long_window_ma)

    def next(self):
        price = self.data.Close[-1]
        signal = self.strat.signal(self.short_window_ma, self.long_window_ma)

        if signal == TradeSignal.BULLISH:
            self.buy(tp=1.15*price, sl=0.95*price)
        elif signal==TradeSignal.BEARISH:
            self.position.close()
