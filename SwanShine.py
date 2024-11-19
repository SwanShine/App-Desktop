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
import re

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


#####################################################################################################
import mysql.connector
from mysql.connector import Error
import customtkinter as Ctk
from tkinter import ttk, PhotoImage, messagebox
import tkinter as tk

# Variável global para controle de exibição de senha
senha_censurada = True

# Função para conectar ao banco de dados
def conectar_bd():
    try:
        conn = mysql.connector.connect(
            host='swanshine.cpkoaos0ad68.us-east-2.rds.amazonaws.com',
            database='swanshine',
            user='admin',
            password='gLAHqWkvUoaxwBnm9wKD'
        )
        if conn.is_connected():
            return conn
    except Error as e:
        messagebox.showerror("Erro de Conexão", f"Erro ao conectar ao banco de dados: {e}")
        return None

# Função para atualizar o TreeView com os dados
def atualizar_treeview(cursor, rows):
    # Limpar os dados existentes
    for item in tree.get_children():
        tree.delete(item)

    if not rows:
        messagebox.showinfo("Nenhum Registro", "Nenhum registro encontrado.")
        return

    # Atualizar as colunas do TreeView
    colunas = [desc[0] for desc in cursor.description]
    tree.config(columns=colunas)
    for coluna in colunas:
        tree.heading(coluna, text=coluna)
        tree.column(coluna, width=100, anchor="center")

    # Inserir os dados no TreeView
    for row in rows:
        tree.insert('', 'end', values=row)

# Função para exibir registros com filtro de ID
def exibir_registros():
    conn = conectar_bd()
    if conn:
        try:
            cursor = conn.cursor()
            tabela_selecionada = combo_tabelas.get()

            # Obtendo o valor de ID
            id_cliente = entry_id_cliente.get().strip()

            # Construção da query com base no filtro
            query = {
                "admins": f"SELECT Id, Nome, Usuario, {'REPEAT(\'*\', CHAR_LENGTH(Senha)) AS Senha' if senha_censurada else 'Senha'} FROM admins",
                "clientes": f"SELECT id, Nome, endereco, email, cpf, telefone, genero, {'REPEAT(\'*\', CHAR_LENGTH(senha)) AS senha' if senha_censurada else 'senha'} FROM clientes",
                "profissionais": "SELECT id, nome, email, cpf FROM profissionais"
            }

            # Adicionando o filtro por ID, se o ID for informado
            if id_cliente:
                if tabela_selecionada == "admins":
                    query["admins"] += f" WHERE Id = {id_cliente}"
                elif tabela_selecionada == "clientes":
                    query["clientes"] += f" WHERE id = {id_cliente}"
                elif tabela_selecionada == "profissionais":
                    query["profissionais"] += f" WHERE id = {id_cliente}"

            cursor.execute(query[tabela_selecionada])
            rows = cursor.fetchall()
            atualizar_treeview(cursor, rows)
        finally:
            conn.close()

