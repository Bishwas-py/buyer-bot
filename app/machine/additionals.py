from app.models import Settings
from random import choice
from time import sleep as wait, time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from chromedriver_py import binary_path

def get_price(price) -> float:
    price = float(price.text.split('$')[-1].strip('\n'))
    return price

def typeKeys(input, key:str) -> None:
    for letter in key:
        wait(choice([0.01, 0.09, 0.03, 0.08]))
        input.send_keys(letter)
    wait(choice([0.6, 0.5, 0.1, 0.9]))


def getDriver(profile:str) -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--no-sandbox') # Bypass OS security model
    options.add_argument('--disable-blink-features=AutomationControlled') # For ChromeDriver version 79.0.3945.16 or over
    options.add_experimental_option("excludeSwitches", ["enable-automation"]) # For older ChromeDriver under version 79.0.3945.16
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--remote-debugging-port=9222")  # this

    if Settings.objects.first().headless:
        options.add_argument('--headless')

    options.add_argument(f'--user-data-dir=profile/{profile}')
    driver = webdriver.Chrome(executable_path=binary_path, options=options)
    driver.implicitly_wait(15)
    return driver

def clearInput(*WebElements:tuple):
    for element in WebElements:
        element.send_keys(Keys.CONTROL, 'a')
        element.send_keys(Keys.DELETE)