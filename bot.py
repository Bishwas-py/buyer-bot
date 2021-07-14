import warnings
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep as wait
from selenium.webdriver.common.by import By
from decouple import config
from read_inbox import get_verification_code, FindWith
from additionals import *
from selenium.common.exceptions import TimeoutException

class Bots:
    def __init__(self, driver:webdriver.Chrome):
        self.driver = driver

    def bestbuy(self, link:str, quantity=1, skip=False):
        driver = self.driver
        getElement = waitGetElm(driver)
        driver.get("https://www.bestbuy.com")

        if not skip:
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
        else:
            skipAllProcess = True

        if not skipAllProcess:
            try:
                emailInput = getElement.now(By.XPATH, '//*[@id="fld-e"]',waitTime=5)
                passwordInput = getElement.now(By.XPATH, '//*[@id="fld-p1"]',waitTime=5)
                typeKeys(emailInput, "BESTBUY_EMAIL")
                typeKeys(passwordInput, "BESTBUY_PASSWORD")
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
                        wait(5)
                    except:
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
        while True:
            driver.get(link)

            price = getElement.now(By.XPATH, "//*[contains(@class, 'priceView-customer-price')]/span")
            price = get_price(price)
            # get price
            if int(config('BESTBUY_MIN')) < price < int(config('BESTBUY_MAX'))+1:
                # Click on "Add to cart"
                getElement.now(By.CLASS_NAME, 'add-to-cart-button').click()
                # Click on go to cart
                getElement.now(By.XPATH, "//*[contains(@class, 'go-to-cart-button')]/a").click()
                # select quantity
                try:
                    getElement.now(By.XPATH, "//*[contains(@class, 'fluid-item__quantity')]/option[10]").click()
                except:
                    print("\nSkipped.....\n")

                quantityInput = getElement.now(By.XPATH, "//*[contains(@class, 'fluid-item__quantity')]/input[1]")
                quantityInput.send_keys(Keys.CONTROL + "a");
                quantityInput.send_keys(Keys.DELETE);
                wait(5)
                quantityInput.send_keys(quantity)
                
                break

driver = getDriver("Ayaz Pranjit")
bot = Bots(driver)
link = 'https://www.bestbuy.com/site/microsoft-surface-pro-7-12-3-touch-screen-intel-core-i3-4gb-memory-128gb-ssd-with-black-type-cover-latest-model-platinum/6374985.p?skuId=6374985'
bot.bestbuy(link, 10)