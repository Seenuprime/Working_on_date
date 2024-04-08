from talib import stream
import yfinance as yf
import pandas as pd

def take(f_csv):
    df = pd.read_csv(f"{f_csv}.csv")
    Symbols = df["Symbol"]

    store = []
    for Symbol in Symbols:
        symbol = Symbol + ".NS"
        data = yf.download(symbol, period="1y")
        max_data = yf.download(symbol, start="2022-01-01", end="2023-07-29")

        if data.empty:
            print(f"No data available for {symbol}.")
            continue
        
        # max = max_data["High"].max()
        # close = data["Close"][-1]
        # if close > 150 and close < 600:
        #     if close > max:
        #         print(Symbol)
        #         store.append(Symbol)




        at_close = data["Close"]
        close = data["Close"][-1]
        open = data["Open"][-1]
        high = data["High"][-1]
        low = data["Low"][-1]

        if close > 150 and close < 600:
            sma = round(stream.SMA(at_close, timeperiod=9), 3)
            print(sma)
            print(Symbol)
            if (open >= sma or open <= sma) and close > sma and low < sma and close > open:
                print("Got one: ",Symbol)
                store.append(Symbol)
    return store

t = take("Prototypes\Input\All_Equity")
print(t)

            # add volume to it














# data = yf.download("TATAMOTORS.NS", period='1y')
# close = data["Close"]
# print(stream.SMA(close,timeperiod=9))