import mysql.connector
import customtkinter as ctk
from tkinter import Frame, font, messagebox
from customtkinter import CTkCanvas, CTkLabel, CTkEntry, CTkButton, CTkToplevel
from PIL import ImageTk, Image
import pyglet
import tkinter as tk
from tkinter import ttk

#Configuração da tela
janela_principal = ctk.CTk()
janela_principal._set_appearance_mode("System")
janela_principal.geometry("500x500")
janela_principal.title("Login")
janela_principal.maxsize(width=500, height=500)
janela_principal.minsize(width=500, height=500)

# Função para fazer login
def login(usuario, senha):
    try:
        # Conexão com o banco de dados
        conn = mysql.connector.connect(
            host="swanshine.cpkoaos0ad68.us-east-2.rds.amazonaws.com",
            user="admin",
            password="gLAHqWkvUoaxwBnm9wKD",
            database="swanshine"
        )

        cursor = conn.cursor()

        consulta = "SELECT * FROM admins WHERE Usuario = %s AND Senha = %s"
        dados = (usuario, senha)

        cursor.execute(consulta, dados)

        if cursor.fetchone():
            return True
        else:
            return False

    except mysql.connector.Error as erro:
        print("Erro ao conectar ao MySQL:", erro)
        return False

    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

# Função para validar o login
def validar_login():
    usuario = input_usuario.get()
    senha = input_senha.get()

    if login(usuario, senha):
        messagebox.showinfo("Login", "Login bem-sucedido!")
        return True
    else:
        messagebox.showerror("Login", "Login falhou. Verifique suas credenciais.")
        return False
    
def validar_login_print():
    usuario = input_usuario.get()
    senha = input_senha.get()

    if login(usuario, senha):
        print("Login", "Login bem-sucedido!")
        return True
    else:
        print("Login", "Login falhou. Verifique suas credenciais.")
        return False

