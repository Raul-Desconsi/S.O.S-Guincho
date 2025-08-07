import tkinter as tk
from pathlib import Path
from tkinter import ttk
from connect import create_connection
from tkinter import messagebox as msb

OUTPUT_PATH = Path("C:\build").parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame0")

def relative_to_assets(path: str) -> Path:

    return ASSETS_PATH / Path(path)

class CaminhaoForm:
    def __init__(self, root):
        self.root = root
        self.caminhao_frame = tk.Frame(root, bg='white', width=933, height=580)
        self.caminhao_frame.place(x=320, y=150)
        
        self.lista_form = self.create_lista_form_caminhao()  
        self.create_inputs()
        self.exibir_lista()
    
    def create_inputs(self):
        button_ADICIONAR_img = tk.PhotoImage(file=relative_to_assets("button_adicionar.png"))
        button_REMOVER_img = tk.PhotoImage(file=relative_to_assets("button_remover.png"))
        button_EDITAR_img = tk.PhotoImage(file=relative_to_assets("button_editar.png"))
        button_ATUALIZA_img = tk.PhotoImage(file=relative_to_assets("button_atualiza.png"))
        button_PESQUISA_img = tk.PhotoImage(file=relative_to_assets("pesquisa.png"))

        self.pesquisa_caixa = tk.Entry(self.caminhao_frame, bg='orange', fg="white", width=20, font=("Arial", 14))
        self.pesquisa_caixa.place(relx=0.67, y=15)

        button_adicionar = tk.Button(self.caminhao_frame, image=button_ADICIONAR_img, width=144, height=43, command=self.exibir_add)
        button_adicionar.place(relx=0.22, y=525)

        button_remover = tk.Button(self.caminhao_frame, image=button_REMOVER_img, width=144, height=43, command=self.remover_db)
        button_remover.place(relx=0.42, y=525)
        
        button_editar = tk.Button(self.caminhao_frame, image=button_EDITAR_img, width=144, height=43, command=self.exibir_edit)
        button_editar.place(relx=0.62, y=525)
        
        button_atualiza = tk.Button(self.caminhao_frame, image=button_ATUALIZA_img, width=51.01, height=43.73, command=self.exibir_lista)
        button_atualiza.place(relx=0.91, y=525)

        button_pesquisa = tk.Button(self.caminhao_frame, image=button_PESQUISA_img, width=42, height=33.81, command=self.pesquisa_db)
        button_pesquisa.place(relx=0.92, y=7)
        
        button_adicionar.image = button_ADICIONAR_img
        button_remover.image = button_REMOVER_img
        button_editar.image = button_EDITAR_img
        button_atualiza.image = button_ATUALIZA_img
        button_pesquisa.image = button_PESQUISA_img

    def create_lista_form_caminhao(self):
        lista_form = ttk.Treeview(self.caminhao_frame, height=3, columns=("col1", "col2", "col3","col4"), selectmode='extended')
        lista_form.heading("#0", text="")
        lista_form.heading("#1", text="PLACA")
        lista_form.heading("#2", text="MODELO")
        lista_form.heading("#3", text="COR")
        lista_form.heading("#4", text="STATUS")

        lista_form.column("#0", width=1)
        lista_form.column("#1", width=140)
        lista_form.column("#2", width=350)
        lista_form.column("#3", width=60,anchor='center')
        lista_form.column("#4", width=70,anchor='center')
        
        lista_form.tag_configure('centered', anchor='center')       
        lista_form.place(relx=0, relwidth=0.97, rely=0.1, relheight=0.77)
        
        
        scroll_lista = tk.Scrollbar(self.caminhao_frame, orient='vertical', command=lista_form.yview)
        lista_form.configure(yscroll=scroll_lista.set)
        scroll_lista.place(relx=0.98, rely=0.1, relheight=0.77)

        return lista_form

    def exibir_lista(self):
        with create_connection() as conexao:
            cursor = conexao.cursor()
            try:
                self.lista_form.delete(*self.lista_form.get_children())
                cursor.execute("""SELECT PLACA, FABRICANTE_MODELO , COR, STATUS FROM CAMINHAO ORDER BY PLACA ASC;""")
                lista = cursor.fetchall()
                for item in lista:
                    self.lista_form.insert('', 'end', values=item)
            except Exception as e:
                msb.showerror("Error", str(e))

    def pesquisa_db(self):
        with create_connection() as conexao:
            cursor = conexao.cursor()
            try:
                pesquisa = self.pesquisa_caixa.get()
                if pesquisa:
                    self.lista_form.delete(*self.lista_form.get_children())
                    comando_pesquisar = """SELECT PLACA, FABRICANTE_MODELO, COR, STATUS FROM CAMINHAO WHERE FABRICANTE_MODELO LIKE %s ORDER BY FABRICANTE_MODELO ASC"""
                    cursor.execute(comando_pesquisar, ('%' + pesquisa + '%',))
                    lista = cursor.fetchall()
                    for item in lista:
                        self.lista_form.insert('', 'end', values=item)
            except Exception as e:
                msb.showerror("Error", str(e))

    def exibir_add(self):
        add_window = tk.Toplevel(self.root)
        Add(add_window)

    def remover_db(self):
        selected_items = self.lista_form.selection()  
        if msb.askyesno("Confirmar", "Você tem certeza que deseja apagar este caminhão? motoristas podem ficar sem caminhão !"):
            with create_connection() as conexao:
                cursor = conexao.cursor()

                try:
                    for item_id in selected_items:
                        item = self.lista_form.item(item_id)
                        placa = item['values'][0]  

                        comando_update_motorista = """UPDATE motorista 
                                                    SET guincho = '0' 
                                                    WHERE guincho = %s"""
                        cursor.execute(comando_update_motorista, (placa,))

                        comando_delete = "DELETE FROM caminhao WHERE placa = %s"
                        cursor.execute(comando_delete, (placa,))
                    
                    conexao.commit()
                except Exception as e:
                    msb.showerror("Error", str(e))
                
                self.exibir_lista()


    def SelecionarItem(self):
            
            selected_items = self.lista_form.selection()
            global placa_selecionar 
            placa_selecionar ="null"
            for item_id in selected_items:
                    item = self.lista_form.item(item_id)
        
                    placa_selecionar = item['values'][0]      
                    
    def exibir_edit(self):
        self.SelecionarItem()
        add_window = tk.Toplevel(self.root)
        Edit(add_window, self.exibir_lista)
        
        
        
