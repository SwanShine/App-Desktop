import mysql.connector  # Biblioteca para conexão com banco de dados
import customtkinter as ctk  # Importando a biblioteca gráfica
from tkinter import Frame
from tkinter import font
import conexaoDB
import App.App_swanshine as App_swanshine
from tkinter import messagebox



# Configuração da tela
tela_administrativa = ctk.CTk()  # Criando a tela administrativa
tela_administrativa._set_appearance_mode("System")  # Deixando o tema de acordo com sistema
tela_administrativa.geometry("500x500")  # Definindo o tamanho inicial da tela
tela_administrativa.title("Usuários")  # Definindo o título da tela
tela_administrativa.maxsize(width=500, height=500)  # Definindo a responsividade da tela (Não responsivo)
tela_administrativa.minsize(width=500, height=500)  # Definindo a responsividade da tela (Não responsivo)

rightframe = Frame(tela_administrativa, width=250, height=500, relief="raise", bg="blue")
rightframe.pack(side="right", fill="both")

input_usuario = ctk.CTkEntry(rightframe, width=250, height=50)
input_usuario.pack(pady=10)

input_usuario = ctk.CTkEntry(rightframe, width=250, height=50)
input_usuario.pack(pady=10)

input_usuario = ctk.CTkEntry(rightframe, width=250, height=50)
input_usuario.pack(pady=10)

input_usuario = ctk.CTkEntry(rightframe, width=250, height=50)
input_usuario.pack(pady=10)

input_senha = ctk.CTkEntry(rightframe, width=250, height=50)
input_senha.pack(pady=10)

leftframe = Frame(tela_administrativa, width=250, height=500, relief="raise", bg="blue")
leftframe.pack(side="left", fill="both")

label_usuario = ctk.CTkLabel(leftframe, width=250, height=50, text="Usuário")
label_usuario.pack(pady=10)

label_senha = ctk.CTkLabel(leftframe, width=250, height=50, text="Senha")
label_senha.pack(pady=10)

label_senha = ctk.CTkLabel(leftframe, width=250, height=50, text="Senha")
label_senha.pack(pady=10)

label_senha = ctk.CTkLabel(leftframe, width=250, height=50, text="Senha")
label_senha.pack(pady=10)

label_senha = ctk.CTkLabel(leftframe, width=250, height=50, text="Senha")
label_senha.pack(pady=10)

button_editar = ctk.CTkButton(tela_administrativa, text="EDITAR", fg_color="black")
button_editar.place(x=190, y=400)

button_deletar1 = ctk.CTkButton(tela_administrativa, text="DELETAR", fg_color="black")
button_deletar1.place(x=40, y=400)

button_deletar2 = ctk.CTkButton(tela_administrativa, text="DELETAR", fg_color="black")
button_deletar2.place(x=350, y=400)

tela_administrativa.mainloop()  # Final da tela
