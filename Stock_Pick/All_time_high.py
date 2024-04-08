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
        max_data = yf.download(symbol, start="2018-01-01", end="2023-07-29")

        if data.empty:
            print(f"No data available for {symbol}.")
            continue
        
        max = max_data["High"].max()
        close = data["Close"][-1]
        if close > 150 and close < 600:
            if close > max:
                print(Symbol)
                store.append(Symbol)

    return store

t = take("Prototypes\Input\All_Equity")
print(t)

            # add volume to it


