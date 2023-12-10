from backtesting import Strategy
from core.models.trade_signal import TradeSignal
from core.trading.bbands_rsi import BBandsRSI

import pandas as pd

class BBandsRSIStrategey(Strategy):
    def init(self):
        self.strat = BBandsRSI(self.data.df)
        self.close = self.I(self.strat.get_indicator, "close", plot=False, name="close")
        self.bbands_upper = self.I(self.strat.get_indicator, "bbands_upper", name="bbands_upper")
        self.bbands_middle = self.I(self.strat.get_indicator, "bbands_middle", name="bbands_middle")
        self.bbands_lower = self.I(self.strat.get_indicator, "bbands_lower", name="bbands_lower")
        self.rsi = self.I(self.strat.get_indicator, "rsi", name="rsi")
        self.trading_sideways = self.I(self.strat.get_indicator, "trading_sideways", name="trading_sideways")

    def next(self):
        price = self.data.Close[-1]
        indicators = {
            "close" : self.close.df.close,
            "bbands_upper" : self.bbands_upper.df.bbands_upper,
            "bbands_middle" : self.bbands_middle.df.bbands_middle,
            "bbands_lower" : self.bbands_lower.df.bbands_lower,
            "trading_sideways" : self.trading_sideways.df.trading_sideways,
            "rsi" : self.rsi.df.rsi
        }

        signal = self.strat.signal(indicators)

        if signal == TradeSignal.BULLISH:
            self.buy(tp=1.15*price, sl=0.95*price)
        elif signal==TradeSignal.BEARISH:
            self.position.close()
