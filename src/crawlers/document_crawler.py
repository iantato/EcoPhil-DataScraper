from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from crawlers import driver, wait
from handlers.error_handler import intercommerce_login_error
from src.handlers.validate_data import (validate_if_date_after, validate_if_date_before, validate_data_status,
                                     is_released, is_transferred, is_approved)
from config.secrets import intercommerce_urls

def login(retries = 3) -> None:
    driver.get('https://www.intercommerce.com.ph/login.asp?home=home')
    intercommerce_login_error(retries)

def get_documents(company_branch: str) -> list[list[dict]]:
    driver.get(intercommerce_urls[company_branch])
    data = list([])

    for row_idx in range(15, 25):
        driver.get(intercommerce_urls['main'])
        row_xpath = f'/html/body/form/table/tbody/tr[9]/td[2]/table/tbody/tr/td/div/table/tbody/tr/td/table/tbody/tr[{row_idx}]/td'
        content = wait.until(EC.presence_of_all_elements_located((By.XPATH, row_xpath)))

        row_data = [i.text.strip() for i in content]

        if validate_if_date_before(row_data[-1]):
            return data
        elif validate_if_date_after(row_data[-1]) or not validate_data_status(row_data[1]):
            continue
        else:
            document_data = get_document_data(row_data[0][2:])
            raw_data = dict({'Document Number': row_data[6], 'Raw Date': row_data[-1]})
            release_table = get_document_released()

            data.append(document_data | raw_data | release_table)

    return data

def get_document_released() -> dict[str, list[str]]:
    table_xpath = '/html/body/form/table/tbody/tr[8]/td[2]/div/table'
    table_data = dict({
        'released': [],
        'transferred': [],
        'approved': []
    })

    try:
        content = wait.until(EC.presence_of_all_elements_located((By.XPATH, table_xpath)))
    except NoSuchElementException:
        return table_data

    for row in content[1:]:
        row_data = row.text.split(' ')

        if is_released(row_data):
            table_data['released'] = row_data
        elif is_transferred(row_data):
            table_data['transferred'] = row_data
        elif is_approved(row_data):
            table_data['approved'] = row_data

    return table_data

def get_document_data(reference_no: str) -> dict[str, str]:
    driver.get(f'https://www.intercommerce.com.ph/WebCWS/cws_ip_step2PEZAEXPexpress.asp?ApplNo={reference_no}')

    container_type = wait.until(EC.presence_of_element_located((By.NAME, 'txtTotContType')))
    packages = wait.until(EC.presence_of_element_located((By.NAME, 'txtPackages')))
    invoice_number = wait.until(EC.presence_of_element_located((By.NAME, 'txtInvNo')))

    return dict({'reference_no': reference_no,
                 'container_type': container_type.get_attribute('value'),
                 'packages': packages.get_attribute('value'),
                 'invoice_number': invoice_number.get_attribute('value')})