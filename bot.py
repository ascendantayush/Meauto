from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Single meeting link
meeting_link = "https://teams.microsoft.com/l/meetup-join/19%3ameeting_YmNiNzY2NWMtYzNmNy00Nzk1LWI5NzktZDQ4NTAzMzU1YWM4%40thread.v2/0?context=%7b%22Tid%22%3a%22d4963ce2-af94-4122-95a9-644e8b01624d%22%2c%22Oid%22%3a%226e60bcca-26fb-4e06-b2e9-bbda160702b8%22%7d"

# Number of users to simulate
num_users = 5  # Change this to the number of users you want

# Path to your ChromeDriver
webdriver_service = Service("C:\\Users\\lucif\\Downloads\\chromedriver\\chromedriver-win64\\chromedriver.exe")

# Store all the drivers for each user session
drivers = []

# Open new incognito windows for each user
for i in range(num_users):
    # Set up Chrome options for incognito mode
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--start-maximized")  # Optional: Maximize the window
    chrome_options.add_argument("--use-fake-ui-for-media-stream")  # Automatically allow media stream

    # Create a new instance of Chrome for each user
    driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)
    drivers.append(driver)

    # Go to the meeting link
    driver.get(meeting_link)

    # Wait and click "Continue on this browser"
    try:
        continue_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Join meeting from this browser"]'))
        )
        continue_button.click()
        print(f"User {i + 1} clicked Continue on this browser.")

        # Automatically click the "Join conversation" button
        join_conversation_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@data-tid="joinOnWeb"]'))
        )
        join_conversation_button.click()
        print(f"User {i + 1} clicked Join Conversation.")

        # Join the meeting
        try:
            join_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//button[text()="Join now"]'))
            )
            join_button.click()
            print(f"User {i + 1} joined meeting: {meeting_link}")

        except Exception as e:
            print(f"Error joining meeting for User {i + 1}: {e}")

    except Exception as e:
        print(f"Error clicking Continue on this browser for User {i + 1}: {e}")

# Keep the browser windows open for 1 hour (3600 seconds)
time.sleep(3600)

# Quit all drivers after the meeting duration
for driver in drivers:
    driver.quit()
