from backtesting import Strategy
from core.models.trade_signal import TradeSignal
from core.trading.engulfing_candlesticks import EngulfingCandlesticks

class EngulfingCandlesticksStrategy(Strategy):
    def init(self):
        self.strat = EngulfingCandlesticks(self.data.df)
        self.signals = self.I(self.strat.get_indicator, "signals")

    def next(self):
        price = self.data.Close[-1]
        indicators = {
            "signals": self.signals.s
        }
        signal = self.strat.signal(indicators)

        if signal == TradeSignal.BULLISH:
            self.buy(tp=1.15*price, sl=0.95*price)
        elif signal==TradeSignal.BEARISH:
            self.position.close()
