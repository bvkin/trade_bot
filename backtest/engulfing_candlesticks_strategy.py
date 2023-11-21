from backtesting import Strategy
from core.models.trade_signal import TradeSignal
from core.trading.engulfing_candlesticks import EngulfingCandlesticks

class EngulfingCandlesticksStrategy(Strategy):
    def init(self):
        self.strat = EngulfingCandlesticks(open_prices=self.data.Open, high_prices=self.data.High, low_prices=self.data.Low, close_prices=self.data.Close)
        self.signals = self.I(self.strat.get_signals)

    def next(self):
        price = self.data.Close[-1]
        signal = self.strat.signal(self.signals)

        if signal == TradeSignal.BULLISH:
            self.buy(tp=1.15*price, sl=0.95*price)
        elif signal==TradeSignal.BEARISH:
            self.position.close()