# Função para abrir a tela administrativa após o login bem-sucedido
def tela_administrativa():
    
    def conectar_bd():
        try:
            conn = mysql.connector.connect(
                host="swanshine.cpkoaos0ad68.us-east-2.rds.amazonaws.com",
                user="admin",
                password="gLAHqWkvUoaxwBnm9wKD",
                database="swanshine"
            )
            cursor = conn.cursor()
            if conn.is_connected():
                print("Conectado ao banco de dados")
            return conn, cursor
        except mysql.connector.Error as erro:
            print("Erro ao conectar ao MySQL:", erro)
            return None, None

    def exibir_registros():
        conn, cursor = conectar_bd()
        if conn and cursor:
            cursor.execute("SELECT Id_clientes, CPF, Email, Endereço, Nome, Telefone FROM clientes")
            rows = cursor.fetchall()
            for row in tree.get_children():
                tree.delete(row)
            for row in rows:
                tree.insert('', 'end', values=row)
            conn.close()

    def adicionar_registro():
        cpf = entry_cpf.get()
        email = entry_email.get()
        endereco = entry_endereco.get()
        nome = entry_nome.get()
        telefone = entry_telefone.get()
        conn, cursor = conectar_bd()
        if conn and cursor:
            cursor.execute("INSERT INTO clientes (CPF, Email, Endereço, Nome, Telefone) VALUES (%s, %s, %s, %s, %s)", (cpf, email, endereco, nome, telefone))
            conn.commit()
            conn.close()
            exibir_registros()

    def deletar_registro():
        selected_item = tree.selection()
        if selected_item:
            conn, cursor = conectar_bd()
            if conn and cursor:
                try:
                    for item in selected_item:
                        id_registro = tree.item(item, 'values')[0]
                        cursor.execute("DELETE FROM clientes WHERE Id_clientes=%s", (id_registro,))
                        conn.commit()
                        tree.delete(item)
                except mysql.connector.Error as erro:
                    print("Erro ao deletar registro:", erro)
                finally:
                    conn.close()

    def editar_registro():
        selected_item = tree.selection()
        novo_valor = entry_novo_valor.get()
        campo = combo_campos.get()
        if selected_item and novo_valor and campo:
            conn, cursor = conectar_bd()
            if conn and cursor:
                try:
                    for item in selected_item:
                        id_registro = tree.item(item, 'values')[0]
                        cursor.execute(f"UPDATE clientes SET {campo}=%s WHERE Id_clientes=%s", (novo_valor, id_registro))
                        conn.commit()
                        valores_atuais = list(tree.item(item, 'values'))
                        indice_campo = ['Id_clientes', 'CPF', 'Email', 'Endereço', 'Nome', 'Telefone'].index(campo)
                        valores_atuais[indice_campo] = novo_valor
                        tree.item(item, values=valores_atuais)
                except mysql.connector.Error as erro:
                    print("Erro ao editar registro:", erro)
                finally:
                    conn.close()

    def filtrar_por_id_cliente():
        id_cliente = entry_id_cliente.get()
        conn, cursor = conectar_bd()
        if conn and cursor:
            cursor.execute("SELECT Id_clientes, CPF, Email, Endereço, Nome, Telefone FROM clientes WHERE Id_clientes = %s", (id_cliente,))
            rows = cursor.fetchall()
            for row in tree.get_children():
                tree.delete(row)
            for row in rows:
                tree.insert('', 'end', values=row)
            conn.close()
            
    def fechar_jamela_admin():
        janela_admin.withdraw()
        janela_principal.deiconify()

    janela_admin = tk.Toplevel(janela_principal)
    janela_admin.title("Consulta e Edição de Registros")

    frame_input = ttk.Frame(janela_admin)
    frame_input.pack(pady=10)

    label_nome = ttk.Label(frame_input, text="Nome:")
    label_nome.grid(row=0, column=0, padx=5, pady=5, sticky='e')
    entry_nome = ttk.Entry(frame_input, width=30)
    entry_nome.grid(row=0, column=1, padx=5, pady=5)

    label_cpf = ttk.Label(frame_input, text="CPF:")
    label_cpf.grid(row=1, column=0, padx=5, pady=5, sticky='e')
    entry_cpf = ttk.Entry(frame_input, width=30)
    entry_cpf.grid(row=1, column=1, padx=5, pady=5)

    label_email = ttk.Label(frame_input, text="Email:")
    label_email.grid(row=2, column=0, padx=5, pady=5, sticky='e')
    entry_email = ttk.Entry(frame_input, width=30)
    entry_email.grid(row=2, column=1, padx=5, pady=5)

    label_endereco = ttk.Label(frame_input, text="Endereço:")
    label_endereco.grid(row=3, column=0, padx=5, pady=5, sticky='e')
    entry_endereco = ttk.Entry(frame_input, width=30)
    entry_endereco.grid(row=3, column=1, padx=5, pady=5)

    label_telefone = ttk.Label(frame_input, text="Telefone:")
    label_telefone.grid(row=4, column=0, padx=5, pady=5, sticky='e')
    entry_telefone = ttk.Entry(frame_input, width=30)
    entry_telefone.grid(row=4, column=1, padx=5, pady=5)

    label_campos = ttk.Label(frame_input, text="Campo:")
    label_campos.grid(row=5, column=0, padx=5, pady=5, sticky='e')
    campos_disponiveis = ['Id_clientes', 'CPF', 'Email', 'Endereço', 'Nome', 'Telefone']
    combo_campos = ttk.Combobox(frame_input, values=campos_disponiveis, width=27)
    combo_campos.grid(row=5, column=1, padx=5, pady=5)

    label_novo_valor = ttk.Label(frame_input, text="Novo Valor:")
    label_novo_valor.grid(row=6, column=0, padx=5, pady=5, sticky='e')
    entry_novo_valor = ttk.Entry(frame_input, width=30)
    entry_novo_valor.grid(row=6, column=1, padx=5, pady=5)

    label_id_cliente = ttk.Label(frame_input, text="Filtrar por ID Cliente:")
    label_id_cliente.grid(row=7, column=0, padx=5, pady=5, sticky='e')
    entry_id_cliente = ttk.Entry(frame_input, width=10)
    entry_id_cliente.grid(row=7, column=1, padx=5, pady=5)

    btn_adicionar = ttk.Button(frame_input, text="Adicionar", command=adicionar_registro)
    btn_adicionar.grid(row=8, column=1, padx=5, pady=5, sticky='e')

    btn_editar = ttk.Button(janela_admin, text="Editar Campo Selecionado", command=editar_registro)
    btn_editar.pack(pady=5)

    btn_filtrar = ttk.Button(janela_admin, text="Filtrar por ID Cliente", command=filtrar_por_id_cliente)
    btn_filtrar.pack(pady=5)

    tree = ttk.Treeview(janela_admin, columns=('ID', 'CPF', 'Email', 'Endereço', 'Nome', 'Telefone'), show='headings')
    tree.heading('ID', text='ID')
    tree.heading('CPF', text='CPF')
    tree.heading('Email', text='Email')
    tree.heading('Endereço', text='Endereço')
    tree.heading('Nome', text='Nome')
    tree.heading('Telefone', text='Telefone')
    tree.pack()

    btn_atualizar = ttk.Button(janela_admin, text="Atualizar Lista", command=exibir_registros)
    btn_atualizar.pack(pady=10)

    btn_deletar = ttk.Button(janela_admin, text="Deletar Selecionado", command=deletar_registro)
    btn_deletar.pack()
    
    btn_voltar = ttk.Button(janela_admin, text="Voltar", command=fechar_jamela_admin)
    btn_voltar.pack()

    exibir_registros()
