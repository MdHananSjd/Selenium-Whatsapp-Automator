import time
import csv
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

def create_csv_and_return_df():
    filename = "messages.csv"   
    columns = ["Number", "Message"]
    n = int(input("How many entries do you want to add? "))

    data = []
    for i in range(n):
        number = input(f"Enter number {i+1}: ")
        message = input(f"Enter message {i+1}: ")
        data.append([number, message])

    # Write to CSV 
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(columns)
        writer.writerows(data)

    # Return pandas DataFrame
    return pd.read_csv(filename)

# --- Load Contacts ---
print('''
Do you have the csv file ready to send?
if yes, type "1"
if no, type "0"
''')
choice = int(input("Enter choice: "))

if choice == 1:
    contacts = pd.read_csv("messages.csv")  # must have: number,message
else:
    contacts = create_csv_and_return_df()

options = Options() #Webdriver options class

#change this path to your chrome profile (this is mine)
options.add_argument("user-data-dir=/Users/mhs/Library/Application Support/Google/Chrome/Default")


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Opening WhatsApp Web
driver.get("https://web.whatsapp.com")
print("Scan QR code if not already logged in...")
time.sleep(15)  # delay for WhatsApp Web to load


for i, row in contacts.iterrows():
    number = str(row["number"])
    message = str(row["message"])

    url = f"https://web.whatsapp.com/send?phone={number}&text={message}"
    driver.get(url)
    time.sleep(10)  # delay for chat to load

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