class Add:
    def __init__(self, root):
        self.root = root
        self.caminhao_frame_add = tk.Frame(root, bg='#3A3A3A', width=400, height=550)
        root.resizable(False, False)
        self.caminhao_frame_add.pack()
        self.create_inputs_add()
    
    def create_inputs_add(self):
        button_aplicar_img = tk.PhotoImage(file=relative_to_assets("APLICAR.png"))
        button_limpa_img = tk.PhotoImage(file=relative_to_assets("LIMPAR.png"))

        button_aplicar = tk.Button(self.caminhao_frame_add, image=button_aplicar_img, bg='#3A3A3A', borderwidth=0, width=122, height=33.64, command=self.add_db)
        button_aplicar.place(relx=0.3, rely=0.82, anchor='center')

        button_limpar = tk.Button(self.caminhao_frame_add, image=button_limpa_img, bg='#3A3A3A', borderwidth=0, width=122, height=33.64, command=self.apagar_campo)
        button_limpar.place(relx=0.7, rely=0.82, anchor='center')

        tk.Label(self.caminhao_frame_add, text="ADICIONAR CAMINHÔES", bg='#3A3A3A', fg='white', font=("Arial", 20)).place(relx=0.5, rely=0.1, anchor='center')

        tk.Label(self.caminhao_frame_add, text="Placa", bg='#3A3A3A', fg='white', font=("Arial",13)).place(relx=0.5, rely=0.25, anchor='center')
        self.entry_placa = tk.Entry(self.caminhao_frame_add, bg='orange', width=20, font=("Arial", 12))
        self.entry_placa.place(relx=0.5, rely=0.3, anchor='center')

        tk.Label(self.caminhao_frame_add, text="Modelo", bg='#3A3A3A', fg='white', font=("Arial",13)).place(relx=0.5, rely=0.4, anchor='center')
        self.entry_modelo = tk.Entry(self.caminhao_frame_add, bg='orange', width=20, font=("Arial", 12))
        self.entry_modelo.place(relx=0.5, rely=0.45, anchor='center')


        # Lista de cores para a ComboBox #
        cb_lista_cor = ["SELECIONE","PRETO","BRANCO","CINZA","LARANJA","VERDE","AMARELO","ROXO","ROSA","VERMELHO","AZUL"]
        
        # ComboBox para selecionar cor 
        tk.Label(self.caminhao_frame_add, text="Cor", bg='#3A3A3A', fg='white', font=("Arial",13)).place(relx=0.5, rely=0.55, anchor='center')
        self.cb_cor = ttk.Combobox(self.caminhao_frame_add, values=cb_lista_cor, width=28,  state='readonly',style='TCombobox')
        self.cb_cor.place(relx=0.5, rely=0.6, anchor='center')
        self.cb_cor.set("SELECIONE")
        #


        button_aplicar.image = button_aplicar_img
        button_limpar.image = button_limpa_img

    def add_db(self):
            conexao = create_connection()
            cursor = conexao.cursor()
            placa = self.entry_placa.get()
            modelo = self.entry_modelo.get()
            cor = self.cb_cor.get()
            
            try:
                if placa and modelo and cor != "SELECIONE" and cor:
                    comando = "INSERT INTO CAMINHAO (placa, fabricante_modelo, cor ,status ) VALUES (%s, %s, %s,'Disponivel')"
                    cursor.execute(comando, (placa, modelo, cor))
                    conexao.commit()
                    self.root.destroy()
                else: 
                    msb.showwarning("Alert", "Preencha todos os campos")
            finally:
                cursor.close()
                conexao.close()

    def apagar_campo(self):
        self.entry_placa.delete(0, tk.END)
        self.entry_modelo.delete(0, tk.END)

