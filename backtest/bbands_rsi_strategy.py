from backtesting import Strategy
from core.models.trade_signal import TradeSignal
from core.trading.bbands_rsi import BBandsRSI

class BBandsRSIStrategey(Strategy):
    def init(self):
        self.strat = BBandsRSI(self.data.df)
        self.close = self.I(self.strat.get_indicator, "close")
        self.bbands_upper = self.I(self.strat.get_indicator, "bbands_upper")
        self.bbands_middle = self.I(self.strat.get_indicator, "bbands_middle")
        self.bbands_lower = self.I(self.strat.get_indicator, "bbands_lower")
        self.rsi = self.I(self.strat.get_indicator, "rsi")

    def next(self):
        price = self.data.Close[-1]
        indicators = {
            "close" : self.close,
            "bbands_upper" : self.bbands_upper,
            "bbands_middle" : self.bbands_middle,
            "bbands_lower" : self.bbands_lower,
            "rsi" : self.rsi
        }
        
        signal = self.strat.signal(indicators)

        if signal == TradeSignal.BULLISH:
            self.buy(tp=1.15*price, sl=0.95*price)
        elif signal==TradeSignal.BEARISH:
            self.position.close()
