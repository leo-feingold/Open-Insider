from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

main_url = "http://openinsider.com/latest-cluster-buys"
driver = webdriver.Safari()
driver.get(main_url)
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
df.to_csv("test.csv")
print(df.head())