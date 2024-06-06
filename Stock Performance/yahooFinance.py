import pandas as pd
import yfinance as yf
from datetime import timedelta


def loadClusterBuys(csv):
    df = pd.read_csv(csv)
    print("Columns in the DataFrame:", df.columns.tolist())
    df.columns = df.columns.str.replace('\xa0', ' ').str.strip()
    df['Filing Date'] = pd.to_datetime(df['Filing Date'])
    print("Updated Columns in the DataFrame:", df.columns.tolist())
    return df

def performanceOverNext3Days(df):
    result_df = pd.DataFrame(columns=["Ticker", "Filing Date", "Filing Price", "Sell Date", "Sell Price", "Return on Investment (%)"])
    for stock, start_date in zip(df["Ticker"], df["Filing Date"]):
        end_date = start_date + timedelta(days=3)
        data = yf.download(stock, start=start_date, end=end_date)
        if not data.empty:
            open_price = data.iloc[0]["Close"]
            close_price = data.iloc[-1]["Close"]
            roi = ((close_price - open_price) / open_price) * 100

        result_df = pd.concat([result_df, pd.DataFrame({
                        "Ticker": [stock],
                        "Filing Date": [start_date],
                        "Filing Price": [open_price],
                        "Sell Date": [end_date],
                        "Sell Price": [close_price],
                        "Return on Investment (%)": [roi]
                    })], ignore_index=True)


    return result_df

def main():
    csv = "/Users/leofeingold/Desktop/Open Insider/test.csv"
    clusters = loadClusterBuys(csv)
    results = performanceOverNext3Days(clusters)
    print(results)
    results.to_csv("resultsClose.csv")


if __name__ == "__main__":
    main()
