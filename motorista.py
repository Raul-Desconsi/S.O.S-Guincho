import tkinter as tk
from pathlib import Path
from tkinter import ttk
from connect import create_connection
from tkinter import messagebox as msb
from tkinter import Canvas, Button, PhotoImage
from tabela_caminhao import TabelasFormCaminhao
from tabela_form_cidade import tabelasFormCIDADE 
from tabela_caminhao import obtervariavel
from tabela_form_cidade import obtercep


OUTPUT_PATH = Path("C:\build").parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame0")

def relative_to_assets(path: str) -> Path:

    return ASSETS_PATH / Path(path)

class MotoristaForm:
    def __init__(self, root):
        self.root = root
        self.motorista_frame = tk.Frame(root, bg='white', width=933, height=580)
        self.motorista_frame.place(x=320, y=150)

        self.lista_motorista = self.create_lista_form_motorista()
        self.create_inputs()
        self.exibir_lista()
        
    def create_inputs(self):
            button_ADICIONAR_img = tk.PhotoImage(file=relative_to_assets("button_adicionar.png"))
            button_REMOVER_img = tk.PhotoImage(file=relative_to_assets("button_remover.png"))
            button_EDITAR_img = tk.PhotoImage(file=relative_to_assets("button_editar.png"))
            button_ATUALIZA_img = tk.PhotoImage(file=relative_to_assets("button_atualiza.png"))
            button_PESQUISA_img = tk.PhotoImage(file=relative_to_assets("pesquisa.png"))

            self.pesquisa_caixa = tk.Entry(self.motorista_frame, bg='orange', fg="white", width=20, font=("Arial", 14))
            self.pesquisa_caixa.place(relx=0.67, y=15)

            button_adicionar = tk.Button(self.motorista_frame, image=button_ADICIONAR_img, width=144, height=43, command=self.exibir_add)
            button_adicionar.place(relx=0.22, y=525)

            button_remover = tk.Button(self.motorista_frame, image=button_REMOVER_img, width=144, height=43, command=self.remover_motorista_db)
            button_remover.place(relx=0.42, y=525)
            
            button_editar = tk.Button(self.motorista_frame, image=button_EDITAR_img, width=144, height=43, command=self.exibir_edit)
            button_editar.place(relx=0.62, y=525)
            
            button_atualiza = tk.Button(self.motorista_frame, image=button_ATUALIZA_img, width=51.01, height=43.73, command=self.exibir_lista)
            button_atualiza.place(relx=0.91, y=525)

            button_pesquisa = tk.Button(self.motorista_frame, image=button_PESQUISA_img, width=42, height=33.81, command=self.pesquisa_db)
            button_pesquisa.place(relx=0.92, y=7)
            
            button_adicionar.image = button_ADICIONAR_img
            button_remover.image = button_REMOVER_img
            button_editar.image = button_EDITAR_img
            button_atualiza.image = button_ATUALIZA_img
            button_pesquisa.image = button_PESQUISA_img

    def create_lista_form_motorista(self):
        lista_motorista = ttk.Treeview(self.motorista_frame, height=3, columns=("col1", "col2", "col3","col4", "col5","col6","col7"), selectmode='extended')
        lista_motorista.heading("#0", text="")
        lista_motorista.heading("#1",text= "ID")
        lista_motorista.heading("#2",text= "NOME")
        lista_motorista.heading("#3",text= "GUINCHO")
        lista_motorista.heading("#4",text= "STATUS")
        lista_motorista.heading("#5",text= "CIDADE")
        lista_motorista.heading("#6",text= "PLACA")
        lista_motorista.heading("#7",text= "CEP")

        lista_motorista.column("#0", width=1)
        lista_motorista.column("#1", width=30)
        lista_motorista.column("#2", width=200)
        lista_motorista.column("#3", width=200)
        lista_motorista.column("#4", width=30, anchor='center')
        lista_motorista.column("#5", width=180, anchor='center')
        lista_motorista.column("#6", width=30)
        lista_motorista.column("#7", width=30)


        lista_motorista.place(relx=0, relwidth=0.97, rely=0.1, relheight=0.77)
        scroll_lista = tk.Scrollbar(self.motorista_frame, orient='vertical', command=lista_motorista.yview)
        lista_motorista.configure(yscroll=scroll_lista.set)
        scroll_lista.place(relx=0.98, rely=0.1, relheight=0.77)

        return lista_motorista
    
    def exibir_lista(self):
        conexao = create_connection()
        cursor = conexao.cursor()
        
        try:
            self.lista_motorista.delete(*self.lista_motorista.get_children())
            cursor.execute("""
    SELECT 
    m.id_motorista AS 'ID Motorista', 
    m.nome_motorista AS 'Nome Motorista', 
    c.fabricante_modelo AS 'Fabricante Modelo', 
    m.status_motorista AS 'Status Motorista', 
    ci.Nome AS 'Nome da Cidade', 
    c.placa AS 'Placa',
    m.cep_motorista AS 'CEP'
FROM 
    motorista m
LEFT JOIN 
    caminhao c ON m.guincho = c.placa
LEFT JOIN 
    cidade ci ON m.cep_motorista = ci.CEP;; """)

            
            lista = cursor.fetchall()
            for item in lista:
                self.lista_motorista.insert('', 'end', values=item)
        finally:
            cursor.close()
            conexao.close()

    def pesquisa_db(self):
        conexao = create_connection()
        cursor = conexao.cursor()
        try:
            pesquisa = self.pesquisa_caixa.get()
            if pesquisa:
                self.lista_motorista.delete(*self.lista_motorista.get_children())
                comando_pesquisar = """SELECT ID_MOTORISTA, NOME_MOTORISTA, GUINCHO, STATUS_MOTORISTA, CEP_MOTORISTA FROM MOTORISTA WHERE NOME_MOTORISTA LIKE %s ORDER BY ID_MOTORISTA ASC"""
                cursor.execute(comando_pesquisar, ('%' + pesquisa + '%',))
                lista = cursor.fetchall()
                for item in lista:
                    self.lista_motorista.insert('', 'end', values=item)
        finally:
            cursor.close()
            conexao.close()
    def exibir_add(self):
        add_window = tk.Toplevel(self.root)
        MotoristaAdd(add_window)
        
        

    def exibir_edit(self):
        add_window = tk.Toplevel(self.root)
        MotoristaEdit(add_window, self.exibir_lista)        

    def remover_motorista_db(self):
        selected_items = self.lista_motorista.selection()  
        
        if not selected_items:
            msb.showwarning("Alert", "Selecione um item para remover")
            return
        if msb.askyesno("Confirmar", "Você tem certeza que deseja apagar este motorista?"):
            conexao = create_connection()
            cursor = conexao.cursor()

            try:
                for item_id in selected_items:
                    item = self.lista_motorista.item(item_id)
                    id_motorista = item['values'][0]  
                    guincho_placa = item['values'][5] 
                    



                    comando_update_motorista = """UPDATE caminhao 
                                                    SET status = 'Disponivel' 
                                                    WHERE PLACA = %s"""
                    cursor.execute(comando_update_motorista, (guincho_placa,))

                    comando_delete = "DELETE FROM MOTORISTA WHERE ID_MOTORISTA = %s"
                    cursor.execute(comando_delete, (id_motorista,))
                    


                    conexao.commit()
                conexao.commit()
            finally:
                cursor.close()
                conexao.close()
            
            self.exibir_lista()
    
    def SelecionarItem(self):   
        selected_items = self.lista_motorista.selection()
        global placa_selecionar 
        placa_selecionar ="null"
        for item_id in selected_items:
                item = self.lista_motorista.item(item_id)
                placa_selecionar = item['values'][0]
        global placa1
        placa1 = "null"
        for item_id in selected_items:
                item = self.lista_motorista.item(item_id)
                placa1 = item['values'][5]

        global cep_motorista
        cep_motorista = "null"
        for item_id in selected_items:
                item = self.lista_motorista.item(item_id)
                cep_motorista = item['values'][6]
                
        global nome_motorista
        nome_motorista = "null"
        for item_id in selected_items:
                item = self.lista_motorista.item(item_id)
                nome_motorista = item['values'][1]


    def exibir_edit(self):
        self.SelecionarItem()
        add_window = tk.Toplevel(self.root)
        MotoristaEdit(add_window, self.exibir_lista)

