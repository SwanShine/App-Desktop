import mysql.connector
import customtkinter as ctk
from tkinter import Frame, font, messagebox
from customtkinter import CTkCanvas, CTkLabel, CTkEntry, CTkButton, CTkToplevel
from PIL import ImageTk, Image
import pyglet


#Configuração tela 
tela_id = ctk.CTk()
tela_id._set_appearance_mode("System")
tela_id.geometry("500x500")
tela_id.title("Digite o ID do Usuário")
tela_id.maxsize(width=300, height=300)
tela_id.minsize(width=300, height=300)

frame_central = Frame(tela_id,bg="orange",width=300, height=300,relief="raise")
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

#Final da tela
tela_id.mainloop()