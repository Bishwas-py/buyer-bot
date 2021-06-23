from chromedriver_py import binary_path
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep as wait
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from decouple import config
import numpy

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
    def __init__(self, driver:webdriver.Chrome):
        self.driver = driver

    def apple(self, link:str, price_range:tuple):
        driver = self.driver
        getElement = waitGetElm(driver)
        
        driver.get("https://www.apple.com")

        try:
            getElement.now(By.XPATH, '//*[@id="ac-gn-bag"]/div/a').click()
            signInBtn = getElement.now(By.XPATH, '//*[@id="ac-gn-bagview-content"]/nav/ul/li[5]/a')
            if "sign out" not in signInBtn.text.lower():
                signInBtn.click()
                email = config('APPLE_EMAIL')
                password = config('APPLE_PASSWORD')
                signInOn = True
                while signInOn:
                    emailInput = getElement.now(By.XPATH, '//*[@id="signIn.customerLogin.appleId"]')
                    typeKeys(emailInput, email)

                    passwordInput = getElement.now(By.XPATH, '//*[@id="signIn.customerLogin.password"]')
                    typeKeys(passwordInput, password)
                    passwordInput.send_keys(Keys.RETURN)
                    wait(5)
                    print(driver.current_url)
                    try:
                        signIn = getElement.now(By.CLASS_NAME, 'form-button')
                        signIn.click()
                    except:
                        signInOn = False
        except:
            print("Sign In Faild")       

        driver.get(link)
        price_tag = float(getElement.now(By.XPATH, '//*[@id="root"]/div[3]/div[1]/div[1]/div/div[1]/div/span').text.replace('$',''))
        print(price_tag)

        if price_range[0] < price_range[0]+1:
            getElement.now(By.ID, "add-to-cart").click() # click on Add to  cart
            getElement.now(By.ID, "shoppingCart.actions.checkout").click() # click on Add to  cart
    def bestbuy(self, link:str, price_range:tuple):
        driver = self.driver
        getElement = waitGetElm(driver)
        driver.get("https://www.bestbuy.com")

        try:
            getElement.now(By.XPATH, "/html/body/div[2]/div/div/div/div[1]/div[2]/a[2]", waitTime=5).click()
        except:
            pass
        try:
            getElement.now(By.XPATH, '//*[@id="widgets-view-email-modal-mount"]/div/div/div[1]/div/div/div/div/button',waitTime=5).click()
        except:
            pass
        try:
            getElement.now(By.CLASS_NAME, 'account-button',waitTime=5).click()
            getElement.now(By.CLASS_NAME, 'sign-in-btn',waitTime=5).click()
        except:
            pass
        emailInput = getElement.now(By.XPATH, '//*[@id="fld-e"]',waitTime=5)
        passwordInput = getElement.now(By.XPATH, '//*[@id="fld-p1"]',waitTime=5)

        typeKeys(emailInput, config("BESTBUY_EMAIL"))
        typeKeys(passwordInput, config("BESTBUY_PASSWORD"))
        
        getElement.now(By.XPATH, '/html/body/div[1]/div/section/main/div[2]/div[1]/div/div/div/div/form/div[3]/button', waitTime=5).click()
        
        getElement.now(By.XPATH, '/html/body/div[1]/div/section/main/div[2]/div[1]/div/div/div/div/form/fieldset/fieldset/div[3]', waitTime=5).click()

        getElement.now(By.XPATH, '/html/body/div[1]/div/section/main/div[2]/div[1]/div/div/div/div/form/div/button', waitTime=5).click()


driver = getDriver("bestbuy")
bot = Bots(driver)
link = 'https://www.apple.com/us-hed/shop/product/MRXJ2AM/A/airpods-with-wireless-charging-case'
bot.bestbuy(link, (100, 199))