class Edit:
    def __init__(self, root, refresh_list_callback):
        self.root = root
        self.refresh_list_callback = refresh_list_callback
        self.caminhao_frame_edit = tk.Frame(root, bg='#3A3A3A', width=400, height=550)
        root.resizable(False, False)
        self.caminhao_frame_edit.pack()
        self.create_inputs_edit()
        
    def create_inputs_edit(self):
        button_aplicar_img = tk.PhotoImage(file=relative_to_assets("APLICAR.png"))
        button_limpa_img = tk.PhotoImage(file=relative_to_assets("LIMPAR.png"))

        button_aplicar = tk.Button(self.caminhao_frame_edit, image=button_aplicar_img, bg='#3A3A3A', borderwidth=0, width=122, height=33.64, command=self.editar_db)
        button_aplicar.place(relx=0.3, rely=0.82, anchor='center')

        button_limpar = tk.Button(self.caminhao_frame_edit, image=button_limpa_img, bg='#3A3A3A', borderwidth=0, width=122, height=33.64, command=self.apagar_campo)
        button_limpar.place(relx=0.7, rely=0.82, anchor='center')

        tk.Label(self.caminhao_frame_edit, text="EDITAR CAMINHÔES", bg='#3A3A3A', fg='white', font=("Arial", 20)).place(relx=0.5, rely=0.1, anchor='center')

        tk.Label(self.caminhao_frame_edit, text="Placa", bg='#3A3A3A', fg='white', font=("Arial", 13)).place(relx=0.5, rely=0.25, anchor='center')
        self.entry_placa = tk.Entry(self.caminhao_frame_edit, bg='orange', width=20, font=("Arial", 12))
        if placa_selecionar != "null":
            self.entry_placa.insert(0, placa_selecionar)  
        self.entry_placa.place(relx=0.5, rely=0.3, anchor='center')

        tk.Label(self.caminhao_frame_edit, text="Modelo", bg='#3A3A3A', fg='white', font=("Arial",13)).place(relx=0.5, rely=0.4, anchor='center')
        self.entry_modelo = tk.Entry(self.caminhao_frame_edit, bg='orange', width=20, font=("Arial", 12))
        self.entry_modelo.place(relx=0.5, rely=0.45, anchor='center')


        # Lista de cores para a ComboBox #
        cb_lista_cor = ["SELECIONE","PRETO","BRANCO","CINZA","LARANJA","VERDE","AMARELO","ROXO","ROSA","VERMELHO","AZUL"]
        
        # ComboBox para selecionar cor 
        tk.Label(self.caminhao_frame_edit, text="Cor", bg='#3A3A3A', fg='white', font=("Arial",13)).place(relx=0.5, rely=0.55, anchor='center')
        self.cb_cor = ttk.Combobox(self.caminhao_frame_edit, values=cb_lista_cor, width=28,  state='readonly',style='TCombobox')
        self.cb_cor.place(relx=0.5, rely=0.6, anchor='center')
        self.cb_cor.set("SELECIONE")
        #
        
        button_aplicar.image = button_aplicar_img
        button_limpar.image = button_limpa_img
        
    def apagar_campo(self):
        self.entry_placa.delete(0, tk.END)
        self.entry_modelo.delete(0, tk.END)
        self.cb_cor.delete(0, tk.END)

    def editar_db(self):
        conexao = create_connection()
        cursor = conexao.cursor()
        placa = self.entry_placa.get()
        modelo = self.entry_modelo.get()
        cor = self.cb_cor.get()

        try:
            if placa and modelo and cor !="SELECIONE" and cor :
                comando = "UPDATE CAMINHAO SET Fabricante_modelo = %s, COR = %s WHERE PLACA = %s"
                cursor.execute(comando, (modelo, cor, placa))
                conexao.commit()
                self.root.destroy()
            else:
                msb.showwarning("Alert", "Preencha todos os campos")
        finally:
            cursor.close()
            conexao.close()


                
              
    