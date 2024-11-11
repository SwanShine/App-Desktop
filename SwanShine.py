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
from tkinter import ttk, PhotoImage
import re

# Função para alternar a barra lateral
def switch():
    if navmenu_inicial.winfo_x() == 0:
        navmenu_inicial.place(x=-300)  # Esconder barra lateral
    else:
        navmenu_inicial.place(x=0)  # Mostrar barra lateral
        navmenu_inicial.lift()  # Coloca a barra lateral na frente de tudo

# Função principal para criar o menu inicial
def menu_inicial():
    global menu_inicial, navmenu_inicial, topFrame, homeLabel, theme_button, navIcon, closeIcon
    
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
    dark_color = "#d68728"  # Cor mais escura (variação do laranja)

    # Criação da barra lateral (Navbar)
    navmenu_inicial = Ctk.CTkFrame(menu_inicial, fg_color=main_color, height=720, width=300)  # Barra lateral em tom de laranja
    navmenu_inicial.place(x=-300, y=0)  # Inicialmente oculta (fora da tela)

    # Cabeçalho da barra lateral
    Ctk.CTkLabel(
        navmenu_inicial,
        text="Menu",
        font=("Bahnschrift", 15),
        fg_color=main_color,  # Cor do fundo do cabeçalho
        text_color="white",
        height=60,
        width=300
    ).place(x=0, y=0)

    # Opções no Navbar
    options = ["Configurações", "Contato", "Sobre", "Sair"]
    commands = [open_configuracoes, open_contato, open_sobre, sair_menu]

    y = 80  # Posição vertical inicial para os botões
    for option, command in zip(options, commands):
        button = Ctk.CTkButton(
            navmenu_inicial,
            text=option,
            font=("Bahnschrift", 15),
            fg_color=main_color,  # Cor de fundo dos botões
            hover_color=hover_color,  # Cor de hover dos botões
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
        fg_color=main_color,  # Cor de fundo
        hover_color=hover_color,  # Cor de hover
        command=switch,
        width=40,
        height=40
    )
    closeBtn.place(x=250, y=10)

    # Barra superior de navegação
    topFrame = Ctk.CTkFrame(menu_inicial, fg_color=main_color, height=60)  # Barra superior em tom de laranja
    topFrame.pack(side="top", fill="x")

    # Rótulo do nome da aplicação na barra superior
    homeLabel = Ctk.CTkLabel(
        topFrame,
        text="SwanShine",
        font=("Bahnschrift", 15),
        fg_color=main_color,  # Cor de fundo do nome
        text_color="white",
        height=60,
        padx=20
    )
    homeLabel.pack(side="right", padx=10)

    # Botão de abrir a barra lateral
    navbarBtn = Ctk.CTkButton(
        topFrame,
        image=navIcon,
        fg_color=main_color,  # Cor de fundo
        hover_color=hover_color,  # Cor de hover
        command=switch,
        width=40,
        height=40,
        text=""
    )
    navbarBtn.place(x=10, y=10)

    # Função de conexão com o banco de dados
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

    # Função para atualizar as colunas do TreeView
    def atualizar_treeview(colunas):
        tree.delete(*tree.get_children())
        tree["columns"] = colunas

        for col in colunas:
            tree.heading(col, text=col.title(), anchor="center")
            largura = 150 if col.lower() == "nome" else 120  # Aumentando largura para "nome"
            tree.column(col, anchor='center', width=largura, minwidth=80)  # Tamanho aumentado

    # Função para exibir registros no TreeView
    def exibir_registros():
        conn = conectar_bd()
        if conn:
            try:
                cursor = conn.cursor()
                tabela_selecionada = combo_tabelas.get()
                id_cliente = entry_id_cliente.get()

                query = {
                    "admins": "SELECT Id, Nome, Usuario, Senha FROM admins",
                    "clientes": "SELECT id, Nome, endereco, email, cpf, telefone, genero, senha FROM clientes",
                    "profissionais": "SELECT id, nome, email, cpf FROM profissionais"
                }

                colunas = {
                    "admins": ("Id", "Nome", "Usuario", "Senha"),
                    "clientes": ("id", "Nome", "endereco", "email", "cpf", "telefone", "genero", "senha"),
                    "profissionais": ("id", "nome", "email", "cpf")
                }

                # Atualiza as colunas do TreeView com base na tabela selecionada
                atualizar_treeview(colunas[tabela_selecionada])

                # Verifica se há um ID de cliente inserido para filtrar
                if id_cliente:
                    # Realiza a busca filtrada por ID
                    cursor.execute(f"{query[tabela_selecionada]} WHERE id = %s", (id_cliente,))
                else:
                    # Caso não tenha ID, traz todos os registros
                    cursor.execute(query[tabela_selecionada])

                rows = cursor.fetchall()
                for row in rows:
                    # Filtra os valores vazios antes de inserir no TreeView
                    row_filtered = [value if value != '' else None for value in row]
                    tree.insert('', 'end', values=row_filtered)
            except Error as e:
                print(f"Erro ao executar consulta: {e}")
            finally:
                conn.close()

  


    def aplicar_mascara(entry, tipo):
        """Aplica uma máscara ao conteúdo do campo de entrada (entry) com base no tipo especificado."""
        
        def mascarar(event):
            texto = entry.get()

            # Remove caracteres indesejados dependendo do tipo de entrada
            if tipo != "email":
                texto = re.sub(r'[^0-9]', '', texto)

            # Aplica a máscara apropriada para o tipo

                

            elif tipo == "telefone":
                texto = texto[:11]  # Limita a 11 caracteres
                texto = re.sub(r'(\d{2})(\d)', r'(\1) \2', texto)
                texto = re.sub(r'(\(\d{2}\)) (\d{5})(\d)', r'\1 \2-\3', texto)

            elif tipo == "email":
                # Validação básica do e-mail
                if not re.match(r"[^@]+@[^@]+\.[^@]+", texto):
                    print("Formato de e-mail inválido")

            # Atualiza o conteúdo do entry com o texto formatado
            entry.delete(0, tk.END)
            entry.insert(0, texto)

        # Associa a função de máscara ao evento de liberação de tecla
        entry.bind("<KeyRelease>", mascarar)


    # Função para atualizar as abas com os campos corretos
    def atualizar_aba_adicionar():
        for widget in frame_adicionar.winfo_children():
            widget.destroy()

        tabela_selecionada = combo_tabelas.get()

        campos_por_tabela = {
            "clientes": [("Nome", "entry_nome"), ("Endereço", "entry_endereco"), ("Email", "entry_email"), 
                         ("CPF", "entry_cpf"), ("Telefone", "entry_telefone"), ("Gênero", "entry_genero"), 
                         ("Senha", "entry_senha")],
            "admins": [("Nome", "entry_nome"), ("Usuário", "entry_usuario"), ("Senha", "entry_senha")],
            "profissionais": [("Nome", "entry_nome"), ("Email", "entry_email"), ("CPF", "entry_cpf")]
        }

        campos = campos_por_tabela.get(tabela_selecionada, [])

        entradas = {}

        for i, (label_text, entry_name) in enumerate(campos):
            ttk.Label(frame_adicionar, text=label_text).grid(row=i, column=0, padx=5, pady=5, sticky='e')
            entrada = ttk.Entry(frame_adicionar, width=30)
            entrada.grid(row=i, column=1, padx=5, pady=5)
            entradas[entry_name] = entrada

            # Aplicando as máscaras nos campos
            if entry_name == "entry_cpf":
                aplicar_mascara(entrada, "cpf")
            elif entry_name == "entry_telefone":
                aplicar_mascara(entrada, "telefone")
            elif entry_name == "entry_email":
                aplicar_mascara(entrada, "email")

        ttk.Button(frame_adicionar, text="Adicionar Registro", command=lambda: adicionar_registro(entradas)).grid(row=len(campos), columnspan=2, pady=10)

    # Função para adicionar registro ao banco
    def adicionar_registro(entradas):
        try:
            conn = conectar_bd()
            cursor = conn.cursor()

            tabela_selecionada = combo_tabelas.get()
            if tabela_selecionada == "clientes":
                query = "INSERT INTO clientes (Nome, endereco, email, cpf, telefone, genero, senha) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                values = (
                    entradas["entry_nome"].get(),
                    entradas["entry_endereco"].get(),
                    entradas["entry_email"].get(),
                    entradas["entry_cpf"].get(),
                    entradas["entry_telefone"].get(),
                    entradas["entry_genero"].get(),
                    entradas["entry_senha"].get()
                )
            elif tabela_selecionada == "admins":
                query = "INSERT INTO admins (Nome, Usuario, Senha) VALUES (%s, %s, %s)"
                values = (
                    entradas["entry_nome"].get(),
                    entradas["entry_usuario"].get(),
                    entradas["entry_senha"].get()
                )
            else:
                query = "INSERT INTO profissionais (nome, email, cpf) VALUES (%s, %s, %s)"
                values = (
                    entradas["entry_nome"].get(),
                    entradas["entry_email"].get(),
                    entradas["entry_cpf"].get()
                )
            
            cursor.execute(query, values)
            conn.commit()
            print("Registro adicionado com sucesso.")
            exibir_registros()  # Atualizar os registros
        except Error as e:
            print(f"Erro ao adicionar registro: {e}")
        finally:
            conn.close()

    # Notebook para abas
    notebook = ttk.Notebook(menu_inicial)
    notebook.pack(pady=10, expand=True, fill='both')

    aba_adicionar = ttk.Frame(notebook)
    aba_editar = ttk.Frame(notebook)
    aba_desativar = ttk.Frame(notebook)

    notebook.add(aba_adicionar, text="Adicionar")
    notebook.add(aba_editar, text="Editar")
    notebook.add(aba_desativar, text="Desativar")

    # Frame para entrada de dados e botões
    frame_input = ttk.Frame(menu_inicial)
    frame_input.pack(pady=10, padx=10, fill='x')

    # Combobox para seleção de tabelas
    ttk.Label(frame_input, text="Selecionar Tabela", font=("Bahnschrift", 15)).grid(row=0, column=0, padx=5, pady=5, sticky='e')
    tabelas_disponiveis = ['admins', 'clientes', 'profissionais']
    combo_tabelas = ttk.Combobox(frame_input, values=tabelas_disponiveis, width=27)
    combo_tabelas.grid(row=0, column=1, padx=5, pady=5)
    combo_tabelas.current(0)
    combo_tabelas.bind("<<ComboboxSelected>>", lambda event: (exibir_registros(), atualizar_aba_adicionar()))

    # Entrada de ID para filtragem
    ttk.Label(frame_input, text="Filtrar por ID (opcional)").grid(row=1, column=0, padx=5, pady=5, sticky='e')
    entry_id_cliente = ttk.Entry(frame_input, width=30)
    entry_id_cliente.grid(row=1, column=1, padx=5, pady=5)

    # Botão para filtrar registros
    button_filtrar = Ctk.CTkButton(
        frame_input,
        text="Filtrar por ID",
        command=exibir_registros,
        width=20,
        height=30,
        fg_color=main_color,  # Cor de fundo
        hover_color=hover_color  # Cor de hover
    )
    button_filtrar.grid(row=1, column=2, padx=5, pady=5)

    # Frame para exibir a tabela com scrollbar
    frame_exibir = ttk.Frame(menu_inicial)
    frame_exibir.pack(pady=10, expand=True, fill='both')

    # Adicionando o scrollbar
    tree_frame = ttk.Frame(frame_exibir)
    tree_frame.pack(fill='both', expand=True)

    tree_scroll = ttk.Scrollbar(tree_frame, orient="vertical")
    tree_scroll.pack(side="right", fill="y")

    tree = ttk.Treeview(tree_frame, columns=[], show='headings', height=15, yscrollcommand=tree_scroll.set)
    tree.pack(fill="both", expand=True)

    tree_scroll.config(command=tree.yview)

    # Frame para adicionar registros
    frame_adicionar = ttk.Frame(aba_adicionar)
    frame_adicionar.pack(pady=10, fill='x')

    # Atualiza a aba de adicionar quando a aplicação inicia
    atualizar_aba_adicionar()

    exibir_registros()  # Exibe registros quando a aplicação inicia




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

    # Label para exibir a imagem
    logo_label = Ctk.CTkLabel(image_frame, image=logo, text="")
    logo_label.image = logo  # Manter referência da imagem
    logo_label.grid(row=0, column=0)

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












