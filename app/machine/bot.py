from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep as wait
from selenium.webdriver.common.by import By
from.additionals import *

from ..models import Settings

class Bots:
    def __init__(self, driver:webdriver.Chrome):
        self.driver = driver

    def bestbuy(self, item, thread_no=0):
        try:
            print('working!')
            driver = self.driver
            getElement = waitGetElm(driver)
            driver.get("https://www.bestbuy.com/identity/global/signin")

            if not item.skip:
                try:
                    emailInput = driver.find_element_by_xpath('//*[@id="fld-e"]')
                    passwordInput = driver.find_element_by_xpath('//*[@id="fld-p1"]')
                    typeKeys(emailInput, item.account.email)
                    typeKeys(passwordInput, item.account.password)
                    driver.find_element_by_xpath('/html/body/div[1]/div/section/main/div[2]/div[1]/div/div/div/div/form/div[3]/button').click()
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
                    # checking cart before clicking in add to cart
                    driver.execute_script('window.open("https://www.bestbuy.com/cart/", "_blank");')
                    driver.switch_to.window(driver.window_handles[1])
                    cards = driver.find_elements_by_xpath("//section[contains(@class, 'card')]")
                    del cards[-1]
                    quanity_of_item_in_card = 0
                    shouldAddToCart = True
                    for card in cards:
                        print(quanity_of_item_in_card)
                        card_item = card.find_element_by_xpath("//a[contains(@class, 'fluid-item__image')]")
                        print(f"PASSED {card_item}")
                        if item.link != card_item.get_attribute("href"):
                            print("PASSED2")
                            remove_btn = card.find_element_by_xpath("//a[contains(@class, 'cart-item__remove')]")
                            remove_btn.click()
                            wait(3)
                        else:
                            quanity_of_item_in_card += 1
                            item.quantity == item.quantity - 1
                            if quanity_of_item_in_card > item.quantity:
                                remove_btn = card.find_element_by_xpath("//a[contains(@class, 'cart-item__remove')]")
                                remove_btn.click()
                                wait(3)
                            shouldAddToCart = not quanity_of_item_in_card >= item.quantity
                            driver.close()
                            print(f'\nShould Add To Cart:  {shouldAddToCart}\n')
                    wait(2)
                    driver.switch_to.window(driver.window_handles[0])
                    # Click on "Add to cart"
                    if shouldAddToCart:
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
                    
                    # finally buy the product : checkout
                    if not item.is_test:
                        wait(3)
                        driver.find_element_by_xpath('//*[@id="cartApp"]//*[contains(@class, "checkout-buttons__checkout")]').click()
                        passwordInput = driver.find_element_by_xpath('//*[@id="fld-p1"]')
                        typeKeys(passwordInput, item.account.password)
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