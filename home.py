import tkinter as tk
from pathlib import Path
from tkinter import ttk
from connect import create_connection
from tkinter import messagebox as msb
from tkinter import Canvas, Button, PhotoImage



OUTPUT_PATH = Path("C:\build").parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame0")

def relative_to_assets(path: str) -> Path:

    return ASSETS_PATH / Path(path)

class HomeForm:
    def __init__(self, root):
        self.root = root
        self.Home_frame = tk.Frame(root, bg='white', width=933, height=580)
        self.Home_frame.place(x=320, y=150)


        self.create_inputs()
        self.show_item_counts()
    def create_inputs(self):
            
            img_background = tk.PhotoImage(file=relative_to_assets("HM_BK.png"))
            
            image_label = tk.Label(self.Home_frame, image=img_background, bg='#3A3A3A')        
            image_label.place(x=466, y=290, anchor='center')
            image_label.image =img_background


    def show_item_counts(self):
        connection = create_connection() 
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM caminhao")
        caminhao_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM cidade")
        cidade_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM motorista")
        motorista_count = cursor.fetchone()[0]

        cursor.close()
        connection.close()

        tk.Label(self.Home_frame, text=f'{motorista_count}', bg='#2c2c31', fg='white', font=("Arial", 21)).place(relx=0.5, rely=0.65, anchor='center')
            
        tk.Label(self.Home_frame, text=f' {cidade_count}', bg='#2c2c31', fg='white', font=("Arial", 21)).place(relx=0.36, rely=0.65, anchor='center')

        tk.Label(self.Home_frame, text=f' {caminhao_count}', bg='#2c2c31', fg='white', font=("Arial", 21)).place(relx=0.635, rely=0.65, anchor='center')
