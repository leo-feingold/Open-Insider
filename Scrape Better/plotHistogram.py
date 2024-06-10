import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def loadData(csv):
    df = pd.read_csv(csv)
    return df

def plotData(df):
    # bounding between -1 and 1 removes outliers
    lower_bound=-1
    upper_bound=1
    sample = len(df["Return on Investment"])
    plt.hist(df['Return on Investment'], bins=30, range=(lower_bound, upper_bound), edgecolor='k', alpha=0.7)
    plt.title(f'Histogram of 2020 Data: Sample of {sample} Stocks')
    plt.xlabel('ROI')
    plt.ylabel('Frequency')
    plt.show()

    filtered_df = df[(df['Return on Investment'] >= lower_bound) & (df['Return on Investment'] <= upper_bound)]
    sns.kdeplot(filtered_df['Return on Investment'], shade=True)
    plt.title('KDE Plot of Filtered ROI Data')
    plt.xlabel('ROI')
    plt.ylabel('Density')
    plt.show()
    plt.show()



def main():
    csv = "/Users/leofeingold/Desktop/Open Insider/2020Results.csv"
    data = loadData(csv)
    plotData(data)

if __name__ == "__main__":
    main()