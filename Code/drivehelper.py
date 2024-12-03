from selenium import webdriver 
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import os
import random
from selenium.webdriver.common.action_chains import ActionChains


class WebDrive:
    def __init__(self, browser, delay, main_window):
        self.browser = browser
        self.main_window = main_window
        self.delay = delay
#------------------------------------------------------------------------------------------------------------------------------------

    def quit(self):
        self.browser.quit()

#------------------------------------------------------------------------------------------------------------------------------------

    def connectUrl(self, url):
        try:
            self.browser.get(url)
        except Exception as e:
            self.main_window.betterPrint("[ERROR]" + f" Url is invalid:   {str(e)}")

#------------------------------------------------------------------------------------------------------------------------------------

    def clickElement(self, xpath):
        try:
            element = WebDriverWait(self.browser, self.delay).until(
            EC.visibility_of_element_located((By.XPATH, xpath)))
        except Exception as e:
            self.main_window.betterPrint("[ERROR]" + f" Can't find element:   {str(e)}")

        try:
            element.click()
        except Exception as e:
            self.main_window.betterPrint("[ERROR]" + f" Can't click element:   {str(e)}")

#------------------------------------------------------------------------------------------------------------------------------------

    def clickElementJavascript(self, xpath):
        try:
            element = WebDriverWait(self.browser, self.delay).until(
            EC.visibility_of_element_located((By.XPATH, xpath)))
        except Exception as e:
            self.main_window.betterPrint("[ERROR]" + f" Can't find element:   {str(e)}")

        try:
            self.browser.execute_script("arguments[0].click();", element)
        except Exception as e:
            self.main_window.betterPrint("[ERROR]" + f" Can't click element:   {str(e)}")

#------------------------------------------------------------------------------------------------------------------------------------

    def clickElementActionChain(self, xpath):
        try:
            element = WebDriverWait(self.browser, self.delay).until(
            EC.visibility_of_element_located((By.XPATH, xpath)))
        except Exception as e:
            self.main_window.betterPrint("[ERROR]" + f" Can't find element:   {str(e)}")

        try:
            actions = ActionChains(self.browser)
            actions.move_to_element(element).click().perform()
        except Exception as e:
            self.main_window.betterPrint("[ERROR]" + f" Can't click element:   {str(e)}")

#------------------------------------------------------------------------------------------------------------------------------------

    def sendKeysToElement(self, xpath, keys):
        try:
            element = WebDriverWait(self.browser, self.delay).until(
            EC.visibility_of_element_located((By.XPATH, xpath)))
        except Exception as e:
            self.main_window.betterPrint("[ERROR]" + f" Can't find element:   {str(e)}")
        
        try:
            element.send_keys(keys)
        except Exception as e:
            self.main_window.betterPrint("[ERROR]" + f" Can't send Keys:   {str(e)}")

#------------------------------------------------------------------------------------------------------------------------------------

    def clearInput(self, xpath):
        try:
            element = WebDriverWait(self.browser, self.delay).until(
            EC.visibility_of_element_located((By.XPATH, xpath)))
        except Exception as e:
            self.main_window.betterPrint("[ERROR]" + f" Can't find element:   {str(e)}")
        
        try:
            element.clear()
        except Exception as e:
            self.main_window.betterPrint("[ERROR]" + f" Can't send Keys:   {str(e)}")

#------------------------------------------------------------------------------------------------------------------------------------

    def clickCoordinates(self, x, y):
        actions = ActionChains(self.browser)
        try:
            actions.move_by_offset(x, y).click().perform()
        except Exception as e:
            self.main_window.betterPrint("[ERROR]" + f" Can't click Coordinates:   {str(e)}")

#------------------------------------------------------------------------------------------------------------------------------------
