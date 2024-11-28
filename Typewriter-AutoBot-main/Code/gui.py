import sys
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QFormLayout, QStackedWidget, QListWidget, QMainWindow)
import random
import time
import json
from PyQt5.QtGui import QIntValidator, QDoubleValidator

from colorama import *
from colorama import Fore
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


class WorkerThread(QThread):
    
    progress_signal = pyqtSignal(str)  
    
    def betterPrint(self, message: str):
        self.progress_signal.emit(message)  

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
                self.betterPrint("User data loaded successfully. . .")
    
    def run(self):
        try:
            self.loadInfo()
        except Exception as e:
            self.betterPrint("No existing user data found. . .")
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
        firefox_options.binary = FirefoxBinary(firefox_binary_path)
        
        try:
            browser = webdriver.Firefox(executable_path=gecko_driver_path, options=firefox_options)
            driver = drivehelper.WebDrive(browser=browser,  delay=5)
        except Exception as e:
            print("Selenium-Driver-Error: " + str(e))
            time.sleep(2)
        
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
           
            time.sleep(2)  
            driver.clickElement(UNIT)  
        
            self.betterPrint("Clicking letter. . .")
                                 
            keyboard = Controller() 
            keyboard.press("a")
            keyboard.release("a")
                
            self.betterPrint("Clicking start button. . .")
                
            self.betterPrint(f"Writing unit nr. {str(x+1)} . . .")

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

                    if mistakes != 0:
                        try:
                            self.chars = int(browser.find_element(By.XPATH, LETTER_NUM).text)

                            if not random_numbers:
                                random_numbers = random.sample(range(0, self.chars + 1), mistakes)
                                self.betterPrint(f"Random mistake positions: {str(random_numbers)}")
                        except Exception as e:
                            print("Exception" + str(e))



                        if self.chars in random_numbers:
                            self.betterPrint("Made a mistake at: " + str(self.chars))
                            if character == "a":
                                keyboard.press("q")
                                keyboard.release("q")
                            else:
                                keyboard.press("a")
                                keyboard.release("a")


                except Exception as e:
                    if self.chars == 0:
                        print(" \n")
                        print(" \n")
                        self.betterPrint("Restarting unit")
                        break
                    
            
            driver.clickElementJavascript(HOUSE)
            
            self.betterPrint("Clicking house button. . .")
            
            driver.clickElement(UNIT)
            
            self.betterPrint("Clicking unit button. . .")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.worker_thread = WorkerThread() 
        self.worker_thread.progress_signal.connect(self.update_list_widget)
        
        self.setWindowTitle("Typefucker")
        self.setGeometry(100, 100, 400, 600)
        
        self.stacked_widget = QStackedWidget()
        
        self.page1 = self.create_page1()
        self.page2 = self.create_page2()
        
        self.stacked_widget.addWidget(self.page1)
        self.stacked_widget.addWidget(self.page2)
        
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)  
        layout.addWidget(self.stacked_widget)
        
        self.setCentralWidget(central_widget)  
    
    def create_page1(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        self.list_widget = QListWidget(self)
        
        self.button = QPushButton("Start", self)
        self.button.clicked.connect(self.start_task)
        
        layout.addWidget(self.list_widget)
        layout.addWidget(self.button)
        
        button = QPushButton("Settings Page")
        button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.page2))
        layout.addWidget(button)
        
        return page
    
    def create_page2(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        form_layout = QFormLayout()

        self.username_input = QLineEdit()
        form_layout.addRow("Username:", self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        form_layout.addRow("Password:", self.password_input)

        self.units_input = QLineEdit()
        self.units_input.setValidator(QIntValidator())
        form_layout.addRow("Units:", self.units_input)

        self.max_delay_input = QLineEdit()
        self.max_delay_input.setValidator(QDoubleValidator())
        form_layout.addRow("Maximum Delay:", self.max_delay_input)

        self.min_delay_input = QLineEdit()
        self.min_delay_input.setValidator(QDoubleValidator())
        form_layout.addRow("Minimum Delay:", self.min_delay_input)

        self.max_mistakes_input = QLineEdit()
        self.max_mistakes_input.setValidator(QDoubleValidator())
        form_layout.addRow("Maximum Mistakes:", self.max_mistakes_input)

        self.min_mistakes_input = QLineEdit()
        self.min_mistakes_input.setValidator(QDoubleValidator())
        form_layout.addRow("Minimum Mistakes:", self.min_mistakes_input)

        layout.addLayout(form_layout)

        button_layout = QHBoxLayout()

        submit_btn = QPushButton("Save Info")
        submit_btn.clicked.connect(self.validate_and_submit)
        button_layout.addWidget(submit_btn)

        clear_btn = QPushButton("Clear")
        clear_btn.clicked.connect(self.clear_fields)
        button_layout.addWidget(clear_btn)

        layout.addLayout(button_layout)

        self.setLayout(layout)
        
        button = QPushButton("Start Page")
        button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.page1))
        layout.addWidget(button)
        
        return page
        
    def validate_and_submit(self):
        self.username = self.username_input.text().strip()
        self.password = self.password_input.text().strip()
        self.units = self.units_input.text().strip()
        self.max_delay = self.max_delay_input.text().strip()
        self.min_delay = self.min_delay_input.text().strip()
        self.max_mistakes = self.max_mistakes_input.text().strip()
        self.min_mistakes = self.min_mistakes_input.text().strip()

        if not self.username:
            self.show_error("Username cannot be empty!")
            return

        if not self.password:
            self.show_error("Password cannot be empty!")
            return

        if not self.units:
            self.show_error("Units must be an integer!")
            return

        if not self.max_delay:
            self.show_error("Maximum Delay must be a number!")
            return

        if not self.min_delay:
            self.show_error("Minimum Delay must be a number!")
            return

        if not self.max_mistakes:
            self.show_error("Maximum Mistakes must be a number!")
            return

        if not self.min_mistakes:
            self.show_error("Minimum Mistakes must be a number!")
            return

        QMessageBox.information(self, "Success", "All data is valid and submitted successfully!")
        self.worker_thread.username = self.username
        self.worker_thread.password = self.password
        self.worker_thread.units = self.units
        self.worker_thread.maxDelay = self.max_delay
        self.worker_thread.minDelay = self.min_delay
        self.worker_thread.maxMistakes = self.max_mistakes
        self.worker_thread.minMistakes = self.min_mistakes
        self.worker_thread.saveInfo()


    def clear_fields(self):
        self.username_input.clear()
        self.password_input.clear()
        self.units_input.clear()
        self.max_delay_input.clear()
        self.min_delay_input.clear()
        self.max_mistakes_input.clear()
        self.min_mistakes_input.clear()

    def show_error(self, message):
        QMessageBox.critical(self, "Error", message)
        
    def start_task(self):
        self.button.setEnabled(False)
        self.worker_thread.start()
        self.worker_thread.finished.connect(self.task_finished)    
        
    def task_finished(self):
        self.button.setEnabled(True)
        
    def update_list_widget(self, message):
            self.list_widget.addItem(message)  
            self.list_widget.scrollToBottom()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
