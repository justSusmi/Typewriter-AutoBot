import tkinter as tk
from tkinter import messagebox
import json

from constants import *
from workerThread import WorkerThread

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Typefucker")
        self.geometry("400x600")
        
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
        try:
            with open("user_data.json", "r") as file:
                user_data = json.load(file)

            self.username_input.delete(0, tk.END)
            self.username_input.insert(0, user_data.get("username", ""))
            
            self.password_input.delete(0, tk.END)
            self.password_input.insert(0, user_data.get("password", ""))
            
            self.units_input.delete(0, tk.END)
            self.units_input.insert(0, user_data.get("units", ""))
            
            self.max_delay_input.delete(0, tk.END)
            self.max_delay_input.insert(0, user_data.get("maxDelay", ""))
            
            self.min_delay_input.delete(0, tk.END)
            self.min_delay_input.insert(0, user_data.get("minDelay", ""))
            
            self.max_mistakes_input.delete(0, tk.END)
            self.max_mistakes_input.insert(0, user_data.get("maxMistakes", ""))

            
            self.min_mistakes_input.delete(0, tk.END)
            self.min_mistakes_input.insert(0, user_data.get("minMistakes", ""))
            
        except Exception as e:
            self.betterPrint("Es gibt noch keine User Daten!" + str(e))
        

    def update_list_widget(self, message):
        self.listbox.insert(tk.END, message)
        self.listbox.yview(tk.END)

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()