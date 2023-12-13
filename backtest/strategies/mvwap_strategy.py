from backtesting import Strategy
from core.models.trade_signal import TradeSignal
from core.trading.mvwap import MVWAP

class MVWAPStrategy(Strategy):
    def init(self):
        self.strat = MVWAP(self.data.df)

        self.close = self.I(self.strat.get_indicator, "close", plot=False, name="close")
        self.open = self.I(self.strat.get_indicator, "open", plot=False, name="open")
        self.bbands_upper = self.I(self.strat.get_indicator, "bbands_upper", name="bbands_upper")
        self.bbands_lower = self.I(self.strat.get_indicator, "bbands_lower", name="bbands_lower")
        self.rsi = self.I(self.strat.get_indicator, "rsi", name="rsi")
        self.mvwap = self.I(self.strat.get_indicator, "mvwap", name="mvwap")
    
    def next(self):
        price = self.data.Close[-1]
        indicators = {
            "open" : self.open.df.open,
            "close" : self.close.df.close,
            "bbands_upper" : self.bbands_upper.df.bbands_upper,
            "bbands_lower" : self.bbands_lower.df.bbands_lower,
            "rsi" : self.rsi.df.rsi,
            "mvwap": self.mvwap.df.mvwap
        }

        signal = self.strat.signal(indicators)

        if signal == TradeSignal.BULLISH:
            self.buy(tp=1.15*price, sl=0.95*price)
        elif signal==TradeSignal.BEARISH:
            self.position.close()