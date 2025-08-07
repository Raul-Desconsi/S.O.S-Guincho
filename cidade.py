import tkinter as tk
from pathlib import Path
from tkinter import ttk
from connect import create_connection
from tkinter import messagebox as msb

OUTPUT_PATH = Path("C:\build").parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame0")

def relative_to_assets(path: str) -> Path:

    return ASSETS_PATH / Path(path)

class CidadeForm:
    def __init__(self, root):
        self.root = root
        self.cidade_frame = tk.Frame(root, bg='white', width=933, height=580)
        self.cidade_frame.place(x=320, y=150)
        
        self.lista_cidade = self.create_lista_form_cidade()
        self.create_inputs()
        self.exibir_lista()
    
    def create_inputs(self):
        button_ADICIONAR_img = tk.PhotoImage(file=relative_to_assets("button_adicionar.png"))
        button_REMOVER_img = tk.PhotoImage(file=relative_to_assets("button_remover.png"))
        button_EDITAR_img = tk.PhotoImage(file=relative_to_assets("button_editar.png"))
        button_ATUALIZA_img = tk.PhotoImage(file=relative_to_assets("button_atualiza.png"))
        button_PESQUISA_img = tk.PhotoImage(file=relative_to_assets("pesquisa.png"))

        self.pesquisa_caixa = tk.Entry(self.cidade_frame, bg='orange', fg="white", width=20, font=("Arial", 14))
        self.pesquisa_caixa.place(relx=0.67, y=15)

        button_adicionar = tk.Button(self.cidade_frame, image=button_ADICIONAR_img, width=144, height=43, command=self.exibir_add)
        button_adicionar.place(relx=0.22, y=525)

        button_remover = tk.Button(self.cidade_frame, image=button_REMOVER_img, width=144, height=43, command=self.remover_cidade_db)
        button_remover.place(relx=0.42, y=525)
        
        button_editar = tk.Button(self.cidade_frame, image=button_EDITAR_img, width=144, height=43, command=self.exibir_edit)
        button_editar.place(relx=0.62, y=525)
        
        button_atualiza = tk.Button(self.cidade_frame, image=button_ATUALIZA_img, width=51.01, height=43.73, command=self.exibir_lista)
        button_atualiza.place(relx=0.91, y=525)

        button_pesquisa = tk.Button(self.cidade_frame, image=button_PESQUISA_img, width=42, height=33.81, command=self.pesquisa_db)
        button_pesquisa.place(relx=0.92, y=7)
        
        button_adicionar.image = button_ADICIONAR_img
        button_remover.image = button_REMOVER_img
        button_editar.image = button_EDITAR_img
        button_atualiza.image = button_ATUALIZA_img
        button_pesquisa.image = button_PESQUISA_img

    def create_lista_form_cidade(self):
        lista_cidade = ttk.Treeview(self.cidade_frame, height=3, columns=("col1", "col2", "col3"), selectmode='extended')
        lista_cidade.heading("#0", text="")
        lista_cidade.heading("#1", text="CEP")
        lista_cidade.heading("#2", text="NOME")
        lista_cidade.heading("#3", text="ESTADO")

        lista_cidade.column("#0", width=1)
        lista_cidade.column("#1", width=177)
        lista_cidade.column("#2", width=450)
        lista_cidade.column("#3", width=150)
        
        lista_cidade.place(relx=0, relwidth=0.97, rely=0.1, relheight=0.77)
        
        scroll_lista = tk.Scrollbar(self.cidade_frame, orient='vertical', command=lista_cidade.yview)
        lista_cidade.configure(yscroll=scroll_lista.set)
        scroll_lista.place(relx=0.98, rely=0.1, relheight=0.77)

        return lista_cidade

    def exibir_lista(self):
        conexao = create_connection()
        cursor = conexao.cursor()
        
        try:
            self.lista_cidade.delete(*self.lista_cidade.get_children())
            cursor.execute("""SELECT CEP, NOME, ESTADO FROM CIDADE ORDER BY CEP ASC;""")
            lista = cursor.fetchall()
            for item in lista:
                self.lista_cidade.insert('', 'end', values=item)
        finally:
            cursor.close()
            conexao.close()

    def pesquisa_db(self):
        conexao = create_connection()
        cursor = conexao.cursor()
        
        try:
            pesquisa = self.pesquisa_caixa.get()
            if pesquisa:
                self.lista_cidade.delete(*self.lista_cidade.get_children())
                comando_pesquisar = """SELECT CEP, NOME, ESTADO FROM CIDADE WHERE NOME LIKE %s ORDER BY CEP ASC"""
                cursor.execute(comando_pesquisar, ('%' + pesquisa + '%',))
                lista = cursor.fetchall()
                for item in lista:
                    self.lista_cidade.insert('', 'end', values=item)
        finally:
            cursor.close()
            conexao.close()

    def exibir_add(self):
        add_window = tk.Toplevel(self.root)
        CidadeAdd(add_window)

    def exibir_edit(self):
        add_window = tk.Toplevel(self.root)
        CidadeEdit(add_window, self.exibir_lista)

    def remover_cidade_db(self):
        selected_items = self.lista_cidade.selection()  
        if not selected_items:
            msb.showwarning("Alert", "Selecione um item para remover")
            return
        if msb.askyesno("Confirmar", "Você tem certeza que deseja apagar esta cidade ? motoristas podem ficar sem cidade !"):
            conexao = create_connection()
            cursor = conexao.cursor()
            
            try:
                for item_id in selected_items:
                    item = self.lista_cidade.item(item_id)
                    cep = item['values'][0]  

                    
                    comando_update_motorista = """UPDATE motorista 
                                                SET cep_motorista = '0' 
                                                WHERE cep_motorista = %s"""
                    cursor.execute(comando_update_motorista, (cep,))

                    
                    comando_delete = "DELETE FROM cidade WHERE CEP = %s"
                    cursor.execute(comando_delete, (cep,))
                
                conexao.commit()
            except Exception as e:
                msb.showerror("Erro", str(e))
            finally:
                cursor.close()
                conexao.close()
            
            self.exibir_lista()
            
    def SelecionarItem(self):
            
            selected_items = self.lista_cidade.selection()
            global placa_selecionar 
            placa_selecionar ="null"
            for item_id in selected_items:
                    item = self.lista_cidade.item(item_id)
        
                    placa_selecionar = item['values'][0]      
                    
    def exibir_edit(self):
        self.SelecionarItem()
        add_window = tk.Toplevel(self.root)
        CidadeEdit(add_window, self.exibir_lista)

