from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
from datetime import datetime
import os

options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

url = "https://coinmarketcap.com/"
driver.get(url)


rows = WebDriverWait(driver, 15).until(
    EC.presence_of_all_elements_located((By.XPATH, '//table//tbody/tr'))
)[:10]

coins = []

for row in rows:
    try:
        cols = row.find_elements(By.TAG_NAME, 'td')
        name = cols[2].text.split('\n')[0]
        price = cols[3].text
        change_24h = cols[5].text
        market_cap = cols[7].text

        coins.append({
            'Name': name,
            'Price': price,
            '24h Change': change_24h,
            'Market Cap': market_cap,
            'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    except Exception as e:
        print("Error extracting a row:", e)

df = pd.DataFrame(coins)
print(f"Scraped {len(coins)} coins")

filename = os.path.join(os.getcwd(), "pprices.csv")
if os.path.exists(filename):
    df.to_csv(filename, mode='a', index=False, header=False)
else:
    df.to_csv(filename, index=False)

print(f"CSV saved to: {filename}")
print(df)

driver.quit()