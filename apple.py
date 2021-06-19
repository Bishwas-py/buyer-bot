from chromedriver_py import binary_path
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep as wait
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from decouple import config

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

def typeKeys(input, key:str):
    for letter in key:
        wait(0.01)
        input.send_keys(letter)

def getDriver(profile:str):
    options = webdriver.ChromeOptions()
    options.add_argument('--maximized')
    options.add_argument(f'--user-data-dir=D:\Projects\profile\{profile}')
    driver = webdriver.Chrome(executable_path=binary_path, options=options)
    return driver

class Bots:
    def __init__(self, driver):
        self.driver = driver

    def apple(self, link="https://www.apple.com/airpods/"):
        driver = self.driver

        email = config('EMAIL')
        password = config('PASSWORD')
        
        driver.get("https://www.apple.com")

        getElement = waitGetElm(driver)

        getElement.now(By.XPATH, '//*[@id="ac-gn-bag"]/div/a').click()

        getElement.now(By.XPATH, '//*[@id="ac-gn-bagview-content"]/nav/ul/li[5]/a').click()

        emailInput = getElement.now(By.XPATH, '//*[@id="signIn.customerLogin.appleId"]')
        typeKeys(emailInput, email)

        passwordInput = getElement.now(By.XPATH, '//*[@id="signIn.customerLogin.password"]')
        typeKeys(passwordInput, password)

        passwordInput.send_keys(Keys.RETURN)


    def bestbuy(driver):
        email = 'ayaz.parbtani@gmail.com'
        password = 'Aparb003@'
        driver.get("https://www.bestbuy.com/cart")
        try:
            driver.find_element_by_xpath('/html/body/div[2]/div/div/div/div[1]/div[2]/a[2]').click()
        except:
            pass
        
        driver.find_element_by_class_name('account-button').click()
        wait(3)
        driver.find_element_by_class_name('sign-in-btn').click()

        # login part
        # try:
        emailInput = driver.find_element_by_xpath('//*[@id="fld-e"]')
        typeKeys(emailInput, email)

        passwordInput = driver.find_element_by_xpath('//*[@id="fld-p1"]')
        typeKeys(passwordInput, password)

        passwordInput.send_keys(Keys.RETURN)
        # except:
        #     pass

        
        wait(2)
    
# bestbuy(getDriver("bestbuy"))
driver = getDriver("bestbuy")
bot = Bots(driver)
bot.apple()