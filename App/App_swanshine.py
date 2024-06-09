import mysql.connector
import customtkinter as ctk
from tkinter import Frame, font, messagebox
from customtkinter import CTkCanvas, CTkLabel, CTkEntry, CTkButton, CTkToplevel
from PIL import ImageTk, Image
import pyglet

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
    def fechar_tela_administrativa():
        tela_admin.destroy()
        tela_selecionar_usuario()

    # Definindo a janela administrativa
    tela_admin = ctk.CTkToplevel(janela_principal)
    tela_admin.title("Janela administrativa")
    tela_admin.geometry("500x500")
    tela_admin.maxsize(width=500, height=500)
    tela_admin.minsize(width=500, height=500)

    rightframe = Frame(tela_admin, width=250, height=500, relief="raise", bg="orange")
    rightframe.pack(side="right", fill="both")

    input_cpf = ctk.CTkEntry(rightframe, width=250, height=50)
    input_cpf.pack(pady=10)

    input_email = ctk.CTkEntry(rightframe, width=250, height=50, show='*')
    input_email.pack(pady=10)
    
    input_endereco = ctk.CTkEntry(rightframe, width=250, height=50)
    input_endereco.pack(pady=10)

    input_id= ctk.CTkEntry(rightframe, width=250, height=50, show='*')
    input_id.pack(pady=10)
    
    input_nome = ctk.CTkEntry(rightframe, width=250, height=50)
    input_nome.pack(pady=10)

    input_telefone = ctk.CTkEntry(rightframe, width=250, height=50, show='*')
    input_telefone.pack(pady=10)

    leftframe = Frame(tela_admin, width=250, height=500, relief="raise", bg="orange")
    leftframe.pack(side="left", fill="both")

    label_cpf = ctk.CTkLabel(leftframe, width=250, height=50, text="CPF")
    label_cpf.pack(pady=10)

    label_email = ctk.CTkLabel(leftframe, width=250, height=50, text="Email")
    label_email.pack(pady=10)
    
    label_endereco = ctk.CTkLabel(leftframe, width=250, height=50, text="Endereço")
    label_endereco.pack(pady=10)

    label_id = ctk.CTkLabel(leftframe, width=250, height=50, text="ID")
    label_id.pack(pady=10)
    
    label_nome = ctk.CTkLabel(leftframe, width=250, height=50, text="Nome")
    label_nome.pack(pady=10)

    label_telefone = ctk.CTkLabel(leftframe, width=250, height=50, text="Telefone")
    label_telefone.pack(pady=10)
    

    button_editar = ctk.CTkButton(tela_admin, text="EDITAR", fg_color="black")
    button_editar.place(x=190, y=450)

    button_deletar1 = ctk.CTkButton(tela_admin, text="DELETAR", fg_color="black")
    button_deletar1.place(x=40, y=450)

    button_deletar2 = ctk.CTkButton(tela_admin, text="VOLTAR", fg_color="black", command=fechar_tela_administrativa)
    button_deletar2.place(x=345, y=450)

        
def tela_selecionar_usuario():

    def fechar_tela_id():
        tela_id.destroy()
        janela_principal.deiconify()
        
    def abir_tela_admin():
        tela_administrativa()
        tela_id.withdraw()
    
    tela_id = ctk.CTkToplevel(janela_principal)
    tela_id.title("Consulta de ID")
    tela_id.geometry("300x300")
    tela_id.maxsize(width=300, height=300)
    tela_id.minsize(width=300, height=300)

    label_id = ctk.CTkLabel(tela_id, text="Digite o ID do Usuário para fazer a consulta de dados")
    label_id.pack(pady=10)

    input_id = ctk.CTkEntry(tela_id)
    input_id.pack(pady=10)

    botao_consultar = CTkButton(tela_id, text="Consultar", command=abir_tela_admin)
    botao_consultar.place(x=150, y=90)

 
    botao_voltar = CTkButton(tela_id, text="Voltar", command=fechar_tela_id)
    botao_voltar.place(x=5, y=90)

def consulta_Id(CPF,EMAIL,ENDERECO,ID,NOME,TELEFONE):
    tela_administrativa()
    
    try:
        # Conexão com o banco de dados
        conn = mysql.connector.connect(
            host="swanshine.cpkoaos0ad68.us-east-2.rds.amazonaws.com",
            user="admin",
            password="gLAHqWkvUoaxwBnm9wKD",
            database="swanshine"
        )

        cursor = conn.cursor()

        consulta = "SELECT * FROM clientes WHERE Id = %s "
        dados = (CPF,EMAIL,ENDERECO,ID,NOME,TELEFONE)
        print(CPF,EMAIL,ENDERECO,ID,NOME,TELEFONE)

        cursor.execute(consulta, dados)

        if cursor.fetchone():
            return True
        else:
            return False

    except mysql.connector.Error as erro:
        print("Erro ao conectar ao MySQL:", erro)
        return False

    finally:
        # Garantindo que a conexão com o banco de dados seja sempre fechada
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

    
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
            tela_selecionar_usuario()  # Exibe a tela administrativa se o login for válido
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