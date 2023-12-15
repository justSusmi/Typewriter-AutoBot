import tkinter as tk

def on_select(event):
    selected_item = listbox.get(listbox.curselection())
    window.configure(bg=selected_item)
    listbox.config(bg=selected_item)
    title.config(bg=selected_item)


window = tk.Tk()
window.title("Typefucker")
window.geometry("500x500")

title = tk.Label(window, text="Typefucker")
title.pack(pady=20)

usernameEntry = tk.Entry(window)
usernameEntry.pack(pady=20)

usernameLabel = tk.Label(window, text="Username")
usernameLabel.place(x=800, y=80)

passwordEntry = tk.Entry(window)
passwordEntry.pack(pady=20)

passwordLabel = tk.Label(window, text="Password")
passwordLabel.place(x=800, y=140)


items = ["blue", "green", "orange", "red", "magenta"]
listbox = tk.Listbox(window, selectmode=tk.SINGLE, selectbackground="black", selectforeground="white")
for item in items:
    listbox.insert(tk.END, item)
listbox.bind("<<ListboxSelect>>", on_select)
    
    
listbox.place(x=10, y=10)

window.mainloop()