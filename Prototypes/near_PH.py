import yfinance as yf
import pandas as pd

def calculate_rsi(data1, window):
    delta = data1["Close"].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi[-1]

def take(data):
    df = pd.read_csv(f"{data}.csv")
    stock_symbols = df["Symbol"].tolist()

    store=[]
    for symbol in stock_symbols:
        Symbol = symbol+".NS"
        stock_data = yf.download(Symbol, period='1y')
        
        if stock_data.empty:
            print(f"No data available for {Symbol}.")
            continue

        previous_high = stock_data["High"].max()
        latest_close = stock_data["Close"][-1]
        latest_open = stock_data["Open"][-1]
        
        calculate = latest_close - 2 * latest_close / 100


        if pd.isnull(previous_high):
            print(f"Not enough data available for {symbol}.")
            continue

        if latest_close > 150 and latest_close < 600:
            if calculate < previous_high and latest_close > latest_open and latest_close > calculate:
                rsi_25 = calculate_rsi(stock_data, window=25)
                rsi_100 = calculate_rsi(stock_data, window=100)
                if rsi_25 > rsi_100 and rsi_25 < rsi_100 + 10:
                    print(symbol)
                    print("High:", previous_high)
                    store.append(symbol)

    return(store)
    
store = take("Prototypes/Input/All_Equity")
for i in store:
    print(i)

# add rsi 25 and rsi 100: if rsi 25 crossed rsi 100 just 1 point low not greater than 1 point then print it
# add this inside the "if latest_close > 150 and latest_close < 600:"


