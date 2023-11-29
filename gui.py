import os
import random
import time

import colorama
from colorama import *
from colorama import Back, Fore, Style
from pynput.keyboard import Controller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import Screen
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.slider import Slider

def clear():
    os.system('cls||clear')

def main(username, password, falseDelay, mistakes, units):

    
    delay = "".join(x for x in falseDelay if x not in "Type-Speed: ")

    colorama.init(autoreset=True)


    try:#----------------------------------------------------------------------------------------------------------------------------------------------------------------

        browser = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
        browser.set_window_size(1000,500)
        browser.get('https://at4.typewriter.at/index.php?r=typewriter/runLevel')

    except Exception as e:

        print(Back.RED + Fore.BLUE + "[Error]Selenium: " + str(e))
        time.sleep(10)
        quit()
        
    clear()

    print(Fore.CYAN + "[" + Fore.BLUE + "Progress" + Fore.CYAN + "]" + Fore.RESET + "Loaded 5 Settings: "   + "\n" + 
        "Username: " + username                 +     
        "Password: " + password                 + 
        "Delay: " + str(delay)       + "\n" +   
        "Units: " + str(units)                  + 
        "Mistakes: " + str(mistakes) + "\n")

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
        
       #random.randint(int(mistakesMin), int(mistakesMax))

        print("Fehler: " + str(mistakes))
        counter = 0

        while True:  
            try:#----------------------------------------------------------------------------------------------------------------------------------------------------------------
                element = WebDriverWait(browser, 5).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/div[5]/div[2]/div[3]/div[2]/div[2]/span[1]')))
                character = element.text

                time.sleep(delay)

                #float(random.uniform(float(minDelay), float(maxDelay)))


                keyboard = Controller() 
                keyboard.press(character)
                keyboard.release(character)


                bigChars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ;,.-_:!?()=/ "
                
                if counter == mistakes:
                    continue
                elif character in bigChars:
                    #print("Replaced Character " + character)
                    mistake = Controller() 
                    mistake.press("a")
                    mistake.release("a")
                    counter += 1

                    chars = browser.find_element(By.XPATH, '/html/body/div[5]/div[2]/div[3]/div[1]/div[1]/div[2]/div[1]/div[1]/span').text

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


class gui(MDApp):
    def build(self):

        screen = Screen()

        title = MDLabel(text="Typefucker", 
                pos_hint={'center_x':0.8, 'center_y':0.95}, 
                theme_text_color="Custom",
                text_color=(0.5, 0, 0.5, 1),
                font_style='H2')

        inputUsername = TextInput(font_size=20,
                        size_hint_y = None,
                        height=40,
                        pos_hint={'center_x':0.65,
                        'center_y':0.8}, 
                        multiline=False)
        
        labelUsername = MDLabel(text="Username",
                        text_color=(0.5, 0, 0.5, 1),
                        theme_text_color="Custom",
                        pos_hint={'center_x':0.53,
                        'center_y':0.8})

        inputPassword = TextInput(font_size=20,
                        size_hint_y = None,
                        height=40,
                        pos_hint={'center_x':0.65,
                        'center_y':0.7}, 
                        multiline=False)

        labelPassword = MDLabel(text="Password",
                        text_color=(0.5, 0, 0.5, 1),
                        theme_text_color="Custom",
                        pos_hint={'center_x':0.53,
                        'center_y':0.7})

        Typespeed = Slider(min = 0, max = 100000)

       

        TypespeedLabel = MDLabel(text="Type-Speed: ",
                        text_color=(0.5, 0, 0.5, 1),
                        theme_text_color="Custom",
                        pos_hint={'center_x':0.53,
                        'center_y':0.6})

        def OnSliderValueChange(instance, value):
                TypespeedLabel.text = "Type-Speed: " + str(value)

        Typespeed.bind(value=OnSliderValueChange)

        def start(self):
                    username = str(inputUsername.text)
                    password = str(inputPassword.text)
                    print(username + "\n" + password)
                    main(username, password, TypespeedLabel.text, 10, 10)
                    

        buttonStart = Button(text="Start", background_color=(0.5, 0, 0.5, 1), size=(800, 50), size_hint=(None, None))
        buttonStart.bind(on_press=start)


        

        screen.add_widget(title)
        screen.add_widget(inputPassword)
        screen.add_widget(labelPassword)
        screen.add_widget(inputUsername)
        screen.add_widget(labelUsername)
        screen.add_widget(buttonStart)
        screen.add_widget(Typespeed)
        screen.add_widget(TypespeedLabel)
        return screen

Typefucker = gui()
Typefucker.run()