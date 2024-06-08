from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

#main_url = "http://openinsider.com/latest-cluster-buys"
# this was may 31-30 dates #test_url = "http://openinsider.com/screener?s=&o=&pl=&ph=&ll=&lh=&fd=-1&fdr=05%2F01%2F2024+-+06%2F01%2F2024&td=0&tdr=&fdlyl=&fdlyh=&daysago=&xp=1&vl=&vh=&ocl=&och=&sic1=-1&sicl=100&sich=9999&grp=0&nfl=&nfh=&nil=&nih=&nol=&noh=&v2l=&v2h=&oc2l=&oc2h=&sortcol=0&cnt=100&page=1"
#test_url = "http://openinsider.com/screener?s=&o=&pl=&ph=&ll=&lh=&fd=-1&fdr=05%2F06%2F2024+-+05%2F07%2F2024&td=0&tdr=&fdlyl=&fdlyh=&daysago=&xp=1&vl=&vh=&ocl=&och=&sic1=-1&sicl=100&sich=9999&grp=0&nfl=&nfh=&nil=&nih=&nol=&noh=&v2l=&v2h=&oc2l=&oc2h=&sortcol=0&cnt=100&page=1"
#back_test_2016_url = "http://openinsider.com/screener?s=&o=&pl=&ph=&ll=&lh=&fd=-1&fdr=10%2F03%2F2016+-+10%2F03%2F2016&td=0&tdr=&fdlyl=&fdlyh=&daysago=&xp=1&vl=&vh=&ocl=&och=&sic1=-1&sicl=100&sich=9999&grp=0&nfl=&nfh=&nil=&nih=&nol=&noh=&v2l=&v2h=&oc2l=&oc2h=&sortcol=0&cnt=100&page=1"
#back_test_jan_2022_url = "http://openinsider.com/screener?s=&o=&pl=&ph=&ll=&lh=&fd=-1&fdr=01%2F17%2F2022+-+01%2F19%2F2022&td=0&tdr=&fdlyl=&fdlyh=&daysago=&xp=1&vl=&vh=&ocl=&och=&sic1=-1&sicl=100&sich=9999&grp=0&nfl=&nfh=&nil=&nih=&nol=&noh=&v2l=&v2h=&oc2l=&oc2h=&sortcol=0&cnt=100&page=1"
back_test_feb_2023_url = "http://openinsider.com/screener?s=&o=&pl=&ph=&ll=&lh=&fd=-1&fdr=02%2F13%2F2023+-+02%2F14%2F2023&td=0&tdr=&fdlyl=&fdlyh=&daysago=&xp=1&vl=&vh=&ocl=&och=&sic1=-1&sicl=100&sich=9999&grp=0&nfl=&nfh=&nil=&nih=&nol=&noh=&v2l=&v2h=&oc2l=&oc2h=&sortcol=0&cnt=100&page=1"


driver = webdriver.Safari()
driver.get(back_test_feb_2023_url)
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

df = pd.DataFrame(data[1:], columns=data[0])
df.to_csv("backTestFeb2023.csv")
print(df.head())