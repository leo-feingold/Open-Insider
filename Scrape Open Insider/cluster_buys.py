from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

main_url = "http://openinsider.com/latest-cluster-buys"
driver = webdriver.Safari()
driver.get(main_url)
driver.implicitly_wait(10)

# Find the table by its class name
table = driver.find_element(By.CLASS_NAME, 'tinytable')

# Extract the table rows
rows = table.find_elements(By.TAG_NAME, 'tr')

# Extract the data from the rows
data = []
for row in rows:  # Include the header row for column names
    cells = row.find_elements(By.TAG_NAME, 'td')
    if not cells:  # If no 'td' found, check for 'th' (header)
        cells = row.find_elements(By.TAG_NAME, 'th')
    data.append([cell.text for cell in cells])

# Close the browser
driver.quit()

# Convert the data to a DataFrame
df = pd.DataFrame(data[1:], columns=data[0])  # Use the first row as header

# Display the DataFrame
df.to_csv("test.csv")
print(df.head())

