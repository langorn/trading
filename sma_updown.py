from pyalgotrade import strategy
from pyalgotrade.barfeed import quandlfeed
from pyalgotrade.technical import ma
from pyalgotrade.technical import rsi
from pyalgotrade.tools import quandl
from pyalgotrade.technical import cross
from pyalgotrade import plotter
from pyalgotrade.stratanalyzer import sharpe
from pyalgotrade.stratanalyzer import returns
from pyalgotrade.barfeed.csvfeed import GenericBarFeed
from pyalgotrade.bar import Frequency
from pyalgotrade.barfeed import googlefeed


class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument):
        super(MyStrategy, self).__init__(feed)
        self.__instrument = instrument
        self.__position = None
        # self.setUseAdjustedValues(True)
        self.__prices = feed[instrument].getPriceDataSeries()

        # 指数数据
        #self.setUseAdjustedValues(False)
        self.__shortsma = ma.SMA(self.__prices, 20)
        self.__longsma = ma.SMA(self.__prices, 40)

    def getSMA4(self):
        return self.__shortsma

    def getSMA40(self):
        return self.__longsma

    def onEnterOk(self, position):
        execInfo = position.getEntryOrder().getExecutionInfo()
        self.info("買 at $%.2f" % (execInfo.getPrice()))

    def onEnterCanceled(self, position):
        self.__position = None

    def onExitOk(self, position):
        execInfo = position.getExitOrder().getExecutionInfo()
        self.info("賣 at $%.2f" % (execInfo.getPrice()))
        self.__position = None

    def onExitCanceled(self, position):
        # If the exit was canceled, re-submit it.
        self.__position.exitMarket()

    def onBars(self, bars):
        if len(self.__longsma) < 2:
            return
        bar = bars[self.__instrument]
        shares = self.getBroker().getShares(self.__instrument)
        if self.__position is None:
            if cross.cross_above(self.__shortsma, self.__longsma) > 0:
                self.__position = self.enterLong(self.__instrument, 100, True)

        elif not self.__position.exitActive() and cross.cross_below(self.__shortsma, self.__longsma) > 0:
            self.__position.exitMarket()


# feed = quandlfeed.Feed()
# feed.addBarsFromCSV("orcl", "WIKI-ORCL-2000-quandl.csv")
# Evaluate the strategy with the feed's bars.


#import through quandl
# instrument = "AAPL"
# feed = quandl.build_feed("WIKI", [instrument], 2017, 2018, ".")

#import from google
# feed = googlefeed.Feed()
# instrument = "spy"
# feed.addBarsFromCSV(instrument, "spy_2017.csv")

#import through local csv
feed = GenericBarFeed(Frequency.DAY, None, None)
feed.addBarsFromCSV("output", "output.csv")
instrument = "output"
myStrategy = MyStrategy(feed, instrument)

sharpeRatioAnalyzer = sharpe.SharpeRatio()
returnsAnalyzer = returns.Returns()

myStrategy.attachAnalyzer(returnsAnalyzer)
plot = True
if plot:
    plt = plotter.StrategyPlotter(myStrategy)
    plt.getInstrumentSubplot(instrument).addDataSeries("sma20", myStrategy.getSMA4())
    plt.getInstrumentSubplot(instrument).addDataSeries("sma40", myStrategy.getSMA40())

myStrategy.run()

if plot:
    plt.plot()
print("Final portfolio value: $%.2f" % myStrategy.getBroker().getEquity())