class MotoristaAdd:
    def __init__(self, root):
        self.root = root
        self.motorista_frame_add = tk.Frame(root, bg='#3A3A3A', width=1000, height=550)
        root.resizable(False, False)
        self.motorista_frame_add.pack()
        self.create_inputs_add()
        self.mostracaminhao()
        
        
    def mostracaminhao(self):
        TabelasFormCaminhao(self.root)
        self.label_tabelas.config(text="CAMINHÕES")
        
    def mostracidade(self): 
        tabelasFormCIDADE(self.root)
        self.label_tabelas.config(text="CIDADES")
        
        
    def create_inputs_add(self):
        button_aplicar_img = tk.PhotoImage(file=relative_to_assets("APLICAR.png"))
        button_limpa_img = tk.PhotoImage(file=relative_to_assets("LIMPAR.png"))
        button_pesquisa_c = tk.PhotoImage(file=relative_to_assets("cities.png"))
        button_pesquisa_t = tk.PhotoImage(file=relative_to_assets("truck.png"))
        button_img_copy = tk.PhotoImage(file=relative_to_assets("copy.png"))
        img_background = tk.PhotoImage(file=relative_to_assets("image_8.png"))
        
        tk.Label(self.motorista_frame_add, text="ADICIONAR MOTORISTAS", bg='#3A3A3A', fg='white', font=("Arial", 17)).place(relx=0.16, rely=0.095, anchor='center')

        tk.Label(self.motorista_frame_add, text="NOME", bg='#3A3A3A', fg='white', font=("Arial", 13)).place(relx=0.15, rely=0.25, anchor='center')
        self.entry_nome = tk.Entry(self.motorista_frame_add, bg='orange', width=20, font=("Arial", 12))
        self.entry_nome.place(relx=0.15, rely=0.3, anchor='center')


        tk.Label(self.motorista_frame_add, text="PLACA DO CAMINHÃO", bg='#3A3A3A', fg='white', font=("Arial", 13)).place(relx=0.15, rely=0.4, anchor='center')
        self.entry_placa = tk.Entry(self.motorista_frame_add, bg='orange', width=20, font=("Arial", 12))
        self.entry_placa.place(relx=0.15, rely=0.45, anchor='center')

        tk.Label(self.motorista_frame_add, text="CEP DO MOTORISTA", bg='#3A3A3A', fg='white', font=("Arial", 13)).place(relx=0.15, rely=0.55, anchor='center')
        self.entry_cep = tk.Entry(self.motorista_frame_add, bg='orange', width=20, font=("Arial", 12))
        self.entry_cep.place(relx=0.15, rely=0.6, anchor='center')
        
        button_aplicar = tk.Button(self.motorista_frame_add, image=button_aplicar_img, bg='#3A3A3A', borderwidth=0, width=122, height=33.64, command=self.add_motorista_db)
        button_aplicar.place(relx=0.08, rely=0.87, anchor='center')
        
        button_copiar_cidade = tk.Button(self.motorista_frame_add, image=button_img_copy, bg='#3A3A3A', borderwidth=0, width=34.01, height=23.34, command=self.copiar_cep)
        button_copiar_cidade.place(relx=0.225, rely=0.6, anchor='center')

        button_copiar_caminhao = tk.Button(self.motorista_frame_add, image=button_img_copy, bg='#3A3A3A', borderwidth=0, width=34.01, height=23.34, command=self.copiar_caminhao)
        button_copiar_caminhao.place(relx=0.225, rely=0.45, anchor='center')

        button_limpar = tk.Button(self.motorista_frame_add, image=button_limpa_img, bg='#3A3A3A', borderwidth=0, width=122, height=33.64, command=self.apagar_campo)
        button_limpar.place(relx=0.22, rely=0.87, anchor='center')
        
        button_pesquisa_caminhao = tk.Button(self.motorista_frame_add, image=button_pesquisa_t, borderwidth=0, bg=("#3A3A3A"), width=42, height=33.81,command=lambda:self.mostracaminhao())
        button_pesquisa_caminhao.place(relx=0.85, rely=0.10)

        button_pesquisa_cpf = tk.Button(self.motorista_frame_add, image=button_pesquisa_c, borderwidth=0, bg=("#3A3A3A"), width=42, height=33.81, command=lambda:self.mostracidade())
        button_pesquisa_cpf.place(relx=0.906, rely=0.10)

        self.label_tabelas = tk.Label(self.motorista_frame_add, text="CAMINHÕES", bg='#3A3A3A', fg='white', font=("Arial", 20))
        self.label_tabelas.place(relx=0.65, rely=0.12, anchor='center')        
        
        image_label = tk.Label(self.motorista_frame_add, image=img_background, bg='#3A3A3A')        
        image_label.place(x=645, y=310, anchor='center')
        
        
        button_aplicar.image = button_aplicar_img
        button_limpar.image = button_limpa_img
        image_label.image =img_background
        button_pesquisa_cpf.image = button_pesquisa_c
        button_pesquisa_caminhao.image = button_pesquisa_t
        button_copiar_caminhao.image = button_img_copy
        button_copiar_cidade.image = button_img_copy

    
    def copiar_caminhao(self):
            self.entry_placa.delete(0, tk.END)
            placa_selecionada = obtervariavel()
            self.entry_placa.insert(tk.END, placa_selecionada)  
    
    def copiar_cep(self):
        self.entry_cep.delete(0, tk.END)
        cep_selecionado = obtercep()
        self.entry_cep.insert(tk.END, cep_selecionado)


    def add_motorista_db(self):
        conexao = create_connection()
        cursor = conexao.cursor()
        nome = self.entry_nome.get()
        cep = self.entry_cep.get()
        placa = self.entry_placa.get()
        
        
        if placa == "0" and cep =="0":
            msb.showwarning("Alert", "Operação invalida")      
        else:
            try:
                if nome and cep and placa:  
                    comando_insert = "INSERT INTO MOTORISTA (NOME_MOTORISTA, GUINCHO, STATUS_MOTORISTA, CEP_MOTORISTA) VALUES (%s, %s, %s, %s)"
                    cursor.execute(comando_insert, (nome, placa, "D", cep))
                    conexao.commit()

                    comando_update = "UPDATE CAMINHAO SET STATUS = 'Indisponível' WHERE PLACA = %s"  
                    cursor.execute(comando_update, (placa,))
                    conexao.commit()

                    self.root.destroy()
                else:
                    msb.showwarning("Alert", "Preencha todos os campos")

            except Exception as e:  
                msb.showerror("Error", str(e))
            finally:
                cursor.close()
                conexao.close()

    def apagar_campo(self):
        self.entry_nome.delete(0, tk.END)
        self.entry_placa.delete(0, tk.END)
        self.entry_cep.delete(0, tk.END)
        

