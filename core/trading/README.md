# Trading
## Contributing
If you wish to add a new trading strategy into this module. Create a new class in a separate file. The class should inherit the `Strategy` abstract base class and implement all of it's methods. This is primarily for compatability with backtesting.  

## Strategies

### Moving Averages
Uses the [Moving Averages](https://www.investopedia.com/terms/m/movingaverage.asp#:~:text=A%20moving%20average%20is%20a,price%20trends%20for%20specific%20securities.) technical indicator. The strategy uses two moving average lines, a short and long window. When the short window average crosses above the long window, a buy signal is triggered. When the short window crosses below the long window, a sell signal is triggered.

### Engulfing Candlesticks
Uses the [Engulfing Candlesticks](https://www.investopedia.com/terms/b/bullishengulfingpattern.asp) signal pattern. It returns a signal based on the most two recent days in the dataframe.

## Bollinger Bands + RSI
Uses a combination of [Bollinger Bands](https://www.investopedia.com/terms/b/bollingerbands.asp) and [RSI](https://www.investopedia.com/articles/active-trading/042114/overbought-or-oversold-use-relative-strength-index-find-out.asp) technical indicators. Bollinger Bands are used to determine when the market is trading sideways. This is indicated by when the two bands are within the 20th percentile of each other. Trading sidways is considered a dangerous time to buy. A Bullish signal is given when either the market is trading sideways or when the RSI value is above 60 at the same time the close value crosses above the upper bollinger band. A buy signal occurs when the RSI value is below 30 and the close value crosses below the lower bollinger band. 