import os
import random
import time
import json

from colorama import *
from colorama import Back, Fore, Style
from pynput.keyboard import Controller
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import drivehelper
from constants import *
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import platform



class Typewriter:
    def __init__(self, **kwargs):
        self.username: str =  ""
        self.password: str =  ""
        self.units: int = 0
        self.minDelay: int = 0
        self.maxDelay: int = 0
        self.counter: int = 0
        self.minMistakes: int = 0
        self.maxMistakes: int = 0

        
        self.menu()

    def menu(self):#-----------------------------------------------------------------------------------------
        
        self.clear()
        
        print("""
 _______                __            _              
|__   __|              / _|          | |             
   | |_   _ _ __   ___| |_ _   _  ___| | _____ _ __  
   | | | | | '_ \ / _ \  _| | | |/ __| |/ / _ \ '__| 
   | | |_| | |_) |  __/ | | |_| | (__|   <  __/ |         by susmi
   |_|\__, | .__/ \___|_|  \__,_|\___|_|\_\___|_|    
       __/ | |                                       
      |___/|_|                                       
""")
        

        saveData = input("Do you want to start with data from last session? no/yes \n")

        if saveData == "yes":
            self.loadInfo()
            self.start()
        elif saveData == "no":
            self.registerInfo()
            self.saveInfo()
            self.start()
        else:
            print("Please pick no or yes. . .")
            time.sleep(2)
            self.clear()
            self.menu()
    
    
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
        try:
            with open('user_data.json', 'r') as json_file:
                data = json.load(json_file)
                self.username = data['username']
                self.password = data['password']
                self.units = data['units']
                self.minDelay = data['minDelay']
                self.maxDelay = data['maxDelay']
                self.minMistakes = data['minMistakes']
                self.maxMistakes = data['maxMistakes']
                print("User data loaded successfully.")
        except FileNotFoundError:
            print("No existing user data found.")
            self.menu()
            
            
    def betterPrint(self, message: str):#-----------------------------------------------------------------------------------------
        print(Fore.CYAN + "[" + Fore.BLUE + "Process" + Fore.CYAN + "]" + Fore.RESET + f"{message}. . .")
        
    
    def registerInfo(self):#-----------------------------------------------------------------------------------------
        def restart():
            time.sleep(2)
            self.clear()
            self.registerInfo()
                
        self.username = input("Username:    ")
        if self.username == "":
            print("Username can't be empty!")
            restart()
        
        self.password = input("Password:    ")
        if self.password == "":
            print("Password can't be empty!")
            restart()
            
        self.units = input("How many Units:    ")
        if not self.units.isdigit():
            print("Units can only be integer!")
            restart()
            
        self.maxDelay = input("Maximum Delay:    ")
        if self.maxDelay.isalpha():
            print("Maximum Delay can only be float or integer!")
            restart()
            
        self.minDelay = input("Minimum Delay:    ")
        if self.maxDelay.isalpha():
            print("Minimum Delay can only be float or integer!")
            restart()

        self.maxMistakes = input("Maximum Mistakes:    ")
        if self.maxMistakes.isalpha():
            print("Maximum Mistakes can only be float or integer!")
            restart()
            
        self.minMistakes = input("Minimum Mistakes:    ")
        if self.minMistakes.isalpha():
            print("Minimum Mistakes can only be float or integer!")
            restart()

    def clear(self):#-----------------------------------------------------------------------------------------
        os.system('cls||clear')
        


    def start(self):#-----------------------------------------------------------------------------------------
        
        
        gecko_driver_path = "geckodriver.exe"  
        firefox_default_path_64 = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"
        firefox_default_path_32 = "C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe"

        system_architecture = platform.architecture()[0]
        if system_architecture == '64bit':
            firefox_binary_path = firefox_default_path_64
        else:
            firefox_binary_path = firefox_default_path_32

        firefox_options = Options()
        firefox_options.binary = FirefoxBinary(firefox_binary_path)
        
        browser = webdriver.Firefox(executable_path=gecko_driver_path, options=firefox_options)

        driver = drivehelper.WebDrive(browser=browser,  delay=5)
        driver.connectUrl(url='https://at4.typewriter.at/index.php?r=typewriter/runLevel')
        
        self.betterPrint("Getting user data. . .")
        self.betterPrint("Visiting website. . .")

        driver.clickElement(COOKIES)
        
        self.betterPrint("Skipping Cookies. . .")
        
        driver.sendKeysToElement(USERNAME, self.username)
        
        self.betterPrint("Sending username. . .")
        
        driver.sendKeysToElement(PASSWORD, self.password)
        
        self.betterPrint("Sending password. . .")
        
        driver.clickElement(LOGIN)
        
        self.betterPrint("Clicking login button. . .")
        
        for x in range(int(self.units)):
            mistakes = random.randint(int(self.minMistakes), int(self.maxMistakes))
            print(mistakes)
              
            driver.clickElement(UNIT)
        
            self.betterPrint("Clicking unit button. . .")
                                 
            driver.clickElement(START)
                
            self.betterPrint("Clicking start button. . .")
                
            self.betterPrint(f"Writing unit nr. {str(x+1)} . . .")
                
            while True:    
                try:
                    time.sleep(float(random.uniform(float(self.minDelay), float(self.maxDelay))))

                    element = WebDriverWait(browser, 5).until(
                    EC.visibility_of_element_located((By.XPATH, LETTER)))
                    character = element.text
                    

                    keyboard = Controller() 
                    keyboard.press(character)
                    keyboard.release(character)

                    if mistakes != 0:
                        mistakes = mistakes-1
                        if character == "a":
                            keyboard.press("q")
                            keyboard.release("q")
                        else:
                            keyboard.press("a")
                            keyboard.release("a")
            
                    chars = browser.find_element(By.XPATH, LETTER_NUM).text

                except:
                    
                    print("EXCEPT!!!")
                    print("Characters: " + chars)

                    if chars == "0":
                        self.betterPrint("Restarting unit")
                        break
            
            driver.clickElement(HOUSE)
            
            self.betterPrint("Clicking house button. . .")
            
            driver.clickElement(UNIT)
            
            self.betterPrint("Clicking unit button. . .")
                            
                    

instance = Typewriter()



    
