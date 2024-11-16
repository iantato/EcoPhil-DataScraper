from datetime import date, timedelta

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from config.settings import DATA_DIR
from crawlers import driver, wait
from handlers.error_handler import csv_wait_and_retry, vbs_login_error
from handlers.file_handler import move_file

# Login to the VBS website.
def login(retries = 3) -> None:

    driver.get('https://vbs.1-stop.biz/SignIn.aspx?errorCode=1')
    vbs_login_error(retries)

# Change the date range in the database.
def change_date(download_url: str, start_date: date, end_date: date) -> None:

    # Open the database download page.
    wait.until(EC.visibility_of_element_located((By.ID, 'NotifyMessages'))) # Implicitly waits for the page to be loaded.
    driver.get(download_url)
    end_date += timedelta(days = 1)

        # FROM
    date_from = wait.until(EC.presence_of_element_located((By.ID, 'PointsTransactionsSearchForm___DATEFROM')))
    driver.execute_script("arguments[0].removeAttribute('readonly')", date_from)
    date_from.clear()
    date_from.send_keys(f'{start_date:%d/%m/%Y}')
        # TO
    date_to = wait.until(EC.presence_of_element_located((By.ID, 'PointsTransactionsSearchForm___DATETO')))
    driver.execute_script("arguments[0].removeAttribute('readonly')", date_to)
    date_to.clear()
    date_to.send_keys(f'{end_date:%d/%m/%Y}')

'''
    Download Asian Terminal Inc. (ATI) data.
'''
def download_ati(start_date: date, end_date: date) -> None:

    # Accept terms & conditions.
    driver.get('https://atimnl.vbs.1-stop.biz/default.aspx?vbs_new_selected_FACILITYID=ATIMNL&vbs_Facility_Changed=true')
    wait.until(EC.presence_of_element_located((By.ID, 'Accept'))).click()

    # Change the website's date range.
    change_date('https://atimnl.vbs.1-stop.biz/PointsTransactions.aspx', start_date, end_date)

    # Download the data.
    csv_wait_and_retry()
    move_file(DATA_DIR / 'PointsTransactions.csv', DATA_DIR / 'sheets' / 'ati.csv')

'''
    Download Manila International Container Terminal Services Inc. (MICTSI) data.
'''
def download_mictsi(start_date: date, end_date: date) -> None:

    # Accept terms & conditions.
    driver.get('https://ictsi.vbs.1-stop.biz/Default.aspx?vbs_Facility_Changed=true&vbs_new_selected_FACILITYID=ICTSI')
    wait.until(EC.presence_of_element_located((By.ID, 'Accept'))).click()

    # Change the website's date range.
    change_date('https://ictsi.vbs.1-stop.biz/PointsTransactions.aspx', start_date, end_date)

    # Download the data.
    csv_wait_and_retry()
    move_file(DATA_DIR / 'PointsTransactions.csv', DATA_DIR / 'sheets' / 'mictsi.csv')