class MotoristaEdit:
    def __init__(self, root, refresh_list_callback):
        self.root = root
        self.refresh_list_callback = refresh_list_callback
        self.motorista_frame_edit = tk.Frame(root, bg='#3A3A3A',width=1000, height=550)
        root.resizable(False, False)
        self.motorista_frame_edit.pack()
        self.create_inputs_edit()
        self.mostracaminhao()

          
    def mostracaminhao(self):
        TabelasFormCaminhao(self.root)
        self.label_tabelas.config(text="CAMINHÕES")
        
    def mostracidade(self): 
        tabelasFormCIDADE(self.root)
        self.label_tabelas.config(text="CIDADES")
        
        
    def create_inputs_edit(self):
        button_aplicar_img = tk.PhotoImage(file=relative_to_assets("APLICAR.png"))
        button_limpa_img = tk.PhotoImage(file=relative_to_assets("LIMPAR.png"))
        button_pesquisa_c = tk.PhotoImage(file=relative_to_assets("cities.png"))
        button_pesquisa_t = tk.PhotoImage(file=relative_to_assets("truck.png"))
        button_img_copy = tk.PhotoImage(file=relative_to_assets("copy.png"))
        img_background = tk.PhotoImage(file=relative_to_assets("image_8.png"))
        
        tk.Label(self.motorista_frame_edit, text="EDITAR MOTORISTAS", bg='#3A3A3A', fg='white', font=("Arial", 17)).place(relx=0.16, rely=0.095, anchor='center')

        tk.Label(self.motorista_frame_edit, text="ID", bg='#3A3A3A', fg='white', font=("Arial", 13)).place(relx=0.15, rely=0.20, anchor='center')
        self.entry_id = tk.Entry(self.motorista_frame_edit, bg='orange', width=20, font=("Arial", 12))
        if placa_selecionar != "null":
            self.entry_id.insert(0, placa_selecionar)  
        self.entry_id.place(relx=0.15, rely=0.25, anchor='center')

        tk.Label(self.motorista_frame_edit, text="NOME", bg='#3A3A3A', fg='white', font=("Arial", 13)).place(relx=0.15, rely=0.32, anchor='center')
        self.entry_nome = tk.Entry(self.motorista_frame_edit, bg='orange', width=20, font=("Arial", 12))
        if nome_motorista != "null":
            self.entry_nome.insert(1, nome_motorista)
        self.entry_nome.place(relx=0.15, rely=0.37, anchor='center')

        tk.Label(self.motorista_frame_edit, text="PLACA DO CAMINHÃO", bg='#3A3A3A', fg='white', font=("Arial", 13)).place(relx=0.15, rely=0.45, anchor='center')
        self.entry_placa = tk.Entry(self.motorista_frame_edit, bg='orange', width=20, font=("Arial", 12))
        # self.entry_placa.place(relx=0.15, rely=0.5, anchor='center')
        if placa1 != "null":
            self.entry_placa.insert(5, placa1)  
        self.entry_placa.place(relx=0.15, rely=0.5, anchor='center')

        tk.Label(self.motorista_frame_edit, text="CEP DO MOTORISTA", bg='#3A3A3A', fg='white', font=("Arial", 13)).place(relx=0.15, rely=0.60, anchor='center')
        self.entry_cep = tk.Entry(self.motorista_frame_edit, bg='orange', width=20, font=("Arial", 12))
        if cep_motorista != "null":
            self.entry_cep.insert(6, cep_motorista)  
        self.entry_cep.place(relx=0.15, rely=0.65, anchor='center')
        
        button_aplicar = tk.Button(self.motorista_frame_edit, image=button_aplicar_img, bg='#3A3A3A', borderwidth=0, width=122, height=33.64, command=self.edit_motorista_db)
        button_aplicar.place(relx=0.08, rely=0.87, anchor='center')
        
        button_copiar_cidade = tk.Button(self.motorista_frame_edit, image=button_img_copy, bg='#3A3A3A', borderwidth=0, width=34.01, height=23.34, command=self.copiar_cep)
        button_copiar_cidade.place(relx=0.225, rely=0.65, anchor='center')

        button_copiar_caminhao = tk.Button(self.motorista_frame_edit, image=button_img_copy, bg='#3A3A3A', borderwidth=0, width=34.01, height=23.34, command=self.copiar_caminhao)
        button_copiar_caminhao.place(relx=0.225, rely=0.5, anchor='center')

        button_limpar = tk.Button(self.motorista_frame_edit, image=button_limpa_img, bg='#3A3A3A', borderwidth=0, width=122, height=33.64, command=self.apagar_campo)
        button_limpar.place(relx=0.22, rely=0.87, anchor='center')
        
        button_pesquisa_caminhao = tk.Button(self.motorista_frame_edit, image=button_pesquisa_t, borderwidth=0, bg=("#3A3A3A"), width=42, height=33.81,command=lambda:self.mostracaminhao())
        button_pesquisa_caminhao.place(relx=0.85, rely=0.10)

        button_pesquisa_cpf = tk.Button(self.motorista_frame_edit, image=button_pesquisa_c, borderwidth=0, bg=("#3A3A3A"), width=42, height=33.81, command=lambda:self.mostracidade())
        button_pesquisa_cpf.place(relx=0.906, rely=0.10)

        self.label_tabelas = tk.Label(self.motorista_frame_edit, text="CAMINHÕES", bg='#3A3A3A', fg='white', font=("Arial", 20))
        self.label_tabelas.place(relx=0.65, rely=0.12, anchor='center')        
        
        image_label = tk.Label(self.motorista_frame_edit, image=img_background, bg='#3A3A3A')        
        image_label.place(x=645, y=310, anchor='center')
        
        
        button_aplicar.image = button_aplicar_img
        button_limpar.image = button_limpa_img
        image_label.image =img_background
        button_pesquisa_cpf.image = button_pesquisa_c
        button_pesquisa_caminhao.image = button_pesquisa_t
        button_copiar_caminhao.image = button_img_copy
        button_copiar_cidade.image = button_img_copy

    
    def copiar_caminhao(self):
            self.entry_placa.delete(0, tk.END)
            placa_selecionada = obtervariavel()
            self.entry_placa.insert(tk.END, placa_selecionada)  
    
    def copiar_cep(self):
        self.entry_cep.delete(0, tk.END)
        cep_selecionado = obtercep()
        self.entry_cep.insert(tk.END, cep_selecionado)     

    def edit_motorista_db(self):
        conexao = create_connection()
        cursor = conexao.cursor()
        id = self.entry_id.get()
        nome = self.entry_nome.get()
        cep = self.entry_cep.get()
        placa = self.entry_placa.get()
        
        
        
        if placa == "0" and cep =="0" :
            msb.showwarning("Alert", "Operação invalida")      
        else:
            try:
                if id and nome and cep and placa: 

                    comando = "UPDATE MOTORISTA SET nome_motorista = %s, cep_motorista = %s, guincho =%s WHERE id_motorista = %s" 
                    cursor.execute(comando, (nome, cep, placa, id))
                    
                    conexao.commit()
                    comando_update = "UPDATE CAMINHAO SET STATUS = 'Disponível' WHERE PLACA = %s"  
                    cursor.execute(comando_update, (placa1,))
                    comando_update = "UPDATE CAMINHAO SET STATUS = 'Indisponível' WHERE PLACA = %s"  
                    cursor.execute(comando_update, (placa,))
                    
                    conexao.commit()
                    self.root.destroy()
                else:
                    msb.showwarning("Alert", "Preencha todos os campos")

            except Exception as e:  
                msb.showerror("Error", str(e))
            finally:
                cursor.close()
                conexao.close()

    def apagar_campo(self):
        self.entry_id.delete(0, tk.END)
        self.entry_nome.delete(0, tk.END)
        self.entry_placa.delete(0, tk.END)
        self.entry_cep.delete(0, tk.END)