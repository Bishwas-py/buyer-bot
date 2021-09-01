import warnings
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep as wait
from selenium.webdriver.common.by import By
from decouple import config
from.read_inbox import get_verification_code, FindWith
from.additionals import *
from selenium.common.exceptions import TimeoutException

from ..models import Settings

class Bots:
    def __init__(self, driver:webdriver.Chrome):
        self.driver = driver

    def bestbuy(self, item, thread_no=0):
        try:
            driver = self.driver
            getElement = waitGetElm(driver)
            driver.get("https://www.bestbuy.com")
            if not item.skip:
                try:
                    driver.find_element_by_xpath('//div[contains(@class, "country-selection")]//a[contains(@class, "us-link")]//img[1]').click()
                except:
                    pass
                try:
                    driver.find_element_by_xpath('//*[@id="survey_invite_no"]').click()
                except:
                    pass
                try:
                    driver.find_element_by_xpath('//button[@class="c-close-icon c-modal-close-icon"]').click()
                except:
                    pass

                try:
                    driver.find_element_by_xpath(By.XPATH, '//*[@id="widgets-view-email-modal-mount"]/div/div/div[1]/div/div/div/div/button').click()
                except:
                    pass

                try:
                    driver.find_element_by_xpath('//button[contains(@class, "account-button")]//*[contains(text(), "Account")]').click()
                    driver.find_element_by_xpath('//a[contains(@class, "sign-in-btn")][contains(text(), "Sign In")]').click()
                    notSkipAllProcess = True
                except:
                    notSkipAllProcess = False
                    item.skip = False
                    item.save()
                    
            else:
                notSkipAllProcess = False

            if notSkipAllProcess:
                try:
                    emailInput = driver.find_element_by_xpath('//*[@id="fld-e"]')
                    passwordInput = driver.find_element_by_xpath('//*[@id="fld-p1"]')
                    typeKeys(emailInput, item.account.email)
                    typeKeys(passwordInput, item.account.password)
                    driver.find_element_by_xpath('/html/body/div[1]/div/section/main/div[2]/div[1]/div/div/div/div/form/div[3]/button').click()
                except Exception as inst:
                    d = inst
                    print(d)
                try:
                    try:
                        driver.find_element_by_xpath('/html/body/div[1]/div/section/main/div[2]/div[1]/div/div/div/div/form/fieldset/fieldset/div[3]').click()
                    except Exception as inst:
                        d = inst
                        print(d)
                        print("Skipped...")
                    try:
                        driver.find_element_by_xpath('/html/body/div[1]/div/section/main/div[2]/div[1]/div/div/div/div/form/div/button').click()
                    except Exception as inst:
                        d = inst
                        print(d)
                        print("Skipped...")
                    
                    # confirm verification
                    continueVerification = item.need_verification
                    while continueVerification:
                        print('Doing Verification...')
                        try:
                            verificationCodeinput = driver.find_element_by_xpath('//*[@id="verificationCode"]')
                            typeKeys(verificationCodeinput, get_verification_code(FindWith.BESTBUY))
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
        
            refresh_delay = Settings.objects.first().refresh_delay
            while True:
                driver.get(item.link)
                price = driver.find_element_by_xpath("//*[contains(@class, 'priceView-customer-price')]/span")
                price = get_price(price)
                
                # get price
                if item.min_price < price < item.max_price+1:
                    # Click on "Add to cart"
                    getElement.now(By.CLASS_NAME, 'add-to-cart-button').click()
                    # Click on go to cart
                    driver.find_element_by_xpath("//*[contains(@class, 'go-to-cart-button')]/a").click()
                    # select quantity
                    
                    try:
                        driver.find_element_by_xpath(f"//*[contains(@class, 'fluid-item__quantity')]/option[{item.quantity}]").click()
                    except Exception as inst:
                        d = inst
                        print(d)
                        print("Quantity in dropdown not selected.")
                    
                    # finally buy the product
                    if not item.is_test:
                        driver.find_element_by_xpath('//*[@id="cartApp"]//*[contains(@class, "checkout-buttons__checkout")]').click()
                    
                    break
                wait(refresh_delay)
                    
                from.main import quit_bot
                quit_bot(thread_no)
                
        except:
            quit_bot(thread_no, witherror=True)
            
    def clear_cart(self):
        driver = self.driver
        getElement = waitGetElm(driver)
        driver.get('https://www.bestbuy.com/cart')
        removeBtnPath = '//a[@class="btn-default-link link-styled-button cart-item__remove"][contains(text(), "Remove")]'
        removeBtn = driver.find_elements_by_xpath(removeBtnPath)
        for i in range(len(removeBtn)):
            button = getElement.now_clikable(By.XPATH, f"{removeBtnPath}[{i+1}]")
            button.click()
        driver.quit()