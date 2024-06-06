from alpha_vantage.timeseries import TimeSeries
import pandas as pd

def getKey():
    with open('/Users/leofeingold/Desktop/Open Insider/Stock Performance/key.txt', 'r') as file:
        key = file.readline().strip()
        return key

def loadClusterBuys(csv):
    df = pd.read_csv(csv)
    df.columns = df.columns.str.replace('\xa0', ' ').str.strip()
    df['Filing Date'] = pd.to_datetime(df['Filing Date'])
    return df

def hourLaterPerformance(df, key):
    api_key = key
    ts = TimeSeries(key=key, output_format='pandas')
    
    result_df = pd.DataFrame(columns=["Ticker", "Filing Date and Time", "1 Hour Later Date and Time", "Return on Investment (%)"])

    for symbol in df["Ticker"].unique():
        try:
            data, meta_data = ts.get_intraday(symbol=symbol, interval='60min', outputsize='full')
            data.reset_index(inplace=True)
            data['date'] = pd.to_datetime(data['date'])
            
            for index, row in df[df["Ticker"] == symbol].iterrows():
                filing_time = pd.to_datetime(row["Date"])
                
                closest_time = data.iloc[(data['date'] - filing_time).abs().argsort()[:1]]
                initial_price = closest_time["close"].values[0]
                
                one_hour_later_time = filing_time + pd.Timedelta(hours=1)
                one_hour_later_data = data.iloc[(data['date'] - one_hour_later_time).abs().argsort()[:1]]
                one_hour_later_price = one_hour_later_data["close"].values[0]
                
                roi = ((one_hour_later_price - initial_price) / initial_price) * 100

                result_df = result_df.append({
                    "Ticker": symbol,
                    "Filing Date and Time": filing_time,
                    "1 Hour Later Date and Time": one_hour_later_time,
                    "Return on Investment (%)": roi
                }, ignore_index=True)

        except Exception as e:
            print(f"Could not retrieve data for {symbol}: {e}")

    return result_df

def main():
    key = getKey()
    print(f"Key: {key}")
    csv = "/Users/leofeingold/Desktop/Open Insider/cluster_buys.csv"
    clusters = loadClusterBuys(csv)
    hourLaterPerformance(clusters, key)

if __name__ == "__main__":
    main()
