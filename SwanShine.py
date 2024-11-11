import tkinter as tk
from tkinter import Frame, PhotoImage, messagebox, ttk
import mysql.connector
from mysql.connector import Error
import customtkinter as Ctk
from customtkinter import CTkCanvas, CTkLabel, CTkEntry, CTkButton, CTkToplevel
from customtkinter import *
import PIL
from PIL import Image
import pyglet
import webbrowser

#Funções para fazer Login
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

        return cursor.fetchone() is not None

    except mysql.connector.Error as erro:
        print("Erro ao conectar ao MySQL:", erro)
        return False

    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

# Função para validar login e mostrar mensagem
def validar_login(modo='messagebox'):
    usuario = input_usuario.get()
    senha = input_senha.get()

    sucesso = login(usuario, senha)
    if sucesso:
        if modo == 'messagebox':
            messagebox.showinfo("Login", "Login bem-sucedido!")
        elif modo == 'print':
            print("Login bem-sucedido!")
    else:
        if modo == 'messagebox':
            messagebox.showerror("Login", "Login falhou. Verifique suas credenciais.")
        elif modo == 'print':
            print("Login falhou. Verifique suas credenciais.")
    return sucesso

# Função para validar o login e abrir a tela administrativa
def login_valido_tela_selecionar_usuario():
    usuario = input_usuario.get()
    senha = input_senha.get()

    try:
        if login(usuario, senha):  # Verifica se o login é válido
            tela_login.withdraw()  # Fecha a tela de login
            menu_inicial()  # Abre o menu inicial
        else:
            messagebox.showerror("Login", "Login falhou. Verifique suas credenciais.")
            initialize_window()
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
    finally:
        # Qualquer limpeza ou operação adicional necessária
        pass

#funções de reinicialização das telas
def initialize_window():
    # Limpa a janela antes de reinicializá-la
    for widget in menu_inicial.winfo_children():
        widget.destroy()
        


def fechar_profile():
    global janela_profile
    if janela_profile is not None:
        janela_profile.destroy()
        janela_profile = None
    
def switch_theme():
    global current_theme
    if current_theme == colors_light:
        Ctk.set_appearance_mode("dark")
        theme_button.configure(text="Tema Claro")
        current_theme = colors_dark
    else:
        Ctk.set_appearance_mode("light")
        theme_button.configure(text="Tema Escuro")
        current_theme = colors_light
    
    update_ui()  # Atualiza a interface com o novo tema

# Definindo Cores e temas
colors_light = {
    "background": "#FFFFFF",       # Branco
    "foreground": "#000000",       # Preto
    "accent": "#FF8700",           # Laranja Principal
    "button_color": "#FFB347",      # Laranja Claro para Botões
    "highlight": "#FF8C00",         # Laranja Escuro para Destaques
    "border_color": "#FFA500"       # Laranja Médio para Bordas
}

colors_dark = {
    "background": "#2E2E2E",        # Cinza Escuro
    "foreground": "#FFFFFF",        # Branco
    "accent": "#FF8700",            # Laranja Principal
    "button_color": "#FFB347",       # Laranja Claro para Botões
    "highlight": "#FF8C00",          # Laranja Escuro para Destaques
    "border_color": "#FFA500"        # Laranja Médio para Bordas
}

current_theme = colors_light  # Tema inicial
btnState = False

# Atualizar a interface
def update_ui():
    homeLabel.configure(fg_color=current_theme["background"], text_color=current_theme["foreground"])
    topFrame.configure(fg_color=current_theme["background"])
    menu_inicial.configure(fg_color=current_theme["background"])

# Atualizar a interface quando a Navbar estiver fechada
def update_ui_for_navbar_closed():
    update_ui()
    global btnState
    btnState = False

# Atualizar a interface quando a Navbar estiver aberta
def update_ui_for_navbar_open():
    update_ui()
    global btnState
    btnState = True

# Função para alterar a cor de fundo dos botões quando o mouse passa sobre eles
def on_enter(button):
    button.configure(fg_color=current_theme["accent"])

def on_leave(button):
    button.configure(fg_color=current_theme["button_color"])

