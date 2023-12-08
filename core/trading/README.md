# Trading
## Contributing
If you wish to add a new trading strategy into this module. Create a new class in a separate file. The class should inherit the `Strategy` abstract base class and implement all of it's methods. This is primarily for compatability with backtesting.  

## Strategies

### Moving Averages
Uses the [Moving Averages](https://www.investopedia.com/terms/m/movingaverage.asp#:~:text=A%20moving%20average%20is%20a,price%20trends%20for%20specific%20securities.) technical indicator. The strategy uses two moving average lines, a short and long window. When the short window average crosses above the long window, a buy signal is triggered. When the short window crosses below the long window, a sell signal is triggered.

### Engulfing Candlesticks
Uses the [Engulfing Candlesticks](https://www.investopedia.com/terms/b/bullishengulfingpattern.asp) signal pattern. It returns a signal based on the most two recent days in the dataframe.