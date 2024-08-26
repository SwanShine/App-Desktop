import customtkinter as Ctk
from customtkinter import *
from PIL import Image

tela_login = Ctk.CTk()
tela_login.title("Login")
tela_login.config(bg="white")
tela_login.resizable(False, False)

bg_img = CTkImage(dark_image=Image.open("Logo_tela_de_login.png"), size=(500, 500))

bg_lab = CTkLabel(tela_login, image=bg_img, text="")
bg_lab.grid(row=0, column=0)

frame1 = CTkFrame(tela_login,fg_color="white", bg_color="white", height=350, width=300,corner_radius=20)
frame1.grid(row=0, column=1,padx=40)

title = CTkLabel(frame1,text="Login",text_color="Black",font=("",35,"bold"))
title.grid(row=0,column=0,sticky="nw",pady=30,padx=100)

input_usuario = CTkEntry(frame1,text_color="black", placeholder_text="Username", fg_color="white", placeholder_text_color="black",
                         font=("",16,"bold"), width=200, corner_radius=15, height=45)
input_usuario.grid(row=1,column=0,sticky="nwe",padx=30)

input_senha = CTkEntry(frame1,text_color="black",placeholder_text="Password",fg_color="white",placeholder_text_color="black",
                         font=("",16,"bold"), width=200,corner_radius=15, height=45, show="*")
input_senha.grid(row=2,column=0,sticky="nwe",padx=30,pady=20)


l_btn = CTkButton(frame1,text="Login",font=("",15,"bold"),height=40,width=60,fg_color="#FF66C4",cursor="hand2",
                  corner_radius=15,command=login_valido_tela_selecionar_usuario,)
l_btn.grid(row=3,column=0,sticky="ne",pady=20, padx=100)

tela_login.mainloop()