import os
import random
import time
import json

import colorama
from colorama import *
from colorama import Back, Fore, Style
from pynput.keyboard import Controller
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium import webdriver 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import drivehelper




class Typewriter:
    def __init__(self, **kwargs):
        self.username = ""
        self.password = ""
        self.units = 0 
        self.minDelay = 0
        self.maxDelay = 0
        
        self.menu()

    def menu(self):#-----------------------------------------------------------------------------------------
        
        print("Welcome to Typefucker by susmi ")
        saveData = input("Do you want to start with data from last session? no/yes \n")

        if saveData == "yes":
            self.loadInfo()
            self.start()
        elif saveData == "no":
            self.registerInfo()
            self.saveInfo()
            self.start()
        elif saveData == "susmi":
            self.username = "Susmi"
            self.password = "JosefistCool15?"
            self.units = 1
            self.clear()
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
            'maxDelay': self.maxDelay
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
                print("User data loaded successfully.")
        except FileNotFoundError:
            print("No existing user data found.")
    
    def registerInfo(self):#-----------------------------------------------------------------------------------------
        self.username = input("Username:    ")
        if self.username == "":
            print("Please enter a username. . .")
            time.sleep(2)
            self.clear()
            self.registerInfo()
        
        self.password = input("Password:    ")
        if self.username == "":
            print("Please enter a password. . .")
            time.sleep(2)
            self.clear()
            self.registerInfo()
            
        self.units = input("How many Units:    ")
        if self.username == "":
            print("Please enter a units number. . .")
            time.sleep(2)
            self.clear()
            self.registerInfo()
            
        self.maxDelay = input("Maximum Delay:    ")
        if self.username == "":
            print("Please enter a maximum Delay number. . .")
            time.sleep(2)
            self.clear()
            self.registerInfo()
            
        self.minDelay = input("Minimum Delay:    ")
        if self.username == "":
            print("Please enter a minimum Delay number. . .")
            time.sleep(2)
            self.clear()
            self.registerInfo()
        
    def clear(self):#-----------------------------------------------------------------------------------------
        os.system('cls||clear')
        
    def start(self):#-----------------------------------------------------------------------------------------
        options = Options()
        options.binary_location = 'C:\\Program Files\\Mozilla Firefox\\firefox.exe'
        browser = webdriver.Firefox(options=options)


        driver = drivehelper.WebDrive(browser=browser, delay=5)
        driver.connectUrl(url='https://at4.typewriter.at/index.php?r=typewriter/runLevel')
        
        print(Fore.CYAN + "[" + Fore.BLUE + "Progress" + Fore.CYAN + "]" + Fore.RESET + "Getting user data. . .")
        print(Fore.CYAN + "[" + Fore.BLUE + "Progress" + Fore.CYAN + "]" + Fore.RESET + "Visiting website. . .")

        driver.clickElement("/html/body/div[7]/div[2]/div[1]/div[2]/div[2]/button[1]/p")
        
        print(Fore.CYAN + "[" + Fore.BLUE + "Progress" + Fore.CYAN + "]" + Fore.RESET + "Skipping Cookies. . .")
        
        driver.sendKeysToElement('//*[@id="LoginForm_username"]', self.username)
        
        print(Fore.CYAN + "[" + Fore.BLUE + "Progress" + Fore.CYAN + "]" + Fore.RESET + "Sending username. . .")
        
        driver.sendKeysToElement('//*[@id="LoginForm_pw"]', self.password)
        
        print(Fore.CYAN + "[" + Fore.BLUE + "Progress" + Fore.CYAN + "]" + Fore.RESET + "Sending password. . .")
        
        driver.clickElement('/html/body/div[5]/div[2]/div[1]/form/div[3]/input')
        
        print(Fore.CYAN + "[" + Fore.BLUE + "Progress" + Fore.CYAN + "]" + Fore.RESET + "Clicking login button. . .")
        
        for x in range(int(self.units)):
            
            driver.clickElement('/html/body/div[5]/div[3]/div[2]/div[1]/a/div[3]')
        
            print(Fore.CYAN + "[" + Fore.BLUE + "Progress" + Fore.CYAN + "]" + Fore.RESET + "Clicking unit button. . .")
                
            driver.clickElement('/html/body/div[9]/div[3]/div/button')
                
            print(Fore.CYAN + "[" + Fore.BLUE + "Progress" + Fore.CYAN + "]" + Fore.RESET + "Clicking start button. . .")
                
            print(Fore.CYAN + "[" + Fore.BLUE + "Progress" + Fore.CYAN + "]" + Fore.RESET + "Writing unit nr. " + str(x+1) + ". . .")
                
            while True:    
                try:
                    time.sleep(float(random.uniform(float(self.minDelay), float(self.maxDelay))))

                    element = WebDriverWait(browser, 5).until(
                    EC.visibility_of_element_located((By.XPATH, '/html/body/div[5]/div[2]/div[3]/div[2]/div[2]/span[1]')))
                    character = element.text
                    
                    keyboard = Controller() 
                    keyboard.press(character)
                    keyboard.release(character)
            
                    chars = browser.find_element(By.XPATH, '/html/body/div[5]/div[2]/div[3]/div[1]/div[1]/div[2]/div[1]/div[1]/span').text

                except:
                    
                    print("EXCEPT!!!")
                    print("Characters: " + chars)

                    if chars == "0":
                        print(Fore.CYAN + "[" + Fore.BLUE + "Progress" + Fore.CYAN + "]" + Fore.RESET + "Restarting Unit. . .")
                        break
                    else: 
                        continue
            
            driver.clickElement('/html/body/div[5]/div[1]/div[2]/ul/li[1]/a/div/img')
            
            print(Fore.CYAN + "[" + Fore.BLUE + "Progress" + Fore.CYAN + "]" + Fore.RESET + "Clicking house button. . .")
            
            driver.clickElement('//*[@id="contentBody"]/div[2]/div[1]/a')
            
            print(Fore.CYAN + "[" + Fore.BLUE + "Progress" + Fore.CYAN + "]" + Fore.RESET + "Clicking unit button. . .")
                            
                    

instance = Typewriter()



    
