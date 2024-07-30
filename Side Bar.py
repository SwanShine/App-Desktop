import customtkinter as Ctk
from tkinter import PhotoImage

# Dicionário de cores
color = {"white": "#FFFFFF", "orange": "#FF8700"}

# Configuração da janela principal
root = Ctk.CTk()
root.title("Tkinter Navbar")
root.geometry("400x600+850+50")

# Estado do botão de alternância
btnState = False

# Carregamento das imagens dos ícones
navIcon = PhotoImage(file="open.png")
closeIcon = PhotoImage(file="close.png")


# Função para alternar o estado do Navbar
def switch():
    global btnState
    if btnState:
        # Fechar Navbar de forma animada
        for x in range(301):
            navRoot.place(x=-x, y=0)
            root.update_idletasks()
        
        # Resetar as cores dos widgets
        homeLabel.configure(fg_color=color["orange"])
        topFrame.configure(fg_color=color["orange"])
        root.configure(fg_color=color["white"])
        
        # Desligar o botão
        btnState = False
    else:
        # Diminuir a janela principal
        homeLabel.configure(fg_color=color["white"])
        topFrame.configure(fg_color=color["white"])
        root.configure(fg_color=color["white"])
        
        # Abrir Navbar de forma animada
        for x in range(-300, 1):
            navRoot.place(x=x, y=0)
            root.update_idletasks()
        
        # Ligar o botão
        btnState = True

# Barra de navegação superior
topFrame = Ctk.CTkFrame(root, fg_color=color["orange"], height=60)
topFrame.pack(side="top", fill="x")

# Rótulo de cabeçalho
homeLabel = Ctk.CTkLabel(topFrame, text="SwanShine", font=("Bahnschrift", 15), fg_color=color["orange"], text_color=color["white"], height=60, padx=20)
homeLabel.pack(side="right", padx=10)

# Botão de Navbar
navbarBtn = Ctk.CTkButton(topFrame, image=navIcon, fg_color=color["orange"], hover_color=color["orange"], command=switch, width=40, height=40, text="")
navbarBtn.place(x=10, y=10)

# Configuração do frame Navbar
navRoot = Ctk.CTkFrame(root, fg_color=color["white"], height=600, width=300)
navRoot.place(x=-300, y=0)
Ctk.CTkLabel(navRoot, text="", font=("Bahnschrift", 15), fg_color=color["orange"], text_color=color["white"], height=60, width=300).place(x=0, y=0)

# Coordenada y dos widgets da Navbar
y = 80

# Opções no Navbar
options = ["Profile", "Configurações", "Contato", "Sobre"]

# Botões de opções no Navbar
for option in options:
    Ctk.CTkButton(navRoot, text=option, font=("Bahnschrift Light", 15), fg_color=color["orange"], hover_color=color["white"], text_color=color["white"], width=250, height=40).place(x=25, y=y)
    y += 50

# Botão de fechar Navbar
closeBtn = Ctk.CTkButton(navRoot, text="", image=closeIcon, fg_color=color["white"], hover_color=color["white"], command=switch, width=40, height=40)
closeBtn.place(x=250, y=10)

# Iniciar o loop principal da janela
root.mainloop()
