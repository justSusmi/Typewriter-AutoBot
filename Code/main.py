import sys
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import threading
import time
import random
import time
import json
from selenium.webdriver.firefox.service import Service
from tkinter import PhotoImage

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
            print(e)
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
            driver = drivehelper.WebDrive(browser=browser, delay=5)  

            
        except Exception as e:
            print("Selenium-Driver-Error: " + str(e))
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
                            print("Exception" + str(e))



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

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Typefucker")
        self.geometry("400x600")
        
        try:
            icon = PhotoImage(file="typefucker_logo.png") 
            self.wm_iconphoto(True, icon)      
        except Exception as e:
            print(f"Error while loading image: {e}")
        
        self.worker_thread = WorkerThread(self)
        
        self.page1 = self.create_page1()
        self.page2 = self.create_page2()

        self.page1.pack(fill="both", expand=True)

    def create_page1(self):
        page1_frame = tk.Frame(self, bg="#424549")
        
        self.listbox = tk.Listbox(page1_frame, bg="#1e2124", fg="white", font=("Helvetica", 14))
        self.listbox.pack(pady=10, fill="both", expand=True)
        
        start_button = tk.Button(page1_frame, text="Start", command=self.start_task, bg="#7289da", fg="white", font=("Helvetica", 14), width=20, height=2)
        start_button.pack(pady=10)

        settings_button = tk.Button(page1_frame, text="Settings Page", command=self.switch_to_page2, bg="#7289da", fg="white", font=("Helvetica", 14), width=20, height=1)
        settings_button.pack(pady=10)
        
        return page1_frame

    def create_page2(self):
        page2_frame = tk.Frame(self, bg="#424549")
        
        self.username_input = tk.Entry(page2_frame, bg="#1e2124", fg="white", font=("Helvetica", 14))
        self.username_input.pack(pady=5)
        self.username_input.insert(0, "Username")
        
        self.password_input = tk.Entry(page2_frame, show="*", bg="#1e2124", fg="white", font=("Helvetica", 14))
        self.password_input.pack(pady=5)
        self.password_input.insert(0, "Password")
        
        self.units_input = tk.Entry(page2_frame, bg="#1e2124", fg="white", font=("Helvetica", 14))
        self.units_input.pack(pady=5)
        self.units_input.insert(0, "Units")
        
        self.max_delay_input = tk.Entry(page2_frame, bg="#1e2124", fg="white", font=("Helvetica", 14))
        self.max_delay_input.pack(pady=5)
        self.max_delay_input.insert(0, "Max Delay")
        
        self.min_delay_input = tk.Entry(page2_frame, bg="#1e2124", fg="white", font=("Helvetica", 14))
        self.min_delay_input.pack(pady=5)
        self.min_delay_input.insert(0, "Min Delay")
        
        self.max_mistakes_input = tk.Entry(page2_frame, bg="#1e2124", fg="white", font=("Helvetica", 14))
        self.max_mistakes_input.pack(pady=5)
        self.max_mistakes_input.insert(0, "Max Mistakes")
        
        self.min_mistakes_input = tk.Entry(page2_frame, bg="#1e2124", fg="white", font=("Helvetica", 14))
        self.min_mistakes_input.pack(pady=5)
        self.min_mistakes_input.insert(0, "Min Mistakes")
    
        submit_button = tk.Button(page2_frame, text="Save Info", command=self.validate_and_submit, bg="#7289da", fg="white", font=("Helvetica", 14), width=20, height=1)
        submit_button.pack(pady=5)
        
        clear_button = tk.Button(page2_frame, text="Clear", command=self.clear_fields, bg="#7289da", fg="white", font=("Helvetica", 14), width=20, height=1)
        clear_button.pack(pady=5)
        
        back_button = tk.Button(page2_frame, text="Back", command=self.switch_to_page1, bg="#7289da", fg="white", font=("Helvetica", 14), width=20, height=1)
        back_button.pack(pady=5)
        
        return page2_frame

    def start_task(self):
        if self.worker_thread and self.worker_thread.is_alive():
            self.betterPrint("Program is already running, Please Wait!")
            return

        self.worker_thread = WorkerThread(self)
        self.worker_thread.start()
        self.betterPrint("Started Program")

    def validate_and_submit(self):                    
        self.username = self.username_input.get().strip()
        self.password = self.password_input.get().strip()
        self.units = self.units_input.get().strip()
        self.max_delay = self.max_delay_input.get().strip()
        self.min_delay = self.min_delay_input.get().strip()
        self.max_mistakes = self.max_mistakes_input.get().strip()
        self.min_mistakes = self.min_mistakes_input.get().strip() 

        if not self.username:
            self.show_error("Username cannot be empty!")
            return

        if not self.password:
            self.show_error("Password cannot be empty!")
            return

        if not self.units.isdigit():
            self.show_error("Units must be an integer!")
            return

        if not self.max_delay.replace('.', '', 1).isdigit():
            self.show_error("Maximum Delay must be a number!")
            return

        if not self.min_delay.replace('.', '', 1).isdigit():
            self.show_error("Minimum Delay must be a number!")
            return

        if not self.max_mistakes.replace('.', '', 1).isdigit():
            self.show_error("Maximum Mistakes must be a number!")
            return

        if not self.min_mistakes.replace('.', '', 1).isdigit():
            self.show_error("Minimum Mistakes must be a number!")
            return

        messagebox.showinfo("Success", "All data is valid and submitted successfully!")
        self.worker_thread.username = self.username
        self.worker_thread.password = self.password
        self.worker_thread.units = self.units
        self.worker_thread.maxDelay = self.max_delay
        self.worker_thread.minDelay = self.min_delay
        self.worker_thread.maxMistakes = self.max_mistakes
        self.worker_thread.minMistakes = self.min_mistakes
        self.worker_thread.saveInfo()

    def show_error(self, message):
        messagebox.showerror("Error", message)
        
    def clear_fields(self):
        self.username_input.delete(0, 'end')
        self.password_input.delete(0, 'end')
        self.units_input.delete(0, 'end')
        self.max_delay_input.delete(0, 'end')
        self.min_delay_input.delete(0, 'end')
        self.max_mistakes_input.delete(0, 'end')
        self.min_mistakes_input.delete(0, 'end')

    def betterPrint(self, message: str):
        self.after(0, lambda: self.update_list_widget(message))

    def switch_to_page1(self):
        self.page2.pack_forget()
        self.page1.pack(fill="both", expand=True)

    def switch_to_page2(self):
        self.page1.pack_forget()
        self.page2.pack(fill="both", expand=True)

    def update_list_widget(self, message):
        self.listbox.insert(tk.END, message)
        self.listbox.yview(tk.END)

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()