# Função para alternar o estado da Navbar
def switch():
    global btnState
    if btnState:
        close_animation(-300)
    else:
        open_animation(0)

# Função para animar a abertura da Navbar
def open_animation(x):
    if x >= 0:
        navmenu_inicial.place(x=x, y=0)
        update_ui_for_navbar_open()
    else:
        navmenu_inicial.place(x=x, y=0)
        menu_inicial.after(5, open_animation, x + 5)  # Ajuste o intervalo e o deslocamento

# Função para animar o fechamento da Navbar
def close_animation(x):
    if x <= -300:
        navmenu_inicial.place(x=x, y=0)
        update_ui_for_navbar_closed()
    else:
        navmenu_inicial.place(x=x, y=0)
        menu_inicial.after(5, close_animation, x - 5)  # Ajuste o intervalo e o deslocamento

# Variáveis globais para rastrear janelas abertas
janela_profile = None
janela_configuracoes = None
janela_contato = None
janela_sobre = None
menu_inicial = None

        
def open_configuracoes():
    global theme_button
    global janela_configuracoes

    def fechar_config():
        janela_configuracoes.destroy()

    if janela_configuracoes is None or not janela_configuracoes.winfo_exists():
        janela_configuracoes = Ctk.CTkToplevel(menu_inicial)
        janela_configuracoes.title("Configurações")
        janela_configuracoes.geometry("400x300")

        Ctk.CTkLabel(janela_configuracoes, text="Configurações",font=("Bahnschrift", 15)).pack(pady=10)

        theme_button = Ctk.CTkButton(janela_configuracoes, text="Tema Escuro",font=("Bahnschrift", 15) ,command=switch_theme)
        theme_button.pack(pady=10)

        close_button = Ctk.CTkButton(janela_configuracoes, text="Fechar",font=("Bahnschrift", 15),command=fechar_config)
        close_button.pack(pady=10)

        # Forçar atualização dos widgets
        menu_inicial.update()

def enviar_email():
    # Abre o cliente de e-mail com o endereço preenchido
    webbrowser.open("mailto:swanshine2023@gmail.com")

def open_contato():
    global janela_contato
    if janela_contato is None or not janela_contato.winfo_exists():
        janela_contato = Ctk.CTkToplevel(menu_inicial)
        janela_contato.geometry("400x300")
        janela_contato.title("Contato")
        
        label_contato = Ctk.CTkLabel(janela_contato,font=("Bahnschrift", 15), text="Email: swanshine2023@gmail.com")
        label_contato.pack(pady=50)
        
        botao_email = Ctk.CTkButton(janela_contato, font=("Bahnschrift", 15),text="Entrar em contato via Email", command=enviar_email)
        botao_email.pack(pady=20)

def open_sobre():
    global janela_sobre
    
    if janela_sobre is None or not janela_sobre.winfo_exists():
        # Criação da janela sobre
        janela_sobre = Ctk.CTkToplevel(menu_inicial)
        janela_sobre.title("Sobre")
        janela_sobre.geometry("500x300")
        
        # Adiciona um título
        titulo_sobre = CTkLabel(janela_sobre, text="VERSÃO EM DESENVOLVIMENTO", font=("Bahnschrift", 15))
        titulo_sobre.pack(pady=(10, 5))
        
        # Adiciona o texto descritivo
        texto_sobre = CTkLabel(janela_sobre, text="Esse App é um exemplo de como funcionaria o sistema de administração SwanShine",font=("Bahnschrift", 15))
        texto_sobre.pack(pady=(0, 5))
        
        texto_sobre1 = CTkLabel(janela_sobre, text="Competências e Capacidades", font=("Bahnschrift", 15))
        texto_sobre1.pack(pady=(0, 5))
        
        texto_sobre2 = CTkLabel(janela_sobre, text="Aplicativo destinado a administradores e gerentes SwanShine",font=("Bahnschrift", 15))
        texto_sobre2.pack(pady=(0, 5))
        
        texto_sobre3 = CTkLabel(janela_sobre, text="Funções: Editar, Excluir e Adicionar",font=("Bahnschrift", 15))
        texto_sobre3.pack(pady=(10, 0))



