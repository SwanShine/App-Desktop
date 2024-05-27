import mysql.connector #Biblioteca para conexão com banco de dados  
import customtkinter as ctk #Importando a biblioteca grafica
from tkinter import Frame, font, messagebox
from customtkinter import CTkCanvas, CTkLabel, CTkEntry, CTkButton
from PIL import ImageTk, Image
import pyglet
import conexaoDB
import adm



        
#Configuração da tela
janela_principal = ctk.CTk() #Criando a janela
janela_principal._set_appearance_mode("System") #Deixando o tema de acordo com sistema 
janela_principal.geometry("500x500") #Definindo o tamanho inicial da tela
janela_principal.title("Login") #Definindo o título da janela
janela_principal.maxsize(width=500, height=500) #Definindo a resposividade da janela (Não responsivo)
janela_principal.minsize(width=500, height=500) #Definindo a resposividade da janela (Não responsivo)

#Função

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

def validar_login():
    usuario = input_usuario.get()
    senha = input_senha.get()

    if login(usuario, senha):
        messagebox.showinfo("Login", "Login bem-sucedido!")
        return True
    else:
        messagebox.showerror("Login", "Login falhou. Verifique suas credenciais.")
        return False

def tela_administrativa():
    # Definindo a janela administrativa
    tela_administrativa = ctk.CTkToplevel(janela_principal)
    tela_administrativa.title("Janela administrativa")
    tela_administrativa._set_appearance_mode("System")  # Deixando o tema de acordo com sistema
    tela_administrativa.geometry("500x500")  # Definindo o tamanho inicial da tela
    tela_administrativa.maxsize(width=500, height=500)  # Definindo a responsividade da tela (Não responsivo)
    tela_administrativa.minsize(width=500, height=500)  # Definindo a responsividade da tela (Não responsivo)

    rightframe = Frame(tela_administrativa, width=250, height=500, relief="raise", bg="blue")
    rightframe.pack(side="right", fill="both")

    input_usuario_admin = ctk.CTkEntry(rightframe, width=250, height=50)
    input_usuario_admin.pack(pady=10)

    input_senha_admin = ctk.CTkEntry(rightframe, width=250, height=50, show='*')
    input_senha_admin.pack(pady=10)

    leftframe = Frame(tela_administrativa, width=250, height=500, relief="raise", bg="blue")
    leftframe.pack(side="left", fill="both")

    label_usuario = ctk.CTkLabel(leftframe, width=250, height=50, text="Usuário")
    label_usuario.pack(pady=10)

    label_senha = ctk.CTkLabel(leftframe, width=250, height=50, text="Senha")
    label_senha.pack(pady=10)

    button_editar = ctk.CTkButton(tela_administrativa, text="EDITAR", fg_color="black")
    button_editar.place(x=190, y=400)

    button_deletar1 = ctk.CTkButton(tela_administrativa, text="DELETAR", fg_color="black")
    button_deletar1.place(x=40, y=400)

    button_deletar2 = ctk.CTkButton(tela_administrativa, text="DELETAR", fg_color="black")
    button_deletar2.place(x=350, y=400)

def login_valido():
    if validar_login():
        janela_principal.destroy()  # Corrigido para ser um método
        tela_administrativa()
    else:
        messagebox.showerror("Login", "Login falhou. Verifique suas credenciais.")


#Carregando a Imagem
imagem = ImageTk.PhotoImage(Image.open("Imagens/Logo_tela_de_login.png"))

#Carregando a fonte
caminho_fonte = "fontes/Inter-Regular.ttf"
pyglet.font.add_file(caminho_fonte)

#Tela
rightframe = Frame(janela_principal, width=250, height=500, relief="raise",bg="orange")
rightframe.pack(side="right",fill="both")

label_usuario = ctk.CTkLabel(rightframe, width=250, height=50, text="Usuario",font=("Inter-Regular", 16,"italic"))
label_usuario.pack(pady=10)

input_usuario = ctk.CTkEntry(rightframe, width=250, height=50,fg_color="white",font=("Inter-Regular", 16, "italic"))
input_usuario.pack(pady=10)

label_senha = ctk.CTkLabel(rightframe, width=250, height=50, text="Senha",font=("Inter-Regular", 16, "italic"))
label_senha.pack(pady=10)

input_senha = ctk.CTkEntry(rightframe, width=250, height=50,fg_color="white",font=("Inter-Regular", 16, "italic"))
input_senha.pack(pady=10)

button_entrar = ctk.CTkButton(rightframe, text="Entrar!", fg_color="black",command=login_valido,font=("Inter-Regular", 16, "italic")) 
button_entrar.place(x=50,y=330)

leftframe = Frame(janela_principal, width=250, height=500, relief="raise", bg="orange")
leftframe.pack(side="left",fill="both")

label_imagem = CTkLabel(leftframe,width=250,height=250,image=imagem,text="")
label_imagem.place(x=-100,y=-10)

janela_principal.mainloop()

