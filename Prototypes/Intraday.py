import yfinance as yf
import pandas as pd

def Intraday(file):
    data_frame = pd.read_csv(f"{file}.csv")
    stock_name = data_frame["Symbol"]

    store = []
    for symbol in stock_name:
        Symbol = f"{symbol}.NS"
        stock_data = yf.download(Symbol, period="1d", interval="5m")

        if stock_data.empty:
            print(f"No data available for {symbol}.")
            continue

        if len(stock_data) < 2:
            print(f"Not enough data available for {symbol}.")
            continue

        f_open = stock_data["Open"][0]
        s_open = stock_data["Open"][1]

        f_close = stock_data["Close"][0]
        s_close = stock_data["Close"][1]

        if pd.isnull(f_open) or pd.isnull(s_open):
            print(f"Not enough data available for {symbol}.")
            continue

        if f_open > 250 and f_open < 600:
            f_p_o = 2*f_open/100 + f_open
            s_p_o = 2*s_open/100 + s_open
            if f_close > f_p_o and s_close > s_p_o:
                store.append(symbol)
                print(symbol)
                

    for i in store:
        print(i)

Intraday("Prototypes/Input/All_Equity")