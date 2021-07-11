from chromedriver_py import binary_path
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep as wait, time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from decouple import config
import numpy
from read_inbox import get_verification_code, FindWith

driver.get('https://www.walmart.com/blocked')
WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe.iframe-content#tab_Welcome")))
