import threading
import time
import random
import time
import json
from selenium.webdriver.firefox.service import Service


from pynput.keyboard import Controller
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import drivehelper
from constants import *
import platform

class WorkerThread(threading.Thread):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.should_stop = threading.Event()


    def saveInfo(self):#-----------------------------------------------------------------------------------------
        data = {
            'username': self.username,
            'password': self.password,
            'units': self.units,
            'minDelay': self.minDelay,
            'maxDelay': self.maxDelay,
            'minMistakes': self.minMistakes,
            'maxMistakes': self.maxMistakes
        }

        with open('user_data.json', 'w') as json_file:
            json.dump(data, json_file)
            
    def loadInfo(self):#-----------------------------------------------------------------------------------------
            with open('user_data.json', 'r') as json_file:
                data = json.load(json_file)
                self.username = data['username']
                self.password = data['password']
                self.units = data['units']
                self.minDelay = data['minDelay']
                self.maxDelay = data['maxDelay']
                self.minMistakes = data['minMistakes']
                self.maxMistakes = data['maxMistakes']
                self.main_window.betterPrint("User data loaded successfully. . .")
    
    def run(self):
        try:
            self.loadInfo()
        except Exception as e:
            self.main_window.betterPrint("No existing user data found. . .")
            self.should_stop.set()
            return
        
        self.username: str =  self.username if self.username else ""
        self.password: str =  self.password if self.password else ""
        self.units: int =  self.units if self.units else 0
        self.minDelay: int = self.minDelay if self.minDelay else 0
        self.maxDelay: int = self.maxDelay if self.maxDelay else 0
        self.minMistakes: int = self.minMistakes if self.minMistakes else 0
        self.maxMistakes: int = self.maxMistakes if self.maxMistakes else 0
        
        self.saveInfo()
        
        gecko_driver_path = "geckodriver.exe"  
        firefox_default_path_64 = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"
        firefox_default_path_32 = "C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe"

        system_architecture = platform.architecture()[0]
        if system_architecture == '64bit':
            firefox_binary_path = firefox_default_path_64
        else:
            firefox_binary_path = firefox_default_path_32

        firefox_options = Options()
        firefox_options.binary_location = firefox_binary_path  
        
        try:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
            service = Service(gecko_driver_path)
            
            browser = webdriver.Firefox(service=service, options=firefox_options)
            driver = drivehelper.WebDrive(browser=browser, delay=5, main_window=self.main_window)                                                                                       
            
        except Exception as e:
            self.main_window.betterPrint("Selenium-Driver-Error: " + str(e))
            time.sleep(2)
        
        driver.connectUrl(url='https://at4.typewriter.at/index.php?r=typewriter/runLevel')
        
        self.main_window.betterPrint("Getting user data. . .")
        self.main_window.betterPrint("Visiting website. . .")                                                                                                                                                              
                                                                                                                                                                                                    
        driver.clickElement(COOKIES)
        
        self.main_window.betterPrint("Skipping Cookies. . .")
        
        driver.sendKeysToElement(USERNAME, self.username)
        
        self.main_window.betterPrint("Sending username. . .")
        
        driver.sendKeysToElement(PASSWORD, self.password)
        
        self.main_window.betterPrint("Sending password. . .")
        
        driver.clickElement(LOGIN)
        
        self.main_window.betterPrint("Clicking login button. . .")
        
        def transormToSeconds(lettersIn10Minutes):
                        return 600/int(lettersIn10Minutes)

        self.minDelay = transormToSeconds(self.minDelay)
        self.maxDelay = transormToSeconds(self.maxDelay)
        
        for x in range(int(self.units)):        
            mistakes = random.randint(int(self.minMistakes), int(self.maxMistakes))
           
            time.sleep(2)  
            driver.clickElement(UNIT)  
        
            self.main_window.betterPrint("Clicking letter. . .")
                                 
            keyboard = Controller() 
            keyboard.press("a")
            keyboard.release("a")
                
            self.main_window.betterPrint("Clicking start button. . .")
                
            self.main_window.betterPrint(f"Writing unit nr. {str(x+1)} . . .")

            random_numbers = []
                
            while True:    
                try:
                        
                    delay = random.uniform(float(self.minDelay), float(self.maxDelay))
                    
                    
                    time.sleep(delay)
                    

                    element = WebDriverWait(browser, 5).until(
                    EC.visibility_of_element_located((By.XPATH, TEXT)))
                    character = element.text
                    

                    keyboard = Controller() 
                    keyboard.press(character)
                    keyboard.release(character)

                    try:
                        self.chars = int(browser.find_element(By.XPATH, LETTER_NUM).text)
                    except:
                        continue
                    
                    if mistakes != 0:
                        try:
                            if not random_numbers:
                                random_numbers = random.sample(range(0, self.chars + 1), mistakes)
                                self.main_window.betterPrint(f"Random mistake positions: {str(random_numbers)}")
                        except Exception as e:
                            self.main_window.betterPrint("Exception" + str(e))



                        if self.chars in random_numbers:
                            self.main_window.betterPrint("Made a mistake at: " + str(self.chars))
                            if character == "a":
                                keyboard.press("q")
                                keyboard.release("q")
                            else:
                                keyboard.press("a")
                                keyboard.release("a")

                except Exception as e:
                    if int(self.units)-1 == x:
                        self.main_window.betterPrint("Stopping Program")
                        driver.quit()
                        self.should_stop.set()
                        return
                    if self.chars == 0:
                        self.main_window.betterPrint("Restarting unit")
                        break
                    
            
            driver.clickElementJavascript(HOUSE)
            
            self.main_window.betterPrint("Clicking house button. . .")
            
            driver.clickElement(UNIT)
            
            self.main_window.betterPrint("Clicking unit button. . .")

