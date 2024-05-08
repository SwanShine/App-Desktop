import mysql.connector #Biblioteca para conexão com banco de dados  
import customtkinter as ctk #Importando a biblioteca grafica
from tkinter import Frame
from tkinter import font
import conexaoDB

#Configuração de texto


#Configuração da tela
janela_principal = ctk.CTk() #Criando a janela
janela_principal._set_appearance_mode("System") #Deixando o tema de acordo com sistema 
janela_principal.geometry("500x500") #Definindo o tamanho inicial da tela
janela_principal.title("Usuarios") #Definindo o título da janela
janela_principal.maxsize(width=500, height=500) #Definindo a resposividade da janela (Não responsivo)
janela_principal.minsize(width=500, height=500) #Definindo a resposividade da janela (Não responsivo)


rightframe = Frame(janela_principal, width=250, height=500, relief="raise", bg="blue")
rightframe.pack(side="right",fill="both")
                
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




leftframe =Frame(janela_principal, width=250, height=500, relief="raise", bg="blue")
leftframe.pack(side="left",fill="both")

label_usuario = ctk.CTkLabel(leftframe, width=250, height=50, text="Usuario")
label_usuario.pack(pady=10)

label_senha = ctk.CTkLabel(leftframe, width=250, height=50, text="Senha")
label_senha.pack(pady=10)

label_senha = ctk.CTkLabel(leftframe, width=250, height=50, text="Senha")
label_senha.pack(pady=10)


label_senha = ctk.CTkLabel(leftframe, width=250, height=50, text="Senha")
label_senha.pack(pady=10)

label_senha = ctk.CTkLabel(leftframe, width=250, height=50, text="Senha")
label_senha.pack(pady=10)



button_entrar = ctk.CTkButton(janela_principal, text="Entrar!",fg_color="black") 
button_entrar.place(x=190,y=400)



janela_principal.mainloop()#Final da janela