class CidadeAdd:
    def __init__(self, root):
        self.root = root
        self.cidade_frame_add = tk.Frame(root, bg='#3A3A3A', width=400, height=550)
        root.resizable(False, False)
        self.cidade_frame_add.pack()
        self.create_inputs_add()

    def create_inputs_add(self):
        button_aplicar_img = tk.PhotoImage(file=relative_to_assets("APLICAR.png"))
        button_limpa_img = tk.PhotoImage(file=relative_to_assets("LIMPAR.png"))

        button_aplicar = tk.Button(self.cidade_frame_add, image=button_aplicar_img, bg='#3A3A3A', borderwidth=0, width=122, height=33.64, command=self.add_cidade_db)
        button_aplicar.place(relx=0.3, rely=0.82, anchor='center')

        button_limpar = tk.Button(self.cidade_frame_add, image=button_limpa_img, bg='#3A3A3A', borderwidth=0, width=122, height=33.64, command=self.apagar_campo)
        button_limpar.place(relx=0.7, rely=0.82, anchor='center')

        tk.Label(self.cidade_frame_add, text="ADICIONAR CIDADES", bg='#3A3A3A', fg='white', font=("Arial", 20)).place(relx=0.5, rely=0.1, anchor='center')

        tk.Label(self.cidade_frame_add, text="CEP", bg='#3A3A3A', fg='white', font=("Arial",13)).place(relx=0.5, rely=0.25, anchor='center')
        self.entry_CEP = tk.Entry(self.cidade_frame_add, bg='orange', width=20, font=("Arial", 12))
        self.entry_CEP.place(relx=0.5, rely=0.3, anchor='center')

        tk.Label(self.cidade_frame_add, text="Nome", bg='#3A3A3A', fg='white', font=("Arial",13)).place(relx=0.5, rely=0.4, anchor='center')
        self.entry_nome = tk.Entry(self.cidade_frame_add, bg='orange', width=20, font=("Arial", 12))
        self.entry_nome.place(relx=0.5, rely=0.45, anchor='center')

        tk.Label(self.cidade_frame_add, text="Estado", bg='#3A3A3A', fg='white', font=("Arial",13)).place(relx=0.5, rely=0.55, anchor='center')
        self.entry_estado = tk.Entry(self.cidade_frame_add, bg='orange', width=20, font=("Arial", 12))
        self.entry_estado.place(relx=0.5, rely=0.6, anchor='center')

        button_aplicar.image = button_aplicar_img
        button_limpar.image = button_limpa_img

    def add_cidade_db(self):
        conexao = create_connection()
        cursor = conexao.cursor()
        cep = self.entry_CEP.get()
        nome = self.entry_nome.get()
        estado = self.entry_estado.get()
        
        try:
            if cep and nome and estado:
                comando = "INSERT INTO CIDADE (CEP, Nome, Estado) VALUES (%s, %s, %s)"
                cursor.execute(comando, (cep, nome, estado))
                conexao.commit()
                self.root.destroy()
            else: 
                msb.showwarning("Alert", "Preencha todos os campos")
        finally:
            cursor.close()
            conexao.close()

    def apagar_campo(self):
        self.entry_CEP.delete(0, tk.END)
        self.entry_nome.delete(0, tk.END)
        self.entry_estado.delete(0, tk.END)

