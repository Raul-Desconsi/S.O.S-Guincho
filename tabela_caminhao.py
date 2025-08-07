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


def obtervariavel():
        placa_selecionada
        return placa_selecionada    

class TabelasFormCaminhao:
    def __init__(self, root):
        self.root = root
        self.tabela_frame = tk.Frame(root, bg='white', width=635, height=400)
        self.tabela_frame.place(x=328.0, y=110)

        self.lista_form_caminhao = self.create_lista_form_caminhao()  
        self.exibir_lista_caminhao()
        self.create_inputs_tabela()
        self.lista_form_caminhao.bind('<<TreeviewSelect>>', self.Selecionarplaca)
    
    def create_inputs_tabela(self):
        button_PESQUISA_img = tk.PhotoImage(file=relative_to_assets("pesquisa.png"))
        button_pesquisa = tk.Button(self.tabela_frame, image=button_PESQUISA_img, width=42, height=33.81, command=self.pesquisa_db)
        button_pesquisa.place(relx=0.89, rely=0.89)

        self.pesquisa_caixa = tk.Entry(self.tabela_frame, bg='orange', fg="white", width=16, font=("Arial", 14))
        self.pesquisa_caixa.place(relx=0.587, rely=0.908)
        button_pesquisa.image = button_PESQUISA_img

    def create_lista_form_caminhao(self):
        lista_form = ttk.Treeview(self.tabela_frame, height=3, columns=("col1", "col2", "col3"), selectmode='extended')
        lista_form.heading("#0", text="")
        lista_form.heading("#1", text="PLACA")
        lista_form.heading("#2", text="MODELO")
        lista_form.heading("#3", text="COR")

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

    def exibir_lista_caminhao(self):
        with create_connection() as conexao:
            cursor = conexao.cursor()
            try:
                self.lista_form_caminhao.delete(*self.lista_form_caminhao.get_children())
                cursor.execute("""SELECT PLACA, FABRICANTE_MODELO, COR, STATUS 
                                FROM CAMINHAO 
                                WHERE STATUS = 'disponível' 
                                ORDER BY PLACA ASC;""")
                lista = cursor.fetchall()
                for item in lista:
                    self.lista_form_caminhao.insert('', 'end', values=item)
            except Exception as e:
                msb.showerror("Error", str(e))

    def pesquisa_db(self):
        with create_connection() as conexao:
            cursor = conexao.cursor()
            try:
                pesquisa = self.pesquisa_caixa.get()
                if pesquisa == "":
                    self.exibir_lista_caminhao()
                else:  
                    self.lista_form_caminhao.delete(*self.lista_form_caminhao.get_children())
                    comando_pesquisar = """SELECT PLACA, FABRICANTE_MODELO, COR, STATUS 
                                        FROM CAMINHAO 
                                        WHERE STATUS = 'disponível' 
                                        AND FABRICANTE_MODELO LIKE %s 
                                        ORDER BY FABRICANTE_MODELO ASC"""
                    cursor.execute(comando_pesquisar, ('%' + pesquisa + '%',))
                    lista = cursor.fetchall()
                    for item in lista:
                        self.lista_form_caminhao.insert('', 'end', values=item)
            except Exception as e:
                msb.showerror("Error", str(e))


    def Selecionarplaca(self, event):
        global placa_selecionada
        selected_items = self.lista_form_caminhao.selection()
        if selected_items:
            for item_id in selected_items:
                item = self.lista_form_caminhao.item(item_id)
                placa = item['values'][0]  
                placa_selecionada = placa
                  



