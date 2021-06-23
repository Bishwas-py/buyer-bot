from chromedriver_py import binary_path
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep as wait
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from decouple import config
import numpy
from read_inbox import get_verification_code, FindWith

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
    options.add_argument('--start-maximized')
    options.add_argument('--no-sandbox') # Bypass OS security model
    options.add_argument('--disable-blink-features=AutomationControlled') # For ChromeDriver version 79.0.3945.16 or over
    options.add_experimental_option("excludeSwitches", ["enable-automation"]) # For older ChromeDriver under version 79.0.3945.16
    options.add_experimental_option('useAutomationExtension', False)

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
            getElement.now(By.XPATH, '//*[@id="survey_invite_no"]', waitTime=3).click()
        except:
            pass
        
        try:
            getElement.now(By.XPATH, "/html/body/div[2]/div/div/div/div[1]/div[2]/a[2]", waitTime=3).click()
        except:
            pass

        try:
            getElement.now(By.XPATH, '//*[@id="widgets-view-email-modal-mount"]/div/div/div[1]/div/div/div/div/button',waitTime=3).click()
        except:
            pass

        try:
            getElement.now(By.CLASS_NAME, 'account-button',waitTime=5).click()
            getElement.now(By.CLASS_NAME, 'sign-in-btn',waitTime=5).click()
            skipAllProcess = False
        except:
            skipAllProcess = True
        if skipAllProcess:
            try:
                emailInput = getElement.now(By.XPATH, '//*[@id="fld-e"]',waitTime=5)
                passwordInput = getElement.now(By.XPATH, '//*[@id="fld-p1"]',waitTime=5)
                typeKeys(emailInput, config("BESTBUY_EMAIL"))
                typeKeys(passwordInput, config("BESTBUY_PASSWORD"))
                getElement.now(By.XPATH, '/html/body/div[1]/div/section/main/div[2]/div[1]/div/div/div/div/form/div[3]/button', waitTime=5).click()
            except Exception as inst:
                d = inst
                print(d)

            try:
                getElement.now(By.XPATH, '/html/body/div[1]/div/section/main/div[2]/div[1]/div/div/div/div/form/fieldset/fieldset/div[3]', waitTime=5).click()
                getElement.now(By.XPATH, '/html/body/div[1]/div/section/main/div[2]/div[1]/div/div/div/div/form/div/button', waitTime=5).click()
                
                # confirm verification
                continueVerification = True
                while continueVerification:
                    print('CHECKING...')
                    verificationCodeinput = getElement.now(By.XPATH, '//*[@id="verificationCode"]', waitTime=5)
                    typeKeys(verificationCodeinput, get_verification_code(FindWith.BESTBUY))
                    try:
                        errorMsg = getElement.now(By.XPATH, '/html/body/div[1]/div/section/main/div[2]/div[1]/div/div/div[1]/div', waitTime=5)
                        getElement.now(By.XPATH, '/html/body/div[1]/div/section/main/div[2]/div[1]/div/div/div/div/form/div[2]/button', waitTime=5).click()
                        print('WAITING...')
                        wait(5)
                    except:
                        print('ERROR...')
                        continueVerification = False
                        verificationCodeinput.sendKeys(Keys.DELETE)

                # Now we gonna be setting new password...
                newPasswordInput = getElement.now(By.XPATH, '//*[@id="fld-p1"]')
                confNewPasswordInput = getElement.now(By.XPATH, '//*[@id="reenterPassword"]')
                typeKeys(newPasswordInput, config("BESTBUY_NEWPASSWORD"))
                typeKeys(confNewPasswordInput, config("BESTBUY_NEWPASSWORD"))
                
                # save and continue
                getElement.now(By.XPATH, '/html/body/div[1]/div/section/main/div[2]/div[1]/div/div/div/div/form/div[4]/button').click()
            except Exception as inst:
                d = inst
                print(d)

        driver.get(link)
        price_tag = float(getElement.now(By.CLASS_NAME, 'price-box').text)
        print(price_tag)
        if price_range[0] < price_range[0]+1:
            print('Got it')

driver = getDriver("new_profile2")
bot = Bots(driver)
link = 'https://www.bestbuy.com/site/microsoft-surface-pro-7-12-3-touch-screen-intel-core-i5-8gb-memory-128gb-ssd-device-only-latest-model-platinum/6375055.p?skuId=6375055'
bot.bestbuy(link, (100, 199))