import tkinter as tk
from pathlib import Path
from tkinter import ttk
from connect import create_connection
from tkinter import messagebox as msb
from tkinter import Canvas, Button, PhotoImage

OUTPUT_PATH = Path("C:\build").parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame0")

def obtercep():
        cep_selecionado
        return cep_selecionado 

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class tabelasFormCIDADE:
    def __init__(self, root):
        self.root = root
        self.tabela_frame = tk.Frame(root, bg='white', width=635, height=400)
        self.tabela_frame.place(x=328.0, y=110)

        self.lista_form_cidade = self.create_lista_form_cidade()  
        self.exibir_lista_cidade()
        self.create_inputs_tabela()
        self.lista_form_cidade.bind('<<TreeviewSelect>>', self.Selecionarcep)

    def create_inputs_tabela(self):
        self.button_PESQUISA_img = tk.PhotoImage(file=relative_to_assets("pesquisa.png"))
        button_pesquisa = tk.Button(self.tabela_frame, image=self.button_PESQUISA_img, width=42, height=33.81, command=self.pesquisa_db)
        button_pesquisa.place(relx=0.89, rely=0.89)

        self.pesquisa_caixa = tk.Entry(self.tabela_frame, bg='orange', fg="white", width=16, font=("Arial", 14))
        self.pesquisa_caixa.place(relx=0.587, rely=0.908)

    def create_lista_form_cidade(self):
        lista_form = ttk.Treeview(self.tabela_frame, height=3, columns=("col1", "col2", "col3"), selectmode='extended')
        lista_form.heading("#0", text="")
        lista_form.heading("#1", text="CEP")
        lista_form.heading("#2", text="NOME")
        lista_form.heading("#3", text="ESTADO")

        lista_form.column("#0", width=1)
        lista_form.column("#1", width=99)
        lista_form.column("#2", width=300)
        lista_form.column("#3", width=100, anchor='center')


        lista_form.tag_configure('centered', anchor='center')       
        lista_form.place(relx=0, relwidth=0.97, rely=0, relheight=0.85)

        scroll_lista = tk.Scrollbar(self.tabela_frame, orient='vertical', command=lista_form.yview)
        lista_form.configure(yscroll=scroll_lista.set)
        scroll_lista.place(relx=0.97, rely=0, relheight=0.85)

        return lista_form

    def exibir_lista_cidade(self):
        with create_connection() as conexao:
            cursor = conexao.cursor()
            try:
                self.lista_form_cidade.delete(*self.lista_form_cidade.get_children())
                cursor.execute("""SELECT CEP, NOME, ESTADO FROM CIDADE ORDER BY CEP ASC;""")
                lista = cursor.fetchall()
                for item in lista:
                    self.lista_form_cidade.insert('', 'end', values=item)
            except Exception as e:
                msb.showerror("Error", str(e))

    def pesquisa_db(self):
        with create_connection() as conexao:
            cursor = conexao.cursor()
            try:
                pesquisa = self.pesquisa_caixa.get()
                if pesquisa == "":
                    self.exibir_lista_cidade()
                else:  
                    self.lista_form_cidade.delete(*self.lista_form_cidade.get_children())
                    comando_pesquisar = """SELECT CEP, NOME, ESTADO FROM CIDADE WHERE NOME LIKE %s ORDER BY CEP ASC"""
                    cursor.execute(comando_pesquisar, ('%' + pesquisa + '%',))
                    lista = cursor.fetchall()
                    for item in lista:
                        self.lista_form_cidade.insert('', 'end', values=item)
            except Exception as e:
                msb.showerror("Error", str(e))

    def Selecionarcep(self, event):
        selected_items = self.lista_form_cidade.selection()
        if selected_items:
            for item_id in selected_items:
                item = self.lista_form_cidade.item(item_id)
                cep = item['values'][0]  
                global cep_selecionado
                cep_selecionado = cep
