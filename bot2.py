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

    def bestbuy(self, link:str="", quantity=1, skip=False, clear_cart=False):
        driver = self.driver
        getElement = waitGetElm(driver)
        driver.get("https://www.bestbuy.com")
        if not skip:
            try:
                driver.find_element_by_xpath('//*[@id="survey_invite_no"]').click()
            except:
                pass
            
            try:
                driver.find_element_by_xpath("/html/body/div[2]/div/div/div/div[1]/div[2]/a[2]").click()
            except:
                pass

            try:
                driver.find_element_by_xpath(By.XPATH, '//*[@id="widgets-view-email-modal-mount"]/div/div/div[1]/div/div/div/div/button').click()
            except:
                pass

            try:
                print("Try...")
                driver.find_element_by_xpath('//button[contains(@class, "account-button")]//*[contains(text(), "Account")]').click()
                print("Try.....")
                driver.find_element_by_xpath('//a[contains(@class, "sign-in-btn")][contains(text(), "Sign In")]').click()
                print("Try.......")
                skipAllProcess = False
            except:
                skipAllProcess = True
        else:
            skipAllProcess = True

        if not skipAllProcess:
            try:
                emailInput = driver.find_element_by_xpath('//*[@id="fld-e"]')
                passwordInput = driver.find_element_by_xpath('//*[@id="fld-p1"]')
                typeKeys(emailInput, "BESTBUY_EMAIL")
                typeKeys(passwordInput, "BESTBUY_PASSWORD")
                driver.find_element_by_xpath('/html/body/div[1]/div/section/main/div[2]/div[1]/div/div/div/div/form/div[3]/button').click()
            except Exception as inst:
                d = inst
                print(d)

            try:
                driver.find_element_by_xpath('/html/body/div[1]/div/section/main/div[2]/div[1]/div/div/div/div/form/fieldset/fieldset/div[3]').click()
                driver.find_element_by_xpath('/html/body/div[1]/div/section/main/div[2]/div[1]/div/div/div/div/form/div/button').click()
                
                # confirm verification
                continueVerification = True
                while continueVerification:
                    print('CHECKING...')
                    verificationCodeinput = driver.find_element_by_xpath('//*[@id="verificationCode"]')
                    typeKeys(verificationCodeinput, get_verification_code(FindWith.BESTBUY))
                    try:
                        errorMsg = driver.find_element_by_xpath('/html/body/div[1]/div/section/main/div[2]/div[1]/div/div/div[1]/div')
                        driver.find_element_by_xpath('/html/body/div[1]/div/section/main/div[2]/div[1]/div/div/div/div/form/div[2]/button').click()
                        wait(5)
                    except:
                        continueVerification = False
                        verificationCodeinput.sendKeys(Keys.DELETE)

                # Now we gonna be setting new password...
                newPasswordInput = driver.find_element_by_xpath('//*[@id="fld-p1"]')
                confNewPasswordInput = driver.find_element_by_xpath('//*[@id="reenterPassword"]')
                typeKeys(newPasswordInput, config("BESTBUY_NEWPASSWORD"))
                typeKeys(confNewPasswordInput, config("BESTBUY_NEWPASSWORD"))
                
                # save and continue
                driver.find_element_by_xpath('/html/body/div[1]/div/section/main/div[2]/div[1]/div/div/div/div/form/div[4]/button').click()
            except Exception as inst:
                d = inst
                print(d)
        if clear_cart:
            driver.get('https://www.bestbuy.com/cart')
            removeBtnPath = '//a[@class="btn-default-link link-styled-button cart-item__remove"][contains(text(), "Remove")]'
            removeBtn = driver.find_elements_by_xpath(removeBtnPath)
            for i in range(len(removeBtn)):
                button = getElement.now_clikable(By.XPATH, f"{removeBtnPath}[{i+1}]")
                button.click()
            driver.quit()
        else:
            while True:
                driver.get(link)
                price = driver.find_element_by_xpath("//*[contains(@class, 'priceView-customer-price')]/span")
                price = get_price(price)
                # get price
                if int(config('BESTBUY_MIN')) < price < int(config('BESTBUY_MAX'))+1:
                    # Click on "Add to cart"
                    getElement.now(By.CLASS_NAME, 'add-to-cart-button').click()
                    # Click on go to cart
                    driver.find_element_by_xpath("//*[contains(@class, 'go-to-cart-button')]/a").click()
                    # select quantity
                    try:
                        driver.find_element_by_xpath("//*[contains(@class, 'fluid-item__quantity')]/option[10]").click()
                    except:
                        print("\nSkipped.....\n")

                    quantityInput = driver.find_element_by_xpath("//*[contains(@class, 'fluid-item__quantity')]/input[1]")
                    
                    quantityInput.send_keys(Keys.CONTROL + "a");
                    quantityInput.send_keys(Keys.DELETE);
                    wait(5)
                    quantityInput.send_keys(quantity)
                    break


driver = getDriver("Ayaz Prasjit")
bot = Bots(driver)
link = 'https://www.bestbuy.com/site/microsoft-surface-pro-7-12-3-touch-screen-intel-core-i3-4gb-memory-128gb-ssd-with-black-type-cover-latest-model-platinum/6374985.p?skuId=6374985'
bot.bestbuy(link, 10, skip=True, clear_cart=True)