from backtesting import Strategy
from core.models.trade_signal import TradeSignal
from core.trading.macd import MACD

class MACDStrategy(Strategy):
    short_window = 5
    long_window  = 20

    def init(self):
        self.strat = MACD(self.data.df)

        self.close = self.I(self.strat.get_indicator, "close", plot=False, name="close")
        self.macd = self.I(self.strat.get_indicator, "macd", name="macd")
        self.macdsignal = self.I(self.strat.get_indicator, "macdsignal", name="macdsignal")
        self.macdhist = self.I(self.strat.get_indicator, "macdhist", plot=False, name="macdhist")
        self.window_ma_200  = self.I(self.strat.get_indicator, "window_ma_200")

    def next(self):
        price = self.data.Close[-1]
        indicators = {
            "close": self.close.s,
            "macd": self.macd.s,
            "macdsignal": self.macdsignal.s,
            "macdhist": self.macdhist.s,
            "window_ma_200": self.window_ma_200.s
        }
        signal = self.strat.signal(indicators)

        if signal == TradeSignal.BULLISH:
            self.buy(tp=1.15*price, sl=0.95*price)
        elif signal==TradeSignal.BEARISH:
            self.position.close()
