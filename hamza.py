import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = 'https://www.avito.ma/fr/maroc/voitures-à_vendre'

driver = webdriver.Chrome()
driver.get(url)

# Create an empty list to store phone numbers
phone_numbers = []

# Loop indefinitely to check for new phone numbers
while True:
    # Extract links to all vehicle posts on the first page
    links = []
    posts = driver.find_elements("xpath", '//*[@id="__next"]/div/main/div/div[6]/div[1]/div/div[2]')
    for post in posts:
        link = post.find_element("xpath", './/a').get_attribute('href')
        links.append(link)

    # Extract phone numbers from each vehicle post
    for link in links:
        driver.get(link)
        try:
            # Click the button to reveal the phone number
            button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div/main/div/div[3]/div[1]/div[2]/div[1]/div[1]/div[2]/div[2]/div/div/div/div[4]/button[2]')))
            button.click()

            # Get the phone number
            phone_number = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/div/main/div/div[2]/div/div/div/div/a/span/span')))
            phone_number = phone_number.text.strip()

            # Check if the phone number is new
            if phone_number not in phone_numbers:
                # Save the phone number to a file
                with open('phone_number.txt', 'a') as f:
                    f.write(phone_number + '\n')
                phone_numbers.append(phone_number)

                print(phone_number)

        except:
            print("Phone number not found")

    # Refresh the main page to check for new posts
    driver.quit()
    driver = webdriver.Chrome()
    time.sleep(6)
    driver.get(url)
    time.sleep(5)

driver.quit()