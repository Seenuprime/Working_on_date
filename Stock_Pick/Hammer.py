import yfinance as yf
import pandas as pd

def get_the_stock(data, output):
    df = pd.read_csv(f"{data}.csv")
    store = []

    stock_symbols = df["Symbol"].tolist()

    for symbol in stock_symbols:
        full_symbol = symbol + ".NS"
        stock_data = yf.download(full_symbol, period="5d")

        if stock_data.empty:
            print(f"No data available for {symbol}.")
            continue

        latest_close = stock_data["Close"].iloc[-1]
        latest_open = stock_data["Open"].iloc[-1]
        latest_high = stock_data["High"].iloc[-1]
        latest_low = stock_data["Low"].iloc[-1]

        if pd.isnull(latest_high) or pd.isnull(latest_open):
            print(f"Not enough data available for {symbol}.")
            continue
        
        if len(stock_data) < 2:
            print(f"Not enough data available for {symbol}.")
            continue

        logic_l = latest_open - 1.2 * latest_open / 100 
        logic_h = latest_open + 1.2 * latest_open / 100

        logic_high = latest_high - 6 * latest_high / 100
        logic_low = latest_low + 1.5 * latest_low / 100
        
        def hammer(l_c, lo_h, lo_l, l_l, l_h):
            if l_c > 150 and l_c < 600:
                if l_l < lo_l and l_c > lo_h and (l_c == l_h or l_c >= logic_high):
                    print(f"Stock name: {symbol}")
                    store.append(symbol)
        
        # hammer(l_c= latest_close, lo_h= logic_h, lo_l= logic_l, l_l= latest_low, l_h= logic_high)

        def reverse_hammer(l_c, lo_h, lo_l, l_h, l_l):
            if l_c > 150 and l_c < 600:
                if l_c < lo_l and l_h > lo_h and (l_c == l_l or l_c <= logic_low):
                    print(f"Stock name: {symbol}")
                    store.append(symbol)
        reverse_hammer(l_c= latest_close, lo_h= logic_h, lo_l= logic_l, l_h= latest_high, l_l= logic_low)
        
    dataframe = pd.DataFrame({'Stock_name': store})
    dataframe.to_csv(f"{output}.csv", index=False)

    print(f"Stocks are saved into {output}.csv")
    
    return store

data = "C:\Learning\Programs\Python_Projects\Trading\Prototypes\Input\All_Equity"
output = "Stock_Pick\Hammer"
get_the_stock(data, output)
