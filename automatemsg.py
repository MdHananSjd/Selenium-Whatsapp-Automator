import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

# --- Load Contacts ---
contacts = pd.read_csv("contacts.csv")  # must have: number,message


options = Options()
options.add_argument("user-data-dir=/Users/mhs/Library/Application Support/Google/Chrome/Default")  


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Open WhatsApp Web
driver.get("https://web.whatsapp.com")
print("Scan QR code if not already logged in...")
time.sleep(15)  # wait for WhatsApp Web to load


for i, row in contacts.iterrows():
    number = str(row["number"])
    message = str(row["message"])

    url = f"https://web.whatsapp.com/send?phone={number}&text={message}"
    driver.get(url)
    time.sleep(10)  # wait for chat to load

    try:
        # Focus the message box
        message_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
        message_box.send_keys(Keys.ENTER)  # simulate pressing enter
        print(f" Message sent to {number}")
    except Exception as e:
        print(f" Failed to send to {number}: {e}")

    time.sleep(5)

print("All messages processed ✅")
driver.quit()
