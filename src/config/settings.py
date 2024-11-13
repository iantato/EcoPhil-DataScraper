from pathlib import Path
from selenium import webdriver

# Parent directory for data.
DATA_DIR = Path().resolve() / 'data'


# Webdriver Chrome options.
chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--enable-chrome-browser-cloud-management')
chrome_options.add_experimental_option('prefs', {
    'download.default_directory': str(DATA_DIR),
    'download.prompt_for_download': False,
    'download.directory_upgrade': True,
    'plugins.always_open_pdf_externally': True,
    'safebrowsing.enabled': True
})


# Global Delays.
WAIT_DELAY = 30
SLEEP_DELAY = 1