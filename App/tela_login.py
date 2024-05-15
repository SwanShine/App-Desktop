import mysql.connector #Biblioteca para conexão com banco de dados  
import customtkinter as ctk #Importando a biblioteca grafica
import conexaoDB
from tkinter import Frame
from customtkinter import CTkCanvas, CTkLabel, CTkEntry, CTkButton
from PIL import ImageTk, Image
import pyglet
import conexaoDB


        
#Configuração da tela
janela_principal = ctk.CTk() #Criando a janela
janela_principal._set_appearance_mode("System") #Deixando o tema de acordo com sistema 
janela_principal.geometry("500x500") #Definindo o tamanho inicial da tela
janela_principal.title("Login") #Definindo o título da janela
janela_principal.maxsize(width=500, height=500) #Definindo a resposividade da janela (Não responsivo)
janela_principal.minsize(width=500, height=500) #Definindo a resposividade da janela (Não responsivo)

#Função

def login(conexaoDB,input_usuario,input_senha):
    
     cursor = conn.cursor()
      cursor.execute("SELECT * FROM minha_tabela")


#Carregando a Imagem
 
imagem = ImageTk.PhotoImage(Image.open("Imagens/Logo_tela_de_login.png"))

#Carregando a fonte

#pyglet.font.add_file('fontes/inter.ttf')


#Tela
rightframe = Frame(janela_principal, width=250, height=500, relief="raise",bg="orange")
rightframe.pack(side="right",fill="both")

label_usuario = ctk.CTkLabel(rightframe, width=250, height=50, text="Usuario",font=("Courier", 16, "italic"))
label_usuario.pack(pady=10)

input_usuario = ctk.CTkEntry(rightframe, width=250, height=50,fg_color="white",font=("Courier", 16, "italic"))
input_usuario.pack(pady=10)

label_senha = ctk.CTkLabel(rightframe, width=250, height=50, text="Senha",font=("Courier", 16, "italic"))
label_senha.pack(pady=10)

input_senha = ctk.CTkEntry(rightframe, width=250, height=50,fg_color="white",font=("Courier", 16, "italic"))
input_senha.pack(pady=10)

button_entrar = ctk.CTkButton(rightframe, text="Entrar!", fg_color="black",font=("Courier", 16, "italic")) 
button_entrar.place(x=50,y=330)

leftframe = Frame(janela_principal, width=250, height=500, relief="raise", bg="orange")
leftframe.pack(side="left",fill="both")

label_imagem = CTkLabel(leftframe,width=250,height=250,image=imagem,text="")
label_imagem.place(x=-100,y=-10)

janela_principal.mainloop()