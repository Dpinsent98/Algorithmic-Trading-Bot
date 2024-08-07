import numpy as np
import pandas as pd
import yfinance as yf
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

S = "2024-04-01"
E = "2024-05-01"

MSFT = yf.download("MSFT", start= S, end= E, interval='15m')

def Top10NSD():
    GOOG = yf.download("GOOG", start= S, end= E, interval='15m')
    TSLA = yf.download("TSLA", start= S, end= E, interval='15m')
    AAPL = yf.download("AAPL", start= S, end= E, interval='15m')
    AMZN = yf.download("AMZN", start= S, end= E, interval='15m')
    META = yf.download("META", start= S, end= E, interval='15m')
    PEP  = yf.download("PEP" , start= S, end= E, interval='15m')
    COST = yf.download("COST", start= S, end= E, interval='15m')
    NVDA = yf.download("NVDA", start= S, end= E, interval='15m')

def MovingAvgCrossOver(data):

    # 3 Day moving AVG
    data["3dayMA"] = data["Close"].rolling(window = 3).mean()

    # 14 Day moving AVG
    data["14dayMA"] = data["Close"].rolling(window = 14).mean()

    # Generate buy/sell signals
    data['Signal'] = 0
    data.loc[data['3dayMA'] > data['14dayMA'], 'Signal'] = 1
    data.loc[data['3dayMA'] < data['14dayMA'], 'Signal'] = -1
    
    class SMA(Strategy):

        def init(self):
            pass

        def next(self):
            current_signal = self.data.Signal[-1]

            if current_signal == 1:
                if not self.position:
                    self.buy()
            elif current_signal == -1:
                if self.position:
                    self.position.close()

    bt = Backtest(data, SMA, cash=10000, commission=.002, exclusive_orders=True)

    stats = bt.run()
    bt.plot()
    print(stats)

def BreakoutUp(data):

    data["14dayMA"] = data["Close"].rolling(window = 14).mean()
    data["14daySD"] = data["Close"].rolling(window = 14).std()
    data["30daySD"] = data["Close"].rolling(window = 30).std()
    
    # Generate buy/sell signals
    data["Signal"] = 0
    data["SignalC"] = 0

    data.loc[data["14daySD"] < 0.5 * data["30daySD"], "SignalC"] = 1

    data.loc[data["Close"] > data["14dayMA"] + 0.2 * data["14daySD"], "Signal"] = 1
    data.loc[data["Close"] < data["Close"].shift(-1), "Signal"] = -1

    class Break(Strategy):

        def init(self):
            pass

        def next(self):
            current_signal = self.data.Signal[-1]
            c_signal = self.data.SignalC[-1]

            if current_signal == 1 & c_signal == 1:
                if not self.position:
                    self.buy()
            elif current_signal == -1:
                    self.position.close()

    bt = Backtest(data, Break, cash=10000, commission=.002, exclusive_orders=True)
    stats = bt.run()
    bt.plot()
    print(stats)

def BreakoutDown(data):

    data["14dayMA"] = data["Close"].rolling(window = 14).mean()
    data["14daySD"] = data["Close"].rolling(window = 14).std()
    data["30daySD"] = data["Close"].rolling(window = 30).std()
    
    # Generate buy/sell signals
    data["Signal"] = 0
    data["SignalC"] = 0

    data.loc[data["14daySD"] < 0.5 * data["30daySD"], "SignalC"] = 1

    data.loc[data["Close"] < data["14dayMA"] - 0.2 * data["14daySD"], "Signal"] = -1
    data.loc[data["Close"] > data["Close"].shift(-1), "Signal"] = 1

    class Break(Strategy):

        def init(self):
            pass

        def next(self):
            current_signal = self.data.Signal[-1]
            c_signal = self.data.SignalC[-1]

            if current_signal == -1 & c_signal == 1:
                if not self.position:
                    self.sell()
            elif current_signal == 1:
                    self.position.close()

    bt = Backtest(data, Break, cash=10000, commission=.002, exclusive_orders=True)
    stats = bt.run()
    bt.plot()
    print(stats)

def MeanReversionBuy(data):
   # 14 Day moving AVG
    data["14dayMA"] = data["Close"].rolling(window = 14).mean()
    data["14daySD"] = data["Close"].rolling(window = 14).std()
    
    # Generate buy/sell signals
    data["Signal"] = 0
    data.loc[data["Close"] > data["14dayMA"] + 1.5 * data["14daySD"], "Signal"] = -1
    data.loc[data["Close"] < data["14dayMA"] , "Signal"] = 1

    class MR(Strategy):

        def init(self):
            pass

        def next(self):
            current_signal = self.data.Signal[-1]

            if current_signal == 1:
                if not self.position:
                    self.buy()
            elif current_signal == -1 :
                    self.position.close()

    bt = Backtest(data, MR, cash=10000, commission=.002, exclusive_orders=True)
    stats = bt.run()
    bt.plot()
    print(stats)
    print(data)

def MeanReversionSell(data):
   # 14 Day moving AVG
    data["14dayMA"] = data["Close"].rolling(window = 14).mean()
    data["14daySD"] = data["Close"].rolling(window = 14).std()

    # Generate buy/sell signals
    data["Signal"] = 0
    data.loc[data["Close"] < data["14dayMA"] - 1.5 * data["14daySD"], "Signal"] = -1
    data.loc[data["Close"] > data["14dayMA"] , "Signal"] = 1

    class MR(Strategy):

        def init(self):
            pass

        def next(self):
            current_signal = self.data.Signal[-1]

            if current_signal == -1:
                if not self.position:
                    self.sell()
            elif current_signal == 1 :
                    self.position.close()

    bt = Backtest(data, MR, cash=10000, commission=.002, exclusive_orders=True)
    stats = bt.run()
    bt.plot()
    print(stats)


#MeanReversionSell(GOOG)
#MeanReversionBuy(MSFT)
#MovingAvgCrossOver(GOOG)
#BreakoutDown(GOOG) 
#BreakoutUp(GOOG) 