############
     
    
# Função para verificar o login e abrir a tela administrativa
def login_valido_tela_adm():
    try:
        
            tela_administrativa()  # Exibe a tela administrativa se o login for válido
    except validar_login:  # Captura exceções que ocorrerem durante a validação do login
        janela_principal.withdraw()  # Fecha a janela de login em caso de falha
        messagebox.showerror("Login", "Login falhou. Verifique suas credenciais.")
    finally:
        if validar_login_print():
            janela_principal.withdraw()
        pass
    
def login_valido_tela_selecionar_usuario():
    try:
        if validar_login():
            tela_administrativa()
    except validar_login:  # Captura exceções que ocorrerem durante a validação do login
        janela_principal.withdraw()  # Fecha a janela de login em caso de falha
        messagebox.showerror("Login", "Login falhou. Verifique suas credenciais.")
    finally:
        if validar_login_print():
            janela_principal.withdraw()
        pass

# Carregando a Imagem
imagem = ImageTk.PhotoImage(Image.open("Imagens/Logo_tela_de_login.png"))

# Carregando a fonte
caminho_fonte = "fontes/Inter-Regular.ttf"
pyglet.font.add_file(caminho_fonte)

# Tela
rightframe = Frame(janela_principal, width=250, height=500, relief="raise", bg="orange")
rightframe.pack(side="right", fill="both")

label_usuario = ctk.CTkLabel(rightframe, width=250, height=50, text="Usuario", font=("Inter-Regular", 16,"italic"))
label_usuario.pack(pady=10)

input_usuario = ctk.CTkEntry(rightframe, width=250, height=50, fg_color="white", font=("Inter-Regular", 16, "italic"))
input_usuario.pack(pady=10)

label_senha = ctk.CTkLabel(rightframe, width=250, height=50, text="Senha", font=("Inter-Regular", 16, "italic"))
label_senha.pack(pady=10)

input_senha = ctk.CTkEntry(rightframe, width=250, height=50, fg_color="white", font=("Inter-Regular", 16, "italic"))
input_senha.pack(pady=10)

button_entrar = ctk.CTkButton(rightframe, text="Entrar!", fg_color="black", command=login_valido_tela_selecionar_usuario, font=("Inter-Regular", 16, "italic"))
button_entrar.place(x=50, y=330)

leftframe = Frame(janela_principal, width=250, height=500, relief="raise", bg="orange")
leftframe.pack(side="left", fill="both")

label_imagem = CTkLabel(leftframe, width=250, height=250, image=imagem, text="")
label_imagem.place(x=-100, y=-10)

janela_principal.mainloop()