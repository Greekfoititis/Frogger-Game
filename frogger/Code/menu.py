import subprocess
import sys
from tkinter import *
from tkinter import messagebox
import tkinter as tk
import os

# Define paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VISUALS_DIR = os.path.join(BASE_DIR, "..", "visuals")

# Create the main window 
root = Tk()
root.title("MENU")
root.geometry("500x600")

# Create Canvas and load PhotoImage AFTER root is initialized
C = Canvas(root, bg="blue", height=250, width=300)
filename = PhotoImage(file=os.path.join(VISUALS_DIR, "menupic.png"))

background_label = Label(root, image=filename)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

my_menu = Menu(root)
root.config(menu=my_menu)

def info():
    messagebox.showinfo(
        title="Hello", 
        message="THE OBJECTIVE OF THE GAME IS TO GUIDE THE FROG TO THE HOMES WITHOUT HITTING OBSTACLES. YOU HAVE 3 LIVES AND THERE IS A TIME LIMIT SHOWN ON THE GREEN BAR. MOVEMENT IS CONTROLLED USING THE WASD KEYS OR THE ARROW KEYS."
    )

file_menu = Menu(my_menu)
my_menu.add_cascade(label="GAME INFORMATION", command=info)

def frogger():
    subprocess.Popen([sys.executable, os.path.join(os.path.dirname(__file__), "frogger.py")])

button2 = tk.Button(root, text="Exit", fg="black", bg="green", command=exit)
button2.config(width=20, height=4)
button1 = tk.Button(root, text="Start", fg="black", bg="green", command=frogger)
button1.config(width=20, height=4)
button1.place(x=150, y=220)
button2.place(x=150, y=310)


root.mainloop()