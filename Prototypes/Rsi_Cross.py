import yfinance as yf
import pandas as pd


def get_stocks_rsi_crossover(data, output_file):
    df = pd.read_csv(f"{data}")
    stock_names = df["Symbol"]

    crossover_stocks = []

    for symbol in stock_names:
        full_symbol = symbol + ".NS"
        stock_data = yf.download(full_symbol, period="1y")

        if stock_data.empty:
            print(f"No data available for {symbol}.")
            continue

        # Calculate RSI
        delta = stock_data["Close"].diff()
        up = delta.clip(lower=0)
        down = -delta.clip(upper=0)
        avg_gain = up.rolling(window=14).mean()
        avg_loss = down.rolling(window=14).mean()
        rs = avg_gain / avg_loss
        rsi_25 = 100 - (100 / (1 + rs))
        rsi_100 = rsi_25.rolling(window=100).mean()

        latest_close = stock_data["Close"][-1]
        # Check for RSI crossover
        if (
            latest_close < 600
            and rsi_25.iloc[-1] < rsi_100.iloc[-1]
            and rsi_25.iloc[-2] >= rsi_100.iloc[-2]
        ):
            crossover_stocks.append(symbol)
            print(f"{symbol} is nearing RSI crossover and less than 600.\n")

    dataframe = pd.DataFrame({"Stock Names": crossover_stocks})
    dataframe.to_csv(output_file, index=False)

    print(f"Stock names saved to '{output_file}'.")


stock_names = "Prototypes/Input/All_Equity.csv"
output_file = "Prototypes/Output/RSI_Crossover_Stocks.csv"

get_stocks_rsi_crossover(stock_names, output_file)