# Função principal para criar o menu inicial
def menu_inicial():
    global menu_inicial, navmenu_inicial, topFrame, homeLabel, theme_button, navIcon, closeIcon
    global combo_tabelas, frame_adicionar, tree, frame_exibir, entry_id_cliente, notebook

    # Função para alternar a exibição da senha
    def alternar_senha():
        global senha_censurada
        senha_censurada = not senha_censurada
        exibir_registros()

    # Criação da janela principal
    menu_inicial = Ctk.CTkToplevel()
    menu_inicial.title("SwanShine")
    menu_inicial.geometry("1280x720")
    menu_inicial.state('zoomed')

    # Carregamento dos ícones para abrir e fechar a barra lateral
    try:
        navIcon = PhotoImage(file="open.png")
        closeIcon = PhotoImage(file="close.png")
    except Exception as e:
        print(f"Erro ao carregar imagens: {e}")
        navIcon = closeIcon = None

    # Cor principal laranja
    main_color = "#ef972f"
    hover_color = "#000000"  # Cor de hover (mais clara)

    # Criação da barra lateral (Navbar)
    navmenu_inicial = Ctk.CTkFrame(menu_inicial, fg_color=main_color, height=720, width=300)
    navmenu_inicial.place(x=-300, y=0)

    # Cabeçalho da barra lateral
    Ctk.CTkLabel(
        navmenu_inicial,
        text="Menu",
        font=("Bahnschrift", 15),
        fg_color=main_color,
        text_color="white",
        height=60,
        width=300
    ).place(x=0, y=0)

    # Opções no Navbar
    options = ["Configurações", "Contato", "Sobre", "Sair"]
    commands = [lambda: print("Configurações"), lambda: print("Contato"), lambda: print("Sobre"), menu_inicial.destroy]

    y = 80  # Posição vertical inicial para os botões
    for option, command in zip(options, commands):
        button = Ctk.CTkButton(
            navmenu_inicial,
            text=option,
            font=("Bahnschrift", 15),
            fg_color=main_color,
            hover_color=hover_color,
            text_color="black",
            width=250,
            height=40,
            command=command
        )
        button.place(x=25, y=y)
        y += 50  # Incremento da posição vertical para o próximo botão

    # Botão para fechar a barra lateral
    closeBtn = Ctk.CTkButton(
        navmenu_inicial,
        text="",
        image=closeIcon,
        fg_color=main_color,
        hover_color=hover_color,
        command=switch,
        width=40,
        height=40
    )
    closeBtn.place(x=250, y=10)

    # Barra superior de navegação
    topFrame = Ctk.CTkFrame(menu_inicial, fg_color=main_color, height=60)
    topFrame.pack(side="top", fill="x")

    # Rótulo do nome da aplicação na barra superior
    homeLabel = Ctk.CTkLabel(
        topFrame,
        text="SwanShine",
        font=("Bahnschrift", 15),
        fg_color=main_color,
        text_color="white",
        height=60,
        padx=20
    )
    homeLabel.pack(side="right", padx=10)

    # Botão de abrir a barra lateral
    navbarBtn = Ctk.CTkButton(
        topFrame,
        image=navIcon,
        fg_color=main_color,
        hover_color=hover_color,
        command=switch,
        width=40,
        height=40,
        text=""
    )
    navbarBtn.place(x=10, y=10)

    # Criando a área de abas (tabs)
    notebook = ttk.Notebook(menu_inicial)
    notebook.pack(pady=10, padx=10, fill='both', expand=True)

    # Abas para navegação
    aba_adicionar = ttk.Frame(notebook)
    aba_editar = ttk.Frame(notebook)
    aba_desativar = ttk.Frame(notebook)

    notebook.add(aba_adicionar, text="Adicionar")
    notebook.add(aba_editar, text="Editar")
    notebook.add(aba_desativar, text="Desativar")

    # Frame de entrada para adicionar, editar e desativar
    frame_input = ttk.Frame(aba_adicionar)
    frame_input.pack(pady=10, padx=10, fill='x')

    ttk.Label(frame_input, text="Selecionar Tabela", font=("Bahnschrift", 15)).grid(row=0, column=0, padx=5, pady=5, sticky='e')
    tabelas_disponiveis = ['admins', 'clientes', 'profissionais']
    combo_tabelas = ttk.Combobox(frame_input, values=tabelas_disponiveis, width=27)
    combo_tabelas.grid(row=0, column=1, padx=5, pady=5)
    combo_tabelas.current(0)

    ttk.Label(frame_input, text="Filtrar por ID").grid(row=1, column=0, padx=5, pady=5, sticky='e')
    entry_id_cliente = ttk.Entry(frame_input, width=30)
    entry_id_cliente.grid(row=1, column=1, padx=5, pady=5)

    button_filtrar = Ctk.CTkButton(
        frame_input,
        text="Filtrar por ID",
        width=20,
        height=30,
        fg_color=main_color,
        hover_color=hover_color,
        command=exibir_registros
    )
    button_filtrar.grid(row=1, column=2, padx=5, pady=5)

    # Frame para exibir a tabela com scrollbar
    frame_exibir = ttk.Frame(aba_adicionar)
    frame_exibir.pack(pady=10, expand=True, fill='both')

    tree_scroll = ttk.Scrollbar(frame_exibir, orient="vertical")
    tree_scroll.pack(side="right", fill="y")

    tree = ttk.Treeview(frame_exibir, columns=[], show='headings', yscrollcommand=tree_scroll.set)
    tree.pack(fill="both", expand=True)

    tree_scroll.config(command=tree.yview)

    # Botão para alternar exibição da senha
    button_alternar_senha = Ctk.CTkButton(
        frame_input,
        text="Exibir/Ocultar Senha",
        width=20,
        height=30,
        fg_color=main_color,
        hover_color=hover_color,
        command=alternar_senha
    )
    button_alternar_senha.grid(row=2, column=1, padx=5, pady=5)

    # Associar a função 'exibir_registros' à mudança de seleção do ComboBox
    combo_tabelas.bind("<<ComboboxSelected>>", lambda event: exibir_registros())

    # Exibir os registros ao iniciar
    exibir_registros()

    # Levanta a barra lateral acima dos outros widgets
    navmenu_inicial.lift()


