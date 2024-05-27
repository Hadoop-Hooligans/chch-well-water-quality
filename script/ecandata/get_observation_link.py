from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException


def get_obs_link(well_code):
    """This function takes a well code and returns the url (and the ID) of the most recent water quality report"""
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')  # Run Chrome in headless mode
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--remote-debugging-port=9222')  # This line is important
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-software-rasterizer')
    #chrome_options.add_argument("--headless=new")

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    baseurl = "https://www.ecan.govt.nz/data/well-search/"

    driver.get(baseurl)

    input_field_xpath = """//*[@id="WellsSearchForm-keywords"]"""
    input_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, input_field_xpath)))
    input_field.send_keys(well_code)
    input_field.send_keys(Keys.RETURN)

    table_xpath = """//*[@id="well-search-results"]"""
    table = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, table_xpath)))
    first_link = table.find_element(By.TAG_NAME, 'a')

    link_href = first_link.get_attribute('href')
    link_text = first_link.text
    driver.quit()
    return link_href, link_text


print(get_obs_link('I39-0007'))
