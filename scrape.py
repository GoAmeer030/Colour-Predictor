from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

import pandas as pd

from dotenv import load_dotenv

import time
import os
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('scrape.log')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

load_dotenv()

LOGIN_NUMBER = os.getenv('LOGIN_NUMBER')
LOGIN_PASSWORD = os.getenv('LOGIN_PASSWORD')

SITE_URL = os.getenv('SITE_URL')

XPATH_NUMBER_INPUT = '/html/body/div/div[1]/div[1]/input'
XPATH_PASSWORD = '/html/body/div/div[1]/div[2]/input'
XPATH_LOGIN_BUTTON = '/html/body/div/div[1]/div[3]/button'
XPATH_LOGIN_SUCCESS = '/html/body/div/div[1]/div/div[1]/div[1]/ul/li[1]'
XPATH_WIN_BUTTON = '/html/body/div/div[4]/ul/li[3]'
XPATH_TABLE = '/html/body/div/div[2]/div[2]/div[3]/div/div[2]/table'
XPATH_NEXT_BUTTON = '/html/body/div/div[2]/div[2]/div[3]/div/div[3]/ul/li[2]/i[2]'

FILE_NAME = "data.csv"
TIME_INTERVAL = 180

def remove_duplicates():
    df = pd.read_csv(FILE_NAME, header=None)
    df = df.drop_duplicates()
    df.to_csv(FILE_NAME, index=False, header=None)

def login():
    number_input = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, XPATH_NUMBER_INPUT)))
    number_input.send_keys(LOGIN_NUMBER)

    password = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, XPATH_PASSWORD)))
    password.send_keys(LOGIN_PASSWORD)

    login_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, XPATH_LOGIN_BUTTON)))
    login_button.click()

    if WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, XPATH_LOGIN_SUCCESS))):
        logger.info('Login Success')
    else:
        logger.error('Login Failed')

def scrape_data():
    table_data = []

    table = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, XPATH_TABLE)))

    table_html = table.get_attribute('outerHTML')
    soup = BeautifulSoup(table_html, 'html.parser')

    table = soup.find('table', {'data-v-5a358a5e': ''})

    if table:
        rows = table.find('tbody').find_all('tr', {'data-v-5a358a5e': ''})

        for row in rows:
            cells = row.find_all('td', {'data-v-5a358a5e': ''})
            period = cells[0].text.strip()
            price = cells[1].text.strip()
            number = cells[2].text.strip()
            result_span = cells[3].find('span')

            result_style = result_span.get('style')
            if 'background: red;' in result_style:
                result_color = 1
            elif 'background: green;' in result_style:
                result_color = 2
            elif 'background: violet;' in result_style:
                result_color = 3
            
            table_data.append([period, price, number, result_color])

    return table_data

def save_data(table_data):
    df = pd.DataFrame(table_data)

    old_df = pd.read_csv(FILE_NAME, header=None)
    new_df = df[~df.isin(old_df).all(axis=1)]

    first = not os.path.exists(FILE_NAME) or os.path.getsize(FILE_NAME) == 0
    new_df.to_csv(FILE_NAME, mode="a", index=False, header=first)
    logger.info('Data updated')
    
if __name__ == '__main__':
    
    option = webdriver.EdgeOptions()
    option.add_argument('--disable-extensions')
    option.add_experimental_option('useAutomationExtension', False)
    
    driver = webdriver.Edge(options=option)

    driver.get(SITE_URL)

    try:
        login()
    except Exception as e:
        logger.error(f'An error occurred while logging in: {e}')

    win_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, XPATH_WIN_BUTTON)))
    win_button.click()

    time.sleep(5)

    while True:
        count = 0

        if count == 0:
            for _ in range(120):
                try:
                    table_data = scrape_data()
                except Exception as e:
                    logger.error(f'An error occurred while scraping the data: {e}')
                    break

                try:
                    save_data(table_data)
                except Exception as e:
                    logger.error(f'An error occurred while saving the data: {e}')
                    break

                next_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, XPATH_NEXT_BUTTON)))
                driver.execute_script("arguments[0].click()", next_button)

            count += 1

        else:
            try:
                table_data = scrape_data()
            except Exception as e:
                logger.error(f'An error occurred while scraping the data: {e}')
                break

            try:
                save_data(table_data)
            except Exception as e:
                logger.error(f'An error occurred while saving the data: {e}')
                break

        remove_duplicates()
        
        logger.info('Waiting for 3 minutes')
        time.sleep(TIME_INTERVAL)
