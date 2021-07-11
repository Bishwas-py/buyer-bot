from time import sleep as wait, time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium import webdriver
from decouple import config
from chromedriver_py import binary_path

def get_price(price):
    price = float(price.text.split('$')[-1].strip('\n'))
    return price


def PressAndHold(getElement):
    while True:
        try:
            wait(2)
            element = getElement.now(By.XPATH, '/html/body/div/div/div[1]/div/div')
            action = ActionChains(driver)
            action.click_and_hold(on_element = element)
            action.perform()
            try:
                warning = getElement.now(By.XPATH, '//*[@id="px-captcha"]/p')
            except:
                break
        except:
            print("\nNo need \n")
            break


def typeKeys(input, key:str):
    try:
        key = config(key)
    except:
        pass
    for letter in key:
        wait(0.01)
        input.send_keys(letter)


class waitGetElm:
    def __init__(self, driver:webdriver.Chrome):
        self.driver = driver

    def now(self, by_, object, multi=False, waitTime=10):
        waitTill = WebDriverWait(self.driver, waitTime)
        if multi:
            elementEC = EC.visibility_of_all_elements_located((by_, object))
        if not multi:
            elementEC = EC.visibility_of_element_located((by_, object))
        return waitTill.until(elementEC) 
    
    def now_clikable(self, by_, object, waitTime=10):
        waitTill = WebDriverWait(self.driver, waitTime)
        elementEC = EC.element_to_be_clickable((by_, object))
        return waitTill.until(elementEC) 

    def now_visible(self, by_, object, waitTime=10):
        waitTill = WebDriverWait(self.driver, waitTime)
        elementEC = EC.visibility_of_element_located((by_, object))
        return waitTill.until(elementEC) 
    

def PressAndHold(driver, element:waitGetElm):
    current_url = driver.current_url
    print(current_url)
    while True:
        wait(3)
        element = element.now_visible(By.XPATH, "//div[@id='px-captcha']", 5)
        action = ActionChains(driver)
        action.click_and_hold(on_element = element)
        action.perform()
        try:
            warning = element.now(By.XPATH, '//*[@id="px-captcha"]/p')
        except:
            pass
        while current_url == driver.current_url:
            wait(1)
        if "blocked?url" != driver.current_url:
            break


def getDriver(profile:str):
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--no-sandbox') # Bypass OS security model
    options.add_argument('--disable-blink-features=AutomationControlled') # For ChromeDriver version 79.0.3945.16 or over
    options.add_experimental_option("excludeSwitches", ["enable-automation"]) # For older ChromeDriver under version 79.0.3945.16
    options.add_experimental_option('useAutomationExtension', False)

    options.add_argument(f'--user-data-dir=D:\Projects\profile\{profile}')
    driver = webdriver.Chrome(executable_path=binary_path, options=options)
    return driver

