import os
import random
import time

import colorama
from colorama import *
from colorama import Back, Fore, Style
from discord_webhook import DiscordEmbed, DiscordWebhook
from pynput.keyboard import Controller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def clear():
    os.system('cls||clear')

colorama.init(autoreset=True)


clear()

username = ""
password = ""
units = 0 
minDelay = 0
maxDelay = 0

try:#----------------------------------------------------------------------------------------------------------------------------------------------------------------

    fileOpen = open('settings.txt')

    file = fileOpen.readlines()

    username = file[0]
    password = file[1]
    minDelay = 600/int(file[2])
    maxDelay = 600/int(file[3])
    units = file[4]

    fileOpen.close()

except Exception as e:

    print(Back.RED + Fore.BLUE + "[Error]File: " + str(e))
    time.sleep(10)
    quit()


try:#----------------------------------------------------------------------------------------------------------------------------------------------------------------

    options = Options()
    options.binary_location = 'C:\\Program Files\\Mozilla Firefox\\firefox.exe'
    browser = webdriver.Firefox(options=options)
    browser.set_window_size(1000,500)
    browser.get('https://at4.typewriter.at/index.php?r=typewriter/runLevel')

except Exception as e:

    print(Back.RED + Fore.BLUE + "[Error]Selenium: " + str(e))
    time.sleep(10)
    quit()
    
clear()

print(Fore.CYAN + "[" + Fore.BLUE + "Progress" + Fore.CYAN + "]" + Fore.RESET + "Loaded 5 Settings: "   + "\n" + 
      "Username: " + username           +     
      "Password: " + password           + 
      "Minimum Delay: " + str(minDelay) + "\n" +   
      "Maximum Delay: " + str(maxDelay) + "\n" +   
      "Units: " + str(units)            + "\n")

print(Fore.CYAN + "[" + Fore.BLUE + "Progress" + Fore.CYAN + "]" + Fore.RESET + "Getting user data. . .")
print(Fore.CYAN + "[" + Fore.BLUE + "Progress" + Fore.CYAN + "]" + Fore.RESET + "Visiting website. . .")

try:#----------------------------------------------------------------------------------------------------------------------------------------------------------------

    element = WebDriverWait(browser, 10).until(
    EC.visibility_of_element_located((By.XPATH, '//*[@id="LoginForm_username"]')))
    element.send_keys(username)
    print(Fore.CYAN + "[" + Fore.BLUE + "Progress" + Fore.CYAN + "]" + Fore.RESET + "Sending username. . .")

except Exception as e:

    print(Back.RED + Fore.BLUE + "[Error]Sending username failed: " + str(e))
    time.sleep(10)
    quit()

try:#----------------------------------------------------------------------------------------------------------------------------------------------------------------

    browser.find_element(By.XPATH, '//*[@id="LoginForm_pw"]').send_keys(password)
    print(Fore.CYAN + "[" + Fore.BLUE + "Progress" + Fore.CYAN + "]" + Fore.RESET + "Sending password. . .")

except Exception as e:

    print(Back.RED + Fore.BLUE + "[Error]Sending password failed: " + str(e))
    time.sleep(10)
    quit()
    
try:#----------------------------------------------------------------------------------------------------------------------------------------------------------------

    browser.find_element(By.XPATH, '/html/body/div[5]/div[2]/div[1]/form/div[3]/input').click()
    print(Fore.CYAN + "[" + Fore.BLUE + "Progress" + Fore.CYAN + "]" + Fore.RESET + "Clicking login button. . .")

except Exception as e:

    print(Back.RED + Fore.BLUE + "[Error]Clicking login button failed: " + str(e))
    time.sleep(10)
    quit()

try:#----------------------------------------------------------------------------------------------------------------------------------------------------------------

    element = WebDriverWait(browser, 5).until(
    EC.visibility_of_element_located((By.XPATH, '/html/body/div[5]/div[3]/div[2]/div[1]/a/div[3]')))
    element.click()
    print(Fore.CYAN + "[" + Fore.BLUE + "Progress" + Fore.CYAN + "]" + Fore.RESET + "Clicking unit button. . .")

except Exception as e:

    print(Back.RED + Fore.BLUE + "[Error]Clicking unit button failed: " + str(e))
    time.sleep(10)
    quit()
    
try:#----------------------------------------------------------------------------------------------------------------------------------------------------------------    
    element = WebDriverWait(browser, 5).until(
    EC.visibility_of_element_located((By.XPATH, '/html/body/div[8]/div[3]/div/button')))
    element.click()
    print(Fore.CYAN + "[" + Fore.BLUE + "Progress" + Fore.CYAN + "]" + Fore.RESET + "Clicking start button. . .")

except Exception as e:

    print(Back.RED + Fore.BLUE + "[Error]Clicking unit button failed: " + str(e))
    time.sleep(10)
    quit()


for x in range(int(units)):
    print(Fore.CYAN + "[" + Fore.BLUE + "Progress" + Fore.CYAN + "]" + Fore.RESET + "Writing unit nr. " + str(x+1) + ". . .")

    while True:  
        try:#----------------------------------------------------------------------------------------------------------------------------------------------------------------
            element = WebDriverWait(browser, 5).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/div[5]/div[2]/div[3]/div[2]/div[2]/span[1]')))
            character = element.text

            time.sleep(float(random.uniform(float(minDelay), float(maxDelay))))

            keyboard = Controller() 
            keyboard.press(character)
            keyboard.release(character)

            chars = browser.find_element(By.XPATH, '//*[@id="amountRemaining"]').text

        except:
            print("EXCEPT!!!")
            print("Characters: " + chars)

            if chars == "0":
                print(Fore.CYAN + "[" + Fore.BLUE + "Progress" + Fore.CYAN + "]" + Fore.RESET + "Restarting Unit. . .")
                break
            else: 
                continue

    try:#----------------------------------------------------------------------------------------------------------------------------------------------------------------    
  
        element = WebDriverWait(browser, 5).until(
        EC.visibility_of_element_located((By.XPATH, '/html/body/div[5]/div[1]/div[2]/ul/li[1]/a/div/img')))
        element.click()
        print(Fore.CYAN + "[" + Fore.BLUE + "Progress" + Fore.CYAN + "]" + Fore.RESET + "Clicking house button. . .")

    except Exception as e:

        print(Back.RED + Fore.BLUE + "[Error]Clicking house button failed: " + str(e))
        time.sleep(10)
        quit()

    try:#----------------------------------------------------------------------------------------------------------------------------------------------------------------  
        element = WebDriverWait(browser, 5).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="contentBody"]/div[2]/div[1]/a')))
        element.click()
        print(Fore.CYAN + "[" + Fore.BLUE + "Progress" + Fore.CYAN + "]" + Fore.RESET + "Clicking unit button. . .")

    except Exception as e:

        print(Back.RED + Fore.BLUE + "[Error]Clicking house button failed: " + str(e))
        time.sleep(10)
        quit()

