from app.machine.read_inbox import FindWith, get_verification_code
from selenium import webdriver
from time import sleep as wait
from selenium.webdriver.common.by import By
from.additionals import *
from .cursor_data import x_i, y_i
from inspect import currentframe, getframeinfo
frameinfo = getframeinfo(currentframe())

from ..models import Settings

class Bots:
    def __init__(self, driver:webdriver.Chrome):
        self.driver = driver
        self.action =  ActionChains(self.driver)
        self.getElement = waitGetElm(driver)
        
    def bestbuy_select_country(self):
        driver = self.driver
        try:
            driver.implicitly_wait(5)
            driver.find_element_by_xpath('//div[contains(@class, "country-selection")]//a[contains(@class, "us-link")]//img[1]').click()
            driver.implicitly_wait(15)
        except:
            pass
        
    def bestbuy_click(self, element:webdriver.Chrome.find_element=''):
        try:
            action = self.action
            if not element:
                element = self.driver.find_element_by_tag_name('body')
            # First, go to your start point or Element:
            action.move_to_element(element)
            action.perform()
            wait(choice([0.01, 0.09, 0.03, 0.08]))
            element.click()
        except Exception as inst:
            d = inst
            print(frameinfo.filename, frameinfo.lineno)
            print(d)
            
    def bestbuy_act_like_human(self, element:webdriver.Chrome.find_element=''):
        print('Acting like Human!')
        action = self.action
        if not element:
            startElement = self.driver.find_element_by_tag_name('body')
        # First, go to your start point or Element:
        action.move_to_element(startElement)
        action.perform()

        for mouse_x, mouse_y in zip(x_i, y_i):
            action.move_by_offset(mouse_x, mouse_y)
            action.perform()
    
    def bestbuy(self, item, thread_no=0):
        try:
            print('working!')
            driver = self.driver
            driver.get("https://www.bestbuy.com/identity/global/signin")
            self.bestbuy_select_country()
            if not item.skip:
                try:
                    is_already_signed_in = False
                    try:
                        emailInput = driver.find_element_by_xpath('//*[@id="fld-e"]')
                        passwordInput = driver.find_element_by_xpath('//*[@id="fld-p1"]')
                        
                        typeKeys(emailInput, item.account.email)
                        typeKeys(passwordInput, item.account.password)
                        click_btn_str = '//button[contains(@class, "cia-form__controls__submit")][contains(text(), "Sign In")]'
                        print('Clicking signin button...')
                        self.bestbuy_click(driver.find_element_by_xpath(click_btn_str))
                        print('Signin button clicked...')
                    except Exception as inst:
                        print(frameinfo.filename, frameinfo.lineno)
                        d = inst
                        print(frameinfo.filename, frameinfo.lineno)
                        print(d)
                        is_already_signed_in = True

                    if not is_already_signed_in:
                        try:
                            driver.implicitly_wait(25)
                            is_alert = driver.find_element_by_class_name('cia-alert')
                            driver.implicitly_wait(15)
                            print('Till here...')
                            print('CLicking in Forget Password')
                            driver.find_element_by_xpath("//span[contains(@class, 'cia-signin__forgot')]//a").click()
                            print('Clicking in Email Submit')
                            driver.find_element_by_xpath("//button[contains(@class, 'cia-form__controls__submit')]").click()
                        except Exception as inst:
                            d = inst
                            print(frameinfo.filename, frameinfo.lineno)
                            print(d)
                            
                    try:
                        print('Clicking in Email Verification')
                        driver.find_element_by_xpath("//label[contains(@for, 'email-radio')]//i[contains(@class, 'c-radio-custom-input')]").click()
                        driver.find_element_by_xpath("//div[contains(@class, 'cia-form__controls')]//button[contains(@class, 'cia-form__controls__submit')]").click()
                        
                        print('Entering Verification Code')
                        verification_code = driver.find_element_by_xpath("//div[contains(@class, 'tb-input-wrapper-full-width')]//input[contains(@class, 'tb-input')]")
                        wait(12)
                        print('Typing Verification Code')

                        continue_verification = True
                        while continue_verification:
                            try:
                                typeKeys(verification_code, get_verification_code(item, FindWith.BESTBUY))
                                continue_verification = False
                            except:
                                driver.find_element_by_xpath("//div[contains(@class, 'cia-prompt-actions__actions')]//button[contains(@data-track, 'Verification Code - Resend')]").click()
                                wait(5)

                        print('Clicking SUBMIT verification code')
                        driver.find_element_by_xpath("//div[contains(@class, 'cia-form__controls')]//button[contains(@class, 'cia-form__controls__submit')]").click()
                        
                        print('Adding New Password and Confirm New Password')
                        new_password = driver.find_element_by_xpath("//div[contains(@class, 'tb-input-wrapper-full-width')]//input[contains(@id, 'fld-p1')]")
                        typeKeys(new_password, item.account.password)
                        confirm_new_password = driver.find_element_by_xpath("//div[contains(@class, 'tb-input-wrapper-full-width')]//input[contains(@id, 'reenterPassword')]")
                        typeKeys(confirm_new_password, item.account.password)
                        
                        print('Clicking Save & Continue')
                        driver.find_element_by_xpath("//div[contains(@class, 'cia-form__controls')]//button[contains(@class, 'cia-form__controls__submit')]").click()
                    
                    except Exception as inst:
                        d = inst
                        print(frameinfo.filename, frameinfo.lineno)

                        print(d)
                        from.main import quit_bot
                        quit_bot(thread_no)
                    self.bestbuy_select_country()
                    print('Best buy select country!')
                    
                except Exception as inst:
                    d = inst
                    print(frameinfo.filename, frameinfo.lineno)
                    print(d)
                    
        
            refresh_delay = Settings.objects.first().refresh_delay
            while True:
                driver.get(item.link)
                self.bestbuy_select_country()
                price = driver.find_element_by_xpath("//*[contains(@class, 'priceView-customer-price')]/span")
                price = get_price(price)
                
                # get price
                if item.min_price < price < item.max_price+1:
                    # checking cart before clicking in add to cart
                    driver.execute_script('window.open("https://www.bestbuy.com/cart/", "_blank");')
                    driver.switch_to.window(driver.window_handles[1])
                    cards = driver.find_elements_by_xpath("//section[contains(@class, 'card')]")
                    del cards[-1]
                    quanity_of_item_in_card = 0
                    shouldAddToCart = True
                    try:
                        for card in cards:
                            card_item = card.find_element_by_xpath("//a[contains(@class, 'fluid-item__image')]")
                            if card_item.get_attribute("href").split('/site/')[1].split('?')[0] in item.link:
                                remove_btn = card.find_element_by_xpath("//a[contains(@class, 'cart-item__remove')]")
                                self.bestbuy_click(remove_btn)
                                wait(3)
                            else:
                                quanity_of_item_in_card += 1
                                item.quantity == item.quantity - 1
                                print(f'\nQuanity of item in model (In Loop):  {item.quantity}\n')
                                print(f'\nQuanity of item in card (In Loop):  {quanity_of_item_in_card}\n')
                                if quanity_of_item_in_card > item.quantity:
                                    remove_btn = card.find_element_by_xpath("//a[contains(@class, 'cart-item__remove')]")
                                    self.bestbuy_click(remove_btn)
                                    wait(3)

                        print(f'\nQuanity of item in model:  {item.quantity}\nQuanity of item in card:  {quanity_of_item_in_card}\n')

                        shouldAddToCart = not quanity_of_item_in_card >= item.quantity

                        driver.close()
                        
                        print(f'\nShould Add To Cart:  {shouldAddToCart}\n')
                        
                    except Exception as inst:
                        d = inst
                        print(frameinfo.filename, frameinfo.lineno)

                        print(d)
                        
                    wait(2)
                    
                    driver.switch_to.window(driver.window_handles[0])
                    
                    if shouldAddToCart:
                        print('Adding to cart')
                        self.bestbuy_act_like_human()
                        self.bestbuy_click(driver.find_element_by_class_name('add-to-cart-button'))
                        print('Clicking on `Go to cart`')

                        self.bestbuy_click(driver.find_element_by_xpath("//*[contains(@class, 'go-to-cart-button')]/a"))
                    else:
                        driver.get("https://www.bestbuy.com/cart/")

                    # select quantity
                    try:
                        if shouldAddToCart:
                            driver.find_element_by_xpath(f"//*[contains(@class, 'fluid-item__quantity')]/option[{item.quantity}]").click()
                    except Exception as inst:
                        d = inst
                        print(frameinfo.filename, frameinfo.lineno)

                        print("Quantity in dropdown not selected.")
                        print(d)
                    
                    # finally buy the product : checkout
                    if not item.is_test:
                        wait(3)
                        driver.find_element_by_xpath('//*[@id="cartApp"]//*[contains(@class, "checkout-buttons__checkout")]').click()
                        try:
                            passwordInput = driver.find_element_by_xpath('//*[@id="fld-p1"]')
                            typeKeys(passwordInput, item.account.password)
                            driver.find_element_by_xpath("//button[contains(@class, 'cia-form__controls__submit')]").click()
                        except Exception as inst:
                            d = inst
                            print(frameinfo.filename, frameinfo.lineno)
                            print(d)
                            
                        try:
                            continueToPayment = driver.find_element_by_xpath("//div[contains(@class, 'streamlined__test-styles')]//span[contains(text(), 'Continue to Payment Information')]")
                            continueToPayment.click()
                        except Exception as inst:
                            d = inst
                            print(frameinfo.filename, frameinfo.lineno)
                            print(d)
                            

                        try:
                            security_code = driver.find_element_by_xpath("//input[contains(@class, 'credit-card-form__cvv--warn')]")
                            typeKeys(security_code, item.security_code)
                        except Exception as inst:
                            d = inst
                            print(frameinfo.filename, frameinfo.lineno)
                            print(d)

                        try:
                            place_order = driver.find_element_by_xpath("//div[contains(@class, 'payment__order-summary')]//button[contains(@class, 'btn')]//span[contains(text(),'Place Your Order')]")
                            place_order.click()
                            item.bought = True
                            item.save()
                        except Exception as inst:
                            d = inst
                            print(frameinfo.filename, frameinfo.lineno)
                            print(d)
                            
                        wait(700)
                    break
                wait(refresh_delay)
            # QUIT THE BOT
            from.main import quit_bot
            quit_bot(thread_no)
                
        except:
            from.main import quit_bot
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