def sair_menu():
    resposta = messagebox.askyesno("Confirmar Saída", "Você realmente deseja sair?",)
    if resposta:
        menu_inicial.quit()  # Fecha a aplicação

# Função para adicionar a máscara de telefone
def mascara_telefone(event, entry):
    texto = entry.get()
    if event.keysym == 'BackSpace':
        return
    if len(texto) > 15:
        return
    if len(texto) == 1:
        entry.delete(0, tk.END)
        entry.insert(0, f"({texto}")
    elif len(texto) == 3:
        entry.insert(3, ') ')
    elif len(texto) == 9:
        entry.insert(9, '-')

# Função para adicionar a máscara de CPF
def mascara_cpf(event, entry):
    texto = entry.get()
    if event.keysym == 'BackSpace':
        return
    if len(texto) > 14:
        return
    if len(texto) == 3:
        entry.insert(3, '.')
    elif len(texto) == 7:
        entry.insert(7, '.')
    elif len(texto) == 11:
        entry.insert(11, '-')

# Função para alternar a barra lateral
def switch():
    if navmenu_inicial.winfo_x() == 0:
        navmenu_inicial.place(x=-300)
    else:
        navmenu_inicial.place(x=0)
        navmenu_inicial.lift()

# Função para abrir a janela de configurações
def open_configuracoes():
    messagebox.showinfo("Configurações", "Janela de configurações ainda não implementada.")

# Função para abrir a janela de contato
def open_contato():
    messagebox.showinfo("Contato", "Janela de contato ainda não implementada.")

# Função para abrir a janela 'Sobre'
def open_sobre():
    messagebox.showinfo("Sobre", "Janela 'Sobre' ainda não implementada.")

# Função para sair do aplicativo
def sair_menu():
    resposta = messagebox.askquestion("Sair", "Você tem certeza que deseja sair?")
    if resposta == "yes":
        janela_inicial.quit()

