import numpy as  np
import pandas as pd
import yfinance as yf
from datetime import timedelta, time


def loadClusterBuys(csv):
    df = pd.read_csv(csv)
    print("Columns in the DataFrame:", df.columns.tolist())
    df.columns = df.columns.str.replace('\xa0', ' ').str.strip()
    df['Filing Date'] = pd.to_datetime(df['Filing Date'])
    print("Updated Columns in the DataFrame:", df.columns.tolist())
    return df

def findNearestFutureDay(df, target_date):
    future_dates = df.index[df.index >= target_date]
    if not future_dates.empty:
        closest_date = future_dates[0]
    else:
        closest_date = df.index[0]
    return closest_date


def performanceOverNext3Days(df):
    market_open = time(9, 0)
    market_close = time(16, 0)
    result_df = pd.DataFrame(columns=["Ticker", "Filing Date", "Actual Purchase Date", "Purchase Price", "Sell Date", "Sell Price", "Return on Investment (%)"])
    for stock, filing_date in zip(df["Ticker"], df["Filing Date"]):
        if filing_date.time() > market_close:
            purchase_date = filing_date + timedelta(days=1)
        else:
            purchase_date = filing_date
        
        data = yf.download(stock, start=filing_date, end=purchase_date + timedelta(days=5))
        
        if not data.empty:
            actual_purchase_date = findNearestFutureDay(data, purchase_date)
            open_price = data.loc[actual_purchase_date]["Open"]
            
            sell_date = findNearestFutureDay(data, actual_purchase_date + timedelta(days=3))
            close_price = data.loc[sell_date]["Close"]
            roi = ((close_price - open_price) / open_price) * 100

            result_df = pd.concat([result_df, pd.DataFrame({
                "Ticker": [stock],
                "Filing Date": [filing_date],
                "Actual Purchase Date": [actual_purchase_date],
                "Purchase Price": [open_price],
                "Sell Date": [sell_date],
                "Sell Price": [close_price],
                "Return on Investment (%)": [roi]
            })], ignore_index=True)

    return result_df

def main():
    csv = "/Users/leofeingold/Desktop/Open Insider/test.csv"
    clusters = loadClusterBuys(csv)
    results = performanceOverNext3Days(clusters)
    print(results)
    results.to_csv("better.csv")


if __name__ == "__main__":
    main()
