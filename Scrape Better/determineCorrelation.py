import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import OneHotEncoder

def clean_column_names(df):
    df.columns = df.columns.str.replace('\xa0', ' ').str.strip()
    return df

def clean_numeric_columns(df, columns):
    for col in columns:
        if col in df.columns:
            df[col] = df[col].replace({'>999': 1000,'New': 0, '\%': '', '\$': '', ',': '', '\+': ''}, regex=True).astype(float)
    return df

def loadData(resultsCSV, scrapeCSV):
    results_df = pd.read_csv(resultsCSV)
    clean_column_names(results_df)
    results_df = clean_numeric_columns(results_df, ['Purchase Price', 'Sell Price', 'Return on Investment'])

    scrape_df = pd.read_csv(scrapeCSV)
    scrape_df = clean_column_names(scrape_df)
    scrape_df = clean_numeric_columns(scrape_df, ['Price', 'Qty', 'Value', 'ΔOwn'])

    return results_df, scrape_df

def mergeData(results_df, scrape_df):
    merged_df = pd.merge(results_df, scrape_df, on=['Filing Date', 'Ticker'], how='left')
    return merged_df

def calcCorrelation(df):
    df['Log_Qty'] = np.log1p(df['Qty'])
    df['Log_ROI'] = np.log1p(df['Return on Investment'])
    #corr = df["Return on Investment"].corr(df["Qty"])
    corr = df['Log_Qty'].corr(df['Log_ROI'])


    return corr, df

def visualizeData(df, corr):
    size = len(df)
    #plt.scatter(df["Qty"], df["Return on Investment"])
    #plt.title(f"2018 ROI vs Qty, Correlation: {corr} (Sample Size: {size} Stocks)")
    #plt.xlabel("Qty")
    #plt.ylabel("ROI")
    #plt.show()

    plt.scatter(df['Log_Qty'], df['Log_ROI'])
    plt.xlabel('Log Qty')
    plt.ylabel('Log ROI')
    plt.title(f"2018 Log ROI vs Log Qty, Correlation: {corr} (Sample Size: {size})")
    plt.show()


def main():
    resultsCSV = "/Users/leofeingold/Desktop/Open Insider/2018Results.csv"
    scrapeCSV = "/Users/leofeingold/Desktop/Open Insider/2018Scrape.csv"
    results, scrape = loadData(resultsCSV, scrapeCSV)
    merged_df = mergeData(results, scrape)
    corr, merged_df = calcCorrelation(merged_df)
    visualizeData(merged_df, corr)

if __name__ == "__main__":
    main()