class CidadeEdit:
    def __init__(self, root, refresh_list_callback):
        self.root = root
        self.refresh_list_callback = refresh_list_callback
        self.cidade_frame_edit = tk.Frame(root, bg='#3A3A3A', width=400, height=550)
        root.resizable(False, False)
        self.cidade_frame_edit.pack()
        self.create_inputs_edit()

    def create_inputs_edit(self):
        button_aplicar_img = tk.PhotoImage(file=relative_to_assets("APLICAR.png"))
        button_limpar_img = tk.PhotoImage(file=relative_to_assets("LIMPAR.png"))

        button_aplicar = tk.Button(
            self.cidade_frame_edit, image=button_aplicar_img, bg='#3A3A3A', borderwidth=0, width=122, height=33.64, command=self.editar_db)
        button_aplicar.place(relx=0.3, rely=0.82, anchor='center')

        button_limpar = tk.Button(
            self.cidade_frame_edit, image=button_limpar_img, bg='#3A3A3A', borderwidth=0, width=122, height=33.64, command=self.apagar_campo)
        button_limpar.place(relx=0.7, rely=0.82, anchor='center')

        tk.Label(self.cidade_frame_edit, text="EDITAR CIDADE", bg='#3A3A3A', fg='white', font=("Arial", 20)).place(relx=0.5, rely=0.1, anchor='center')

        tk.Label(self.cidade_frame_edit, text="Cep", bg='#3A3A3A', fg='white', font=("Arial", 13)).place(relx=0.5, rely=0.25, anchor='center')
        self.entry_CEP = tk.Entry(self.cidade_frame_edit, bg='orange', width=20, font=("Arial", 12))
        if placa_selecionar != "null":
            self.entry_CEP.insert(0, placa_selecionar)  
        self.entry_CEP.place(relx=0.5, rely=0.3, anchor='center')

        tk.Label(self.cidade_frame_edit, text="Nome", bg='#3A3A3A', fg='white', font=("Arial", 13)).place(relx=0.5, rely=0.4, anchor='center')
        self.entry_nome = tk.Entry(self.cidade_frame_edit, bg='orange', width=20, font=("Arial", 12))
        self.entry_nome.place(relx=0.5, rely=0.45, anchor='center')

        tk.Label(self.cidade_frame_edit, text="Estado", bg='#3A3A3A', fg='white', font=("Arial", 13)).place(relx=0.5, rely=0.55, anchor='center')
        self.entry_estado = tk.Entry(self.cidade_frame_edit, bg='orange', width=20, font=("Arial", 12))
        self.entry_estado.place(relx=0.5, rely=0.6, anchor='center')

        button_aplicar.image = button_aplicar_img
        button_limpar.image = button_limpar_img

    def apagar_campo(self):
        self.entry_CEP.delete(0, tk.END)
        self.entry_nome.delete(0, tk.END)
        self.entry_estado.delete(0, tk.END)

    def editar_db(self):
        conexao = create_connection()
        cursor = conexao.cursor()
        cep = self.entry_CEP.get()
        nome = self.entry_nome.get()
        estado = self.entry_estado.get()

        try:
            if cep and nome and estado:
                comando = "UPDATE CIDADE SET NOME = %s, ESTADO = %s WHERE CEP = %s"
                cursor.execute(comando, (nome, estado, cep))
                conexao.commit()
                self.root.destroy()
            else:
                msb.showwarning("Alert", "Preencha todos os campos")
        finally:
            cursor.close()
            conexao.close()
