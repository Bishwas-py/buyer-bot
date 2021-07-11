import warnings
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep as wait
from selenium.webdriver.common.by import By
from decouple import config
from read_inbox import get_verification_code, FindWith
from additionals import *



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
                signInOn = True
                while signInOn:
                    emailInput = getElement.now(By.XPATH, '//*[@id="signIn.customerLogin.appleId"]')
                    typeKeys(emailInput, 'APPLE_EMAIL')

                    passwordInput = getElement.now(By.XPATH, '//*[@id="signIn.customerLogin.password"]')
                    typeKeys(passwordInput, 'APPLE_PASSWORD')
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
        price = float(getElement.now(By.XPATH, '//*[@id="root"]/div[3]/div[1]/div[1]/div/div[1]/div/span').text.replace('$',''))
        print(price)

        if price_range[0] < price < price_range[1]+1:
            getElement.now(By.ID, "add-to-cart").click() # click on Add to  cart
            getElement.now(By.ID, "shoppingCart.actions.checkout").click() # click on Add to  cart

    def bestbuy(self, link:str, price_range:tuple, quantity=1, skip=False):
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

        driver.get(link)

        price = getElement.now(By.XPATH, "//*[contains(@class, 'priceView-customer-price')]/span")
        price = get_price(price)
        
        # get price
        if price_range[0] < price_range[0]+1:
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
    
    def walmart(self, link:str, price_range:tuple, quantity=1, skip=False):
        driver = self.driver
        getElement = waitGetElm(driver)
        driver.get("https://www.walmart.com/account/login?tid=0&returnUrl=%2F")
        PressAndHold(driver, getElement)

        try:
            # Account Login stuff
            emailInput = getElement.now(By.XPATH, '//*[@id="email"]')
            passwordInput = getElement.now(By.XPATH, '//*[@id="password"]')
            typeKeys(emailInput, "WALMART_EMAIL")
            typeKeys(passwordInput, "WALMART_PASSWORD")
            # press the sign in button
            getElement.now(By.XPATH, '//*[@id="sign-in-form"]/div[1]/div/button').click()
        except:
            pass
        PressAndHold(driver, getElement)
        driver.get(link)

        price = get_price(getElement.now(By.XPATH, '//*[@id="price"]/div/span[1]/span/span[2]'))
        print(f"{price}: {price_range[0] < price < price_range[1]+1}")
        if price_range[0] < price < price_range[1]+1:
            quantityInput = getElement.now(By.XPATH, f'//*[@id="add-on-atc-container"]/div[1]/section/div[1]/div[2]/select/option[{quantity}]')
            quantityInput.click()
            getElement.now(By.XPATH, '//*[@id="add-on-atc-container"]/div[1]/section/div[1]/div[3]/button').click() # add to cart
            getElement.now(By.XPATH, "//div[contains(@class, 'cart-pos-proceed-to-checkout')]/div/button//*[contains(text(),'Check out')][1]").click() # check out
            getElement.now(By.XPATH, "//button[contains(@class, 'cxo-continue-btn')]//*[contains(text(),'Continue')][1]").click() # continue
            PressAndHold(driver, getElement)
            
            





driver = getDriver("Ayaz Prajapati")
bot = Bots(driver)
link = 'https://www.walmart.com/ip/Instant-Power-Heavy-Duty-Drain-Opener-67-6-fl-oz/17133603'
bot.walmart(link, (0, 10), 2, True)