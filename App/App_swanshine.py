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

# Função para abrir a tela administrativa após o login bem-sucedido
def tela_administrativa():
        # Definindo a janela administrativa
        tela_admin = ctk.CTkToplevel(janela_principal)
        tela_admin.title("Janela administrativa")
        tela_admin.geometry("500x500")
        tela_admin.maxsize(width=500, height=500)
        tela_admin.minsize(width=500, height=500)

        rightframe = Frame(tela_admin, width=250, height=500, relief="raise", bg="blue")
        rightframe.pack(side="right", fill="both")

        input_usuario_admin = ctk.CTkEntry(rightframe, width=250, height=50)
        input_usuario_admin.pack(pady=10)

        input_senha_admin = ctk.CTkEntry(rightframe, width=250, height=50, show='*')
        input_senha_admin.pack(pady=10)

        leftframe = Frame(tela_admin, width=250, height=500, relief="raise", bg="blue")
        leftframe.pack(side="left", fill="both")

        label_usuario = ctk.CTkLabel(leftframe, width=250, height=50, text="Usuário")
        label_usuario.pack(pady=10)

        label_senha = ctk.CTkLabel(leftframe, width=250, height=50, text="Senha")
        label_senha.pack(pady=10)

        button_editar = ctk.CTkButton(tela_admin, text="EDITAR", fg_color="black")
        button_editar.place(x=190, y=400)

        button_deletar1 = ctk.CTkButton(tela_admin, text="DELETAR", fg_color="black")
        button_deletar1.place(x=40, y=400)

        button_deletar2 = ctk.CTkButton(tela_admin, text="DELETAR", fg_color="black")
        button_deletar2.place(x=350, y=400)
        
def tela_selecionar_usuario():
    if validar_login():
        # Definindo a janela id
        tela_id = ctk.CTkToplevel(janela_principal)
        tela_id._set_appearance_mode("System")
        tela_id.geometry("300x300")
        tela_id.title("Digite o ID do Usuário")
        tela_id.maxsize(width=300, height=300)
        tela_id.minsize(width=300, height=300)
        
        frame_central = Frame(tela_id,bg="orange")
        frame_central.pack(fill="both")
        # Adicionando o label
        label_id = ctk.CTkLabel(frame_central, text="Digite o ID do Usuário para fazer a consulta de dados")
        label_id.pack(pady=10)

        # Adicionando a entrada de texto
        input_id = ctk.CTkEntry(frame_central)
        input_id.pack(pady=10)
        #Adicionando O Botão
        botao_consultar = CTkButton(frame_central,text="Consultar")
        botao_consultar.pack()



# Função para verificar o login e abrir a tela administrativa
def login_valido():
    try:
        validar_login()
        tela_administrativa()  # Exibe a tela administrativa se o login for válido
    except validar_login:  # Captura exceções que ocorrerem durante a validação do login
        janela_principal.withdraw()  # Fecha a janela de login em caso de falha
        messagebox.showerror("Login", "Login falhou. Verifique suas credenciais.")



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

button_entrar = ctk.CTkButton(rightframe, text="Entrar!", fg_color="black", command=login_valido, font=("Inter-Regular", 16, "italic"))
button_entrar.place(x=50, y=330)

leftframe = Frame(janela_principal, width=250, height=500, relief="raise", bg="orange")
leftframe.pack(side="left", fill="both")

label_imagem = CTkLabel(leftframe, width=250, height=250, image=imagem, text="")
label_imagem.place(x=-100, y=-10)


janela_principal.mainloop()