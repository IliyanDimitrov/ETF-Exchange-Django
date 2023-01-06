
## Run selenium and chrome driver to scrape data from cloudbytes.dev
import time
import os.path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import unittest

## Setup chrome options
chrome_options = Options()
chrome_options.add_argument("--headless") # Ensure GUI is off (WSL requirement)
chrome_options.add_argument("--no-sandbox")

# Set path to chromedriver as per your configuration
homedir = os.path.expanduser("~")
webdriver_service = Service(f"{homedir}/chromedriver/stable/chromedriver")

# Choose Chrome Browser
browser = webdriver.Chrome(service=webdriver_service, options=chrome_options)

# Get page
class UserProfilePageTest(unittest.TestCase):

    def test_display_user_information(self):
        # Navigate to the user profile page
        browser.get('http://127.0.0.1:8000' + '/profile')

        # Find the user's name element and verify its text
        name_element = browser.find_element_by_id('account-heading')
        self.assertEqual(name_element.text, self.user.username)

        # Find the user's email element and verify its text
        email_element = browser.find_element_by_id('text-secondary')
        self.assertEqual(email_element.text, self.user.email)

        # Find the user's first name element and verify its text
        first_name_element = browser.find_element_by_id('text-secondary')
        self.assertEqual(first_name_element.text, self.user.first_name)

        # Find the user's last name element and verify its text
        last_name_element = browser.find_element_by_id('text-secondary')
        self.assertEqual(last_name_element.text, self.user.last_name)

        # Find the user's DOB element and verify its text
        dob_element = browser.find_element_by_id('text-secondary')
        self.assertEqual(dob_element.text, self.user.profile.dob)

        # Find the user's address element and verify its text
        address_element = browser.find_element_by_id('text-secondary')
        self.assertEqual(address_element.text, self.user.profile.address)
        
if __name__ == '__main__':
    unittest.main()

#Wait for 10 seconds
time.sleep(10)
browser.quit()