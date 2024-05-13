import mysql.connector #Biblioteca para conexão com banco de dados  
import customtkinter as ctk #Importando a biblioteca grafica
import conexaoDB
from tkinter import Frame
from customtkinter import CTkCanvas, CTkLabel, CTkEntry, CTkButton
from PIL import ImageTk, Image
import conexaoDB

        
#Configuração da tela
janela_principal = ctk.CTk() #Criando a janela
janela_principal._set_appearance_mode("System") #Deixando o tema de acordo com sistema 
janela_principal.geometry("500x500") #Definindo o tamanho inicial da tela
janela_principal.title("Login") #Definindo o título da janela
janela_principal.maxsize(width=500, height=500) #Definindo a resposividade da janela (Não responsivo)
janela_principal.minsize(width=500, height=500) #Definindo a resposividade da janela (Não responsivo)


#Função
def create_gradient(canvas, x1, y1, x2, y2, start_color, end_color):
    # Desenha um retângulo preenchido com um gradiente linear
    canvas.create_rectangle(x1, y1, x2, y2, fill="", outline="")
    for i in range(y1, y2):
        # Calcula a cor intermediária entre start_color e end_color
        r = int(start_color[0] + (end_color[0] - start_color[0]) * (i - y1) / (y2 - y1))
        g = int(start_color[1] + (end_color[1] - start_color[1]) * (i - y1) / (y2 - y1))
        b = int(start_color[2] + (end_color[2] - start_color[2]) * (i - y1) / (y2 - y1))
        color = "#%02x%02x%02x" % (r, g, b)
        # Desenha uma linha horizontal preenchida com a cor intermediária
        canvas.create_line(x1, i, x2, i, fill=color)
        
#Imagens
imagem = ImageTk.PhotoImage(Image.open("Imagens/Logo_tela_de_login.png"))
fundo_trans= ImageTk.PhotoImage(Image.open("Imagens/trasnparente.png"))

#Cores
start_color = (140, 82, 255)  
end_color = (255, 145, 77)  

#Canvas
cor_de_fundo = ctk.CTkCanvas(janela_principal,width=500, height=500)
create_gradient(cor_de_fundo, 0, 0, 500, 500, start_color, end_color)
cor_de_fundo.pack()

#Tela

container = Frame(janela_principal,width=500, height=500, imagem=imagem)
container.place(x=120,y=30)

rightframe = Frame(container, width=250, height=500, relief="raise")
rightframe.pack(side="right")

espacamento = Frame(rightframe)
espacamento.pack(pady=30)

label_usuario = ctk.CTkLabel(rightframe, width=250, height=50, text="Usuario")
label_usuario.pack(pady=10)

input_usuario = ctk.CTkEntry(rightframe, width=250, height=50)
input_usuario.pack(pady=10)

label_senha = ctk.CTkLabel(rightframe, width=250, height=50, text="Senha")
label_senha.pack(pady=10)

input_senha = ctk.CTkEntry(rightframe, width=250, height=50)
input_senha.pack(pady=10)

button_entrar = ctk.CTkButton(rightframe, text="Entrar!",fg_color="black") 
button_entrar.pack(padx=10, pady=10)

leftframe = Frame(container, width=250, height=500, relief="raise")
leftframe.pack(side="left")

label_imagem = ctk.CTkLabel(leftframe,text="")
label_imagem.pack()

janela_principal.mainloop()#Final da janela
