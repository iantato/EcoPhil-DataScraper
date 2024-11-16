from time import sleep

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from crawlers import driver, wait
from config.settings import SLEEP_DELAY
from config.secrets import vbs_credentials, intercommerce_credentials

# CSV file download handler.
def csv_wait_and_retry(delay = 100, retries = 3) -> None:
    for attempt in range(retries):

        # Request for data.
        wait.until(EC.element_to_be_clickable((By.ID, 'PointsTransactionsSearchForm___REFERENCE'))).click()
        driver.implicitly_wait(SLEEP_DELAY)
        wait.until(EC.element_to_be_clickable((By.ID, 'Search'))).click()

        # Download the data.
        try:
            WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.ID, 'CSV'))).click()
            return
        except TimeoutException:
            print(f'Attempt {attempt + 1} failed; Retrying...')

    print(f'Failed to download csv after {retries} retries.')

# VBS Login error handler.
def vbs_login_error(retries = 3) -> None:
    for attempt in range(retries):
        wait.until(EC.element_to_be_clickable((By.ID, 'USERNAME'))).send_keys(vbs_credentials['username'])
        wait.until(EC.element_to_be_clickable((By.ID, 'PASSWORD'))).send_keys(vbs_credentials['password'])

        # Login.
        wait.until(EC.presence_of_element_located((By.ID, 'form1'))).submit()

        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'vbs_new_selected_facilityid')))
            return
        except TimeoutException:
            print(f'Attempt {attempt + 1} failed; Wrong Password...')
            vbs_credentials['username'] = input('Enter new username: ')
            vbs_credentials['password'] = input('Enter new password: ')
            continue

    print(f'Failed to login into vbs.1-stop.biz after {retries} retries.')

def intercommerce_login_error(retries = 3) -> None:
    for attempt in range(retries):
        wait.until(EC.element_to_be_clickable((By.NAME, 'clientid'))).send_keys(intercommerce_credentials['username'])
        wait.until(EC.element_to_be_clickable((By.NAME, 'password'))).send_keys(intercommerce_credentials['password'])

        # Login.
        wait.until(EC.presence_of_element_located((By.NAME, 'form1'))).submit()

        sleep(SLEEP_DELAY)
        if (driver.title != "InterCommerce Network Services - Member's Page"):
            print(f'Attempt {attempt + 1} failed; Wrong Password...')
            intercommerce_credentials['username'] = input('Enter new username: ')
            intercommerce_credentials['password'] = input('Enter new password: ')
            continue
        else:
            return