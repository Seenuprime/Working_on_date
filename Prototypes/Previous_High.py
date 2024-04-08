import yfinance as yf
import pandas as pd


def get_stocks_below_price(data, datato, datato1):
    df = pd.read_csv(f"{data}.csv")
    above_400 = []
    below_400 = []

    stock_symbols = df["Symbol"].tolist()

    for symbol in stock_symbols:
        full_symbol = symbol + ".NS"
        stock_data = yf.download(full_symbol, period="1y", progress=True)

        if stock_data.empty:
            print(f"No data available for {symbol}.")
            continue

        previous_high = stock_data["High"].max()

        if pd.isnull(previous_high):
            print(f"Not enough data available for {symbol}.")
            continue

        latest_close = stock_data["Close"][-1]
        latest_open = stock_data["Open"][-1]
        percentage_difference = ((latest_close - previous_high) / previous_high) * 100

        if latest_close > latest_open:
            if (
                latest_close < 700
                and latest_close > 400
                and abs(percentage_difference) <= 5
            ):
                above_400.append(symbol)
                print(f"{symbol} is near its previous high and above 400.\n")

            elif latest_close < 400 and abs(percentage_difference) <= 5:
                below_400.append(symbol)
                print(f"{symbol} is near its previous high and below 400.\n")

    dataframe = pd.DataFrame({"Stock Names": above_400})
    dataframe1 = pd.DataFrame({"Stock Name": below_400})

    dataframe.to_csv(f"{datato}.csv", index=False)
    dataframe1.to_csv(f"{datato1}.csv", index=False)

    print(f"Stock names saved to '{datato}.csv' and '{datato1}.csv'.")


data = "Prototypes/Input/All_Equity"
datato = "Prototypes/Output/All_Nifty_A400"
datato1 = "Prototypes/Output/All_Nifty_B400"

get_stocks_below_price(data, datato, datato1)
