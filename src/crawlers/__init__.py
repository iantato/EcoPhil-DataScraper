from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from config.settings import chrome_options, WAIT_DELAY

# Initialize webdriver
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, WAIT_DELAY)