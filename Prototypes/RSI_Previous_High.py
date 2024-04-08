import yfinance as yf
import pandas as pd
import talib


def get_stocks_below_price(data):
    df = pd.read_csv(f"{data}.csv")
    names = []

    stock_symbols = df["Symbol"].tolist()

    for symbol in stock_symbols:
        full_symbol = symbol + ".NS"
        stock_data = yf.download(full_symbol, period="1y")

        if stock_data.empty:
            print(f"No data available for {symbol}.")
            continue

        previous_high = stock_data["High"].max()

        if pd.isnull(previous_high):
            print(f"Not enough data available for {symbol}.")
            continue

        latest_close = stock_data["Close"][-1]

        percentage_difference = ((latest_close - previous_high) / previous_high) * 100

        if stock_data.empty:
            print(f"No data available for {symbol}.")
            continue

        if pd.isnull(previous_high):
            print(f"Not enough data available for {symbol}.")
            continue

        if (
            talib.RSI(stock_data["Close"], timeperiod=25)[-1] <= 57
            and abs(percentage_difference) <= 5
        ):
            names.append(symbol)
            print(f"{symbol}'s RSI is <= 31 and at previous High......")
        else:
            print("Not satisfied....")

    print(names)


data = "C:\Learning\Programs\Python_Projects\Trading\Prototypes\Input\All_Equity"


get_stocks_below_price(data)
