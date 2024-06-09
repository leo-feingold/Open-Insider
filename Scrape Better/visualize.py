import numpy as np
import pandas as pd
import yfinance as yf
from datetime import timedelta, time, datetime
import matplotlib.pyplot as plt

def loadClusterBuys(csv):
    df = pd.read_csv(csv)
    print("Columns in the DataFrame:", df.columns.tolist())
    df.columns = df.columns.str.replace('\xa0', ' ').str.strip()
    df['Filing Date'] = pd.to_datetime(df['Filing Date'])
    print("Updated Columns in the DataFrame:", df.columns.tolist())
    return df

def findNearestFutureDay(data, target_date):
    target_date = target_date.replace(hour=0, minute=0, second=0, microsecond=0)
    future_dates = data.index[data.index >= target_date]
    if not future_dates.empty:
        closest_date = future_dates[0]
    else:
        closest_date = data.index[-1]
    return closest_date

def performanceOverNext3Days(df):
    market_open = time(9, 30)
    market_close = time(16, 0)
    result_df = pd.DataFrame(columns=["Ticker", "Filing Date", "Actual Purchase Date", "Purchase Price", "Sell Date", "Sell Price", "Return on Investment"])

    for stock, filing_date in zip(df["Ticker"], df["Filing Date"]):
        if pd.isna(stock) or not isinstance(stock, str):
            print(f"Invalid ticker: {stock}, skipping entry")
            continue
        start_date = filing_date - timedelta(days=1)
        end_date = filing_date + timedelta(days=9)

        #added
        try:
            data = yf.download(stock, start=start_date, end=end_date)
            if data.empty:
                print(f"No data found for ticker: {stock}, skipping entry")
                continue
        except Exception as e:
            print(f"Error downloading data for {stock}: {e}, skipping entry")
            continue
        #stop addition here

        #commented this
        #data = yf.download(stock, start=start_date, end=end_date)

        if not data.empty:
            if filing_date.time() > market_close:
                # filed after hours -> buy next days open
                target_purchase_date = filing_date + timedelta(days=1)
                actual_purchase_date = findNearestFutureDay(data, target_purchase_date)
                open_price = data.loc[actual_purchase_date]["Open"]
            elif filing_date.time() < market_open:
                # filed before opening -> buy that day's open
                target_purchase_date = filing_date
                actual_purchase_date = findNearestFutureDay(data, target_purchase_date)
                open_price = data.loc[actual_purchase_date]["Open"]
            else:
                # filed during the trading day -> buy at the close of that day (best I can do with YF)
                target_purchase_date = filing_date
                actual_purchase_date = findNearestFutureDay(data, target_purchase_date)
                open_price = data.loc[actual_purchase_date]["Close"]

            # still selling at close of day 3
            sell_date = findNearestFutureDay(data, actual_purchase_date + timedelta(days=3))
            close_price = data.loc[sell_date]["Close"]
            roi = ((close_price - open_price) / open_price)

            # no penny stocks
            if open_price > 1 and close_price > 1:
                result_df = pd.concat([result_df, pd.DataFrame({
                "Ticker": [stock],
                "Filing Date": [filing_date],
                "Actual Purchase Date": [actual_purchase_date],
                "Purchase Price": [open_price],
                "Sell Date": [sell_date],
                "Sell Price": [close_price],
                "Return on Investment": [roi]
            })], ignore_index=True)

    return result_df

def visualizeData(results_df):
    all_rois = []
    results_df = results_df.sort_values("Filing Date")
    results_df['Group'] = (results_df["Filing Date"].diff().dt.days > 4).cumsum()

    plt.figure(figsize=(10, 6))

    for group, data in results_df.groupby('Group'):
        mean_filing_date = data["Filing Date"].mean()
        total_roi = data["Return on Investment"].sum()
        all_rois.append(total_roi)
        plt.scatter(mean_filing_date, total_roi, label=f"Group {group}", color='black')
    
    total_roi_sum = np.sum(all_rois)
    plt.title(f"ROI Over Time (Total ROI: {total_roi_sum:.3f}%)")
    plt.xlabel("Filing Date")
    plt.ylabel("ROI)")
    plt.show()



def main():
    csv = "/Users/leofeingold/Desktop/Open Insider/2020Scrape.csv"
    clusters = loadClusterBuys(csv)
    results = performanceOverNext3Days(clusters)
    print(results)
    visualizeData(results)
    results.to_csv("2020Results.csv", index=False)

if __name__ == "__main__":
    main()
