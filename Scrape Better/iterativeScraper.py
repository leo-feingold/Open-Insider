from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from datetime import datetime, timedelta

#main_url = "http://openinsider.com/screener?s=&o=&pl=&ph=&ll=&lh=&fd=-1&fdr=02%2F13%2F2023+-+02%2F14%2F2023&td=0&tdr=&fdlyl=&fdlyh=&daysago=&xp=1&vl=&vh=&ocl=&och=&sic1=-1&sicl=100&sich=9999&grp=0&nfl=&nfh=&nil=&nih=&nol=&noh=&v2l=&v2h=&oc2l=&oc2h=&sortcol=0&cnt=100&page=1"

def iterate_dates(max, min, delta):
    dates = []
    while max > min:
        dates.append(min)
        min += delta
    return dates


def build_urls(dates):
    urls = []
    for date in dates:
        start_date = date #.strftime('%m/%d/%Y')
        end_date = (date + timedelta(days=3)) #.strftime('%m/%d/%Y')
        url = f"http://openinsider.com/screener?s=&o=&pl=&ph=&ll=&lh=&fd=-1&fdr={start_date}+-+{end_date}&td=0&tdr=&fdlyl=&fdlyh=&daysago=&xp=1&vl=&vh=&ocl=&och=&sic1=-1&sicl=100&sich=9999&grp=0&nfl=&nfh=&nil=&nih=&nol=&noh=&v2l=&v2h=&oc2l=&oc2h=&sortcol=0&cnt=100&page=1"
        urls.append(url)
    return urls

def scrape_url(urls):
    dfs = []
    for url in urls:
        driver = webdriver.Safari()
        driver.get(url)
        driver.implicitly_wait(10)

        table = driver.find_element(By.CLASS_NAME, 'tinytable')

        rows = table.find_elements(By.TAG_NAME, 'tr')
        data = []
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, 'td')
            if not cells:
                cells = row.find_elements(By.TAG_NAME, 'th')
            data.append([cell.text for cell in cells])

        driver.quit()

        df = pd.DataFrame(data[1:], columns = data[0])
        dfs.append(df)

    return dfs

def concat_and_finish(dfs):
    final_df = pd.concat(dfs, ignore_index=True)
    print(f"Columns: {final_df.columns}")
    print(f"Result: {final_df}")
    final_df.to_csv("2008Scrape.csv")
    return final_df

def main():
    max_date = datetime(2008, 12, 28)
    min_date = datetime(2008, 1, 1)
    delta = timedelta(days=10)

    dates = iterate_dates(max_date, min_date, delta)
    urls = build_urls(dates)
    dfs = scrape_url(urls)
    final_df = concat_and_finish(dfs)

if __name__ == "__main__":
    main()