# Função principal para criar o menu inicial
def menu_inicial():
    global janela_inicial, navmenu_inicial, topFrame, homeLabel, theme_button, navIcon, closeIcon, current_theme, combo_tabelas, tree, frame_adicionar, entry_id_cliente

    # Tema básico para o aplicativo (pode ser substituído conforme o design)
    current_theme = {
        "background": "#2d2d2d",  # Cor de fundo
        "accent": "#ff6f61",  # Cor de destaque
        "button_color": "#5c5c5c",  # Cor dos botões
        "highlight": "#ff9a8b",  # Cor de hover nos botões
        "foreground": "#ffffff",  # Cor do texto
    }
    
    # Criação da janela principal
    janela_inicial = Ctk.CTkToplevel()
    janela_inicial.title("SwanShine")
    janela_inicial.geometry("1280x720")

    try:
        navIcon = PhotoImage(file="open.png")
        closeIcon = PhotoImage(file="close.png")
    except Exception as e:
        print(f"Erro ao carregar imagens: {e}")
        navIcon = closeIcon = None

    # Barra lateral
    navmenu_inicial = Ctk.CTkFrame(janela_inicial, fg_color=current_theme["background"], height=720, width=300)
    navmenu_inicial.place(x=-300, y=0)

    Ctk.CTkLabel(
        navmenu_inicial,
        text="Menu",
        font=("Bahnschrift", 15),
        fg_color=current_theme["accent"],
        text_color=current_theme["background"],
        height=60,
        width=300
    ).place(x=0, y=0)

    options = ["Configurações", "Contato", "Sobre", "Sair"]
    commands = [open_configuracoes, open_contato, open_sobre, sair_menu]
    y = 80
    for option, command in zip(options, commands):
        button = Ctk.CTkButton(
            navmenu_inicial,
            text=option,
            font=("Bahnschrift", 15),
            fg_color=current_theme["button_color"],
            hover_color=current_theme["highlight"],
            text_color=current_theme["foreground"],
            width=250,
            height=40,
            command=command
        )
        button.place(x=25, y=y)
        y += 50

    if closeIcon:
        closeBtn = Ctk.CTkButton(
            navmenu_inicial,
            text="",
            image=closeIcon,
            fg_color=current_theme["button_color"],
            hover_color=current_theme["highlight"],
            command=switch,
            width=40,
            height=40
        )
        closeBtn.place(x=250, y=10)

    topFrame = Ctk.CTkFrame(janela_inicial, fg_color=current_theme["accent"], height=60)
    topFrame.pack(side="top", fill="x")

    homeLabel = Ctk.CTkLabel(
        topFrame,
        text="SwanShine",
        font=("Bahnschrift", 15),
        fg_color=current_theme["accent"],
        text_color=current_theme["background"],
        height=60,
        padx=20
    )
    homeLabel.pack(side="right", padx=10)

    if navIcon:
        navbarBtn = Ctk.CTkButton(
            topFrame,
            image=navIcon,
            fg_color=current_theme["button_color"],
            hover_color=current_theme["highlight"],
            command=switch,
            width=40,
            height=40,
            text=""
        )
        navbarBtn.place(x=10, y=10)

    # Combo de tabelas
    combo_tabelas = ttk.Combobox(janela_inicial, values=["admins", "clientes", "profissionais"])
    combo_tabelas.pack(pady=10)

    # Treeview
    tree = ttk.Treeview(janela_inicial)
    tree.pack(pady=10, fill="both", expand=True)

    # Frame para a aba de adicionar
    frame_adicionar = Ctk.CTkFrame(janela_inicial)
    frame_adicionar.pack(fill="both", expand=True)

    # Função para conectar com o banco de dados
    def conectar_bd():
        try:
            conn = mysql.connector.connect(
                host="swanshine.cpkoaos0ad68.us-east-2.rds.amazonaws.com",
                user="admin",
                password="gLAHqWkvUoaxwBnm9wKD",
                database="swanshine"
            )
            if conn.is_connected():
                print("Conectado ao banco de dados")
            return conn
        except Error as e:
            print(f"Erro ao conectar ao MySQL: {e}")
            return None

    def atualizar_treeview(colunas):
        tree.delete(*tree.get_children())
        tree["columns"] = colunas
        for col in colunas:
            tree.heading(col, text=col.title(), anchor="center")
            largura = 200 if col.lower() == "nome" else 120
            tree.column(col, anchor='center', width=largura, minwidth=100)

    def exibir_registros():
        conn = conectar_bd()
        if conn:
            try:
                cursor = conn.cursor()
                tabela_selecionada = combo_tabelas.get()
                id_cliente = entry_id_cliente.get() if entry_id_cliente else None  # Verifica se entry_id_cliente foi definido

                query = {
                    "admins": "SELECT Id, Nome, Usuario, Senha FROM admins",
                    "clientes": "SELECT id, nome, endereco, email, cpf, telefone, genero, senha FROM clientes",
                    "profissionais": "SELECT id, nome, email, cpf FROM profissionais"
                }

                colunas = {
                    "admins": ("Id", "Nome", "Usuario", "Senha"),
                    "clientes": ("id", "Nome", "endereco", "email", "cpf", "telefone", "genero", "senha"),
                    "profissionais": ("id", "nome", "email", "cpf")
                }

                atualizar_treeview(colunas[tabela_selecionada])

                if tabela_selecionada == "clientes" and id_cliente:
                    cursor.execute(f"{query[tabela_selecionada]} WHERE id = %s", (id_cliente,))
                else:
                    cursor.execute(query[tabela_selecionada])

                rows = cursor.fetchall()

                # Ajuste para preencher a tabela do começo ao fim
                for row in rows:
                    row_completa = []
                    for idx, campo in enumerate(row):
                        row_completa.append(campo if campo not in (None, '') else "")
                    tree.insert('', 'end', values=row_completa)

            except Error as e:
                print(f"Erro ao executar consulta: {e}")
            finally:
                conn.close()

        # Atualiza a aba de adicionar
        atualizar_aba_adicionar()

    def atualizar_aba_adicionar():
        for widget in frame_adicionar.winfo_children():
            widget.destroy()

        tabela_selecionada = combo_tabelas.get()

        campos_por_tabela = {
            "clientes": [("ID Cliente", "entry_id_cliente"),  # Adicionando o campo de ID do Cliente
                         ("Nome", "entry_nome"), 
                         ("Endereço", "entry_endereco"), 
                         ("Email", "entry_email"), 
                         ("CPF", "entry_cpf"), 
                         ("Telefone", "entry_telefone"), 
                         ("Gênero", "entry_genero"), 
                         ("Senha", "entry_senha")],
            "admins": [("Nome", "entry_nome"), 
                       ("Usuário", "entry_usuario"), 
                       ("Senha", "entry_senha")],
            "profissionais": [("Nome", "entry_nome"), 
                              ("Email", "entry_email"), 
                              ("CPF", "entry_cpf")]
        }

        campos = campos_por_tabela.get(tabela_selecionada, [])

        entradas = {}

        for i, (label_text, entry_name) in enumerate(campos):
            ttk.Label(frame_adicionar, text=label_text).grid(row=i, column=0, padx=5, pady=5, sticky='e')
            largura_entrada = 30 if "endereco" in entry_name else 25
            entrada = ttk.Entry(frame_adicionar, width=largura_entrada)
            entrada.grid(row=i, column=1, padx=5, pady=5, sticky='w')
            entradas[entry_name] = entrada

        # Adicionando a referência do entry_id_cliente
        entry_id_cliente = entradas.get("entry_id_cliente")

        def adicionar_registro():
            tabela_selecionada = combo_tabelas.get()
            # Obter valores dos campos e adicionar no banco de dados
            # A função de adicionar será implementada aqui, dependendo da tabela selecionada.

        # Botão de adicionar
        btn_adicionar = Ctk.CTkButton(frame_adicionar, text="Adicionar", command=adicionar_registro)
        btn_adicionar.grid(row=len(campos), column=0, columnspan=2, pady=10)