###############################################################################################

import customtkinter as Ctk
from PIL import Image, ImageTk  # Necessário para trabalhar com imagens

# Função de tela de login
def tela_login():
    global tela_login, input_usuario, input_senha

    # Configurando a tela de login
    tela_login = Ctk.CTk()
    tela_login.title("Login")
    tela_login.resizable(False, False)
    tela_login.config(bg="white")

    # Carregar a imagem (ajustando para 500x500 pixels)
    logo_img = Image.open("Logo_tela_de_login.png")  # Caminho para a sua imagem
    logo_img = logo_img.resize((500, 500))  # Ajusta o tamanho
    logo = ImageTk.PhotoImage(logo_img)

    # Frame principal que vai conter as áreas de imagem e login
    main_frame = Ctk.CTkFrame(tela_login, fg_color="white", height=600, width=800, corner_radius=20)
    main_frame.grid(row=0, column=0, padx=40, pady=40)

    # Área para a imagem
    image_frame = Ctk.CTkFrame(main_frame, fg_color="white", height=500, width=500, corner_radius=20)
    image_frame.grid(row=0, column=0, padx=20, pady=20)



    # Área para as entradas (lado direito)
    login_frame = Ctk.CTkFrame(main_frame, fg_color="white", height=500, width=300, corner_radius=20)
    login_frame.grid(row=0, column=1, padx=20, pady=20)

    # Título "Login"
    title = Ctk.CTkLabel(login_frame, text="Login", text_color="black", font=("Bahnschrift", 35))
    title.grid(row=0, column=0, sticky="nw", pady=30, padx=50)

    # Entrada de usuário
    input_usuario = Ctk.CTkEntry(login_frame, text_color="black", placeholder_text="Username", fg_color="white",
                                 placeholder_text_color="black", font=("Bahnschrift", 15), width=250,
                                 corner_radius=15, height=45)
    input_usuario.grid(row=1, column=0, sticky="nwe", padx=30)

    # Entrada de senha
    input_senha = Ctk.CTkEntry(login_frame, text_color="black", placeholder_text="Password", fg_color="white",
                               placeholder_text_color="black", font=("Bahnschrift", 15), width=250,
                               corner_radius=15, height=45, show="*")
    input_senha.grid(row=2, column=0, sticky="nwe", padx=30, pady=20)

    # Botão de login
    l_btn = Ctk.CTkButton(login_frame, text="Login", font=("Bahnschrift", 15), height=40, width=120,
                          fg_color="#FF66C4", cursor="hand2", corner_radius=15, command=login_valido_tela_selecionar_usuario)
    l_btn.grid(row=3, column=0, sticky="ne", pady=20, padx=90)

    # Iniciar o loop principal
    tela_login.mainloop()

# Chama a função para abrir a tela de login
tela_login()