# Chamada para inicializar o menu
menu_inicial()




# Tela de Login
def tela_login():
    global tela_login, input_usuario, input_senha
    
import customtkinter as Ctk  # Importa a biblioteca customtkinter
import tkinter as tk  # Importa o tkinter para lidar com a imagem

# Configurando a tela de login
tela_login = Ctk.CTk()
tela_login.title("Login")
tela_login.resizable(False, False)
tela_login.config(bg="white")

# Carregando a imagem com tkinter
dark_image = tk.PhotoImage(file="Logo_tela_de_login.png")

# Label com imagem usando grid ao invés de pack
label = Ctk.CTkLabel(tela_login, image=dark_image, text="")
label.grid(row=0, column=0, pady=20, padx=20)

# Frame de fundo
frame1 = Ctk.CTkFrame(tela_login, fg_color="white", height=350, width=300, corner_radius=20)
frame1.grid(row=0, column=1, padx=40)

# Título "Login"
title = Ctk.CTkLabel(frame1, text="Login", text_color="black", font=("Bahnschrift", 35))
title.grid(row=0, column=0, sticky="nw", pady=30, padx=100)

# Entrada de usuário
input_usuario = Ctk.CTkEntry(frame1, text_color="black", placeholder_text="Username", fg_color="white",
                             placeholder_text_color="black", font=("Bahnschrift", 15), width=200,
                             corner_radius=15, height=45)
input_usuario.grid(row=1, column=0, sticky="nwe", padx=30)

# Entrada de senha
input_senha = Ctk.CTkEntry(frame1, text_color="black", placeholder_text="Password", fg_color="white",
                           placeholder_text_color="black", font=("Bahnschrift", 15), width=200,
                           corner_radius=15, height=45, show="*")
input_senha.grid(row=2, column=0, sticky="nwe", padx=30, pady=20)

# Botão de login
l_btn = Ctk.CTkButton(frame1, text="Login", font=("Bahnschrift", 15), height=40, width=60,
                      fg_color="#FF66C4", cursor="hand2", corner_radius=15, command=login_valido_tela_selecionar_usuario)
l_btn.grid(row=3, column=0, sticky="ne", pady=20, padx=100)

# Iniciar o loop principal
tela_login.mainloop()
