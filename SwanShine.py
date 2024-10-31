import tkinter as tk
from tkinter import Frame, PhotoImage, messagebox, ttk
import mysql.connector
from mysql.connector import Error
import customtkinter as Ctk
from customtkinter import CTkCanvas, CTkLabel, CTkEntry, CTkButton, CTkToplevel
from customtkinter import *
from PIL import ImageTk, Image
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
janela_administracao = None

        
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
####################################################################################################################
import mysql.connector
from mysql.connector import Error
import tkinter as tk
from tkinter import ttk, messagebox

def open_administracao():
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

        # Configuração das colunas com larguras específicas e alinhamento centralizado
        for col in colunas:
            tree.heading(col, text=col.title(), anchor="center")
            largura = 120 if col.lower() == "nome" else 100  # Ajuste específico para cada coluna
            tree.column(col, anchor='center', width=largura, minwidth=50)

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

                atualizar_treeview(colunas[tabela_selecionada])

                if tabela_selecionada == "clientes" and id_cliente:
                    cursor.execute(f"{query[tabela_selecionada]} WHERE id = %s", (id_cliente,))
                else:
                    cursor.execute(query[tabela_selecionada])

                rows = cursor.fetchall()
                for row in rows:
                    tree.insert('', 'end', values=row)
            except Error as e:
                print(f"Erro ao executar consulta: {e}")
            finally:
                conn.close()
        
        atualizar_aba_adicionar()

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

        ttk.Button(frame_adicionar, text="Adicionar Registro", command=lambda: adicionar_registro(entradas)).grid(row=len(campos), columnspan=2, pady=10)

    def adicionar_registro(entradas):
        tabela_selecionada = combo_tabelas.get()
        
        valores = {campo: entradas[entrada].get() for campo, entrada in entradas.items()}
        
        if tabela_selecionada == "clientes":
            if not all(valores.values()):
                messagebox.showwarning("Campos Vazios", "Por favor, preencha todos os campos antes de adicionar.")
                return
            query = "INSERT INTO clientes (Nome, endereco, email, cpf, telefone, senha, genero) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            values = (valores["entry_nome"], valores["entry_endereco"], valores["entry_email"], valores["entry_cpf"], valores["entry_telefone"], valores["entry_senha"], valores["entry_genero"])
        
        elif tabela_selecionada == "admins":
            if not all(valores.values()):
                messagebox.showwarning("Campos Vazios", "Por favor, preencha todos os campos antes de adicionar.")
                return
            query = "INSERT INTO admins (Nome, Usuario, Senha) VALUES (%s, %s, %s)"
            values = (valores["entry_nome"], valores["entry_usuario"], valores["entry_senha"])
        
        elif tabela_selecionada == "profissionais":
            if not all(valores.values()):
                messagebox.showwarning("Campos Vazios", "Por favor, preencha todos os campos antes de adicionar.")
                return
            query = "INSERT INTO profissionais (nome, email, cpf) VALUES (%s, %s, %s)"
            values = (valores["entry_nome"], valores["entry_email"], valores["entry_cpf"])

        else:
            messagebox.showwarning("Tabela Não Suportada", "Adicionar registros não é suportado para esta tabela.")
            return
        
        if messagebox.askokcancel("Confirmação", "Você realmente deseja adicionar este registro?"):
            conn = conectar_bd()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute(query, values)
                    conn.commit()
                    exibir_registros()
                    for entrada in entradas.values():
                        entrada.delete(0, tk.END)
                except Error as e:
                    print(f"Erro ao adicionar registro: {e}")
                finally:
                    conn.close()

    def desativar_registro():
        conn = conectar_bd()
        if conn:
            tabela_selecionada = combo_tabelas.get()
            id_cliente = entry_id_cliente.get()

            if not id_cliente:
                messagebox.showwarning("ID Necessário", "Por favor, insira o ID do registro que deseja desativar.")
                return
            
            query = {
                "clientes": "UPDATE clientes SET ativo = 0 WHERE id = %s",
                "admins": "UPDATE admins SET ativo = 0 WHERE Id = %s",
                "profissionais": "UPDATE profissionais SET ativo = 0 WHERE id = %s"
            }

            if messagebox.askokcancel("Confirmação", "Você realmente deseja desativar este registro?"):
                try:
                    cursor = conn.cursor()
                    cursor.execute(query[tabela_selecionada], (id_cliente,))
                    conn.commit()
                    exibir_registros()
                except Error as e:
                    print(f"Erro ao desativar registro: {e}")
                finally:
                    conn.close()

    # Configurações da janela principal
    janela_administracao = tk.Tk()
    janela_administracao.title("Consulta e Edição de Registros")
    janela_administracao.geometry("1280x720")
    janela_administracao.attributes('-fullscreen', True)

    estilo = ttk.Style()
    estilo.theme_use('clam')
    estilo.configure("TButton", background="#4CAF50", foreground="white", font=("Arial", 12), padding=10)
    estilo.map("TButton", background=[("active", "#45a049")])
    estilo.configure("TLabel", font=("Arial", 12))
    
    notebook = ttk.Notebook(janela_administracao)
    notebook.pack(pady=10, expand=True, fill='both')

    aba_adicionar = ttk.Frame(notebook)
    notebook.add(aba_adicionar, text="Adicionar")

    frame_input = ttk.Frame(janela_administracao)
    frame_input.pack(pady=10, padx=10, fill='x')

    ttk.Label(frame_input, text="Selecionar Tabela", font=("Bahnschrift", 15)).grid(row=0, column=0, padx=5, pady=5, sticky='e')
    tabelas_disponiveis = ['admins', 'clientes', 'profissionais']
    combo_tabelas = ttk.Combobox(frame_input, values=tabelas_disponiveis, width=27)
    combo_tabelas.grid(row=0, column=1, padx=5, pady=5)
    combo_tabelas.current(0)
    combo_tabelas.bind("<<ComboboxSelected>>", lambda event: exibir_registros())

    entry_id_cliente = ttk.Entry(frame_input, width=20)
    entry_id_cliente.grid(row=0, column=3, padx=5, pady=5)

    ttk.Button(frame_input, text="Desativar Registro", command=desativar_registro).grid(row=0, column=4, padx=5, pady=5)

    tree = ttk.Treeview(janela_administracao, columns=(), show='headings')
    tree.pack(pady=10, padx=10, expand=True, fill='both')

    frame_adicionar = ttk.Frame(aba_adicionar)
    frame_adicionar.pack(pady=10, padx=10)

    exibir_registros()

    janela_administracao.mainloop()

open_administracao()


###################################################################################################################

# Função principal para criar o menu inicial
def menu_inicial():
    global menu_inicial, navmenu_inicial, topFrame, homeLabel, theme_button, navIcon, closeIcon
    
    menu_inicial = Ctk.CTkToplevel()
    menu_inicial.title("SwanShine")
    menu_inicial.geometry("1280x720")
    menu_inicial.state('zoomed')

    
    # Carregamento das imagens dos ícones
    try:
        navIcon = PhotoImage(file="open.png")
        closeIcon = PhotoImage(file="close.png")
    except Exception as e:
        print(f"Erro ao carregar imagens: {e}")
        navIcon = closeIcon = None

    # Configuração do frame Navbar
    navmenu_inicial = Ctk.CTkFrame(menu_inicial, fg_color=current_theme["background"], height=600, width=300)
    navmenu_inicial.place(x=-300, y=0)

    # Rótulo de cabeçalho na Navbar
    Ctk.CTkLabel(
        navmenu_inicial,
        text="Menu",
        font=("Bahnschrift", 15),
        fg_color=current_theme["accent"],  # Cor de fundo do rótulo
        text_color=current_theme["background"],  # Cor do texto
        height=60,
        width=300
    ).place(x=0, y=0)

    # Coordenada y dos widgets da Navbar
    y = 80

    # Opções no Navbar
    options = ["Configurações", "Contato", "Sobre", "Administração", "Sair"]
    commands = [open_configuracoes, open_contato, open_sobre, open_administracao, sair_menu]

    # Botões de opções no Navbar
    for option, command in zip(options, commands):
        button = Ctk.CTkButton(
            navmenu_inicial,
            text=option,
            font=("Bahnschrift", 15),
            fg_color=current_theme["button_color"],  # Cor de fundo do botão
            hover_color=current_theme["highlight"],  # Cor de fundo do botão ao passar o mouse
            text_color=current_theme["foreground"],  # Cor do texto do botão
            width=250,
            height=40,
            command=command
        )
        button.place(x=25, y=y)
        
        # Adicionar eventos de hover
        button.bind("<Enter>", lambda event, btn=button: on_enter(btn))
        button.bind("<Leave>", lambda event, btn=button: on_leave(btn))
        
        y += 50

    # Botão de fechar Navbar
    closeBtn = Ctk.CTkButton(
        navmenu_inicial,
        text="",
        image=closeIcon,
        fg_color=current_theme["button_color"],  # Cor de fundo do botão
        hover_color=current_theme["highlight"],  # Cor de fundo do botão ao passar o mouse
        command=switch,
        width=40,
        height=40
    )
    closeBtn.place(x=250, y=10)

    # Barra de navegação superior
    topFrame = Ctk.CTkFrame(
        menu_inicial,
        fg_color=current_theme["accent"],  # Cor de fundo da barra de navegação superior
        height=60
    )
    topFrame.pack(side="top", fill="x")

    # Rótulo de cabeçalho
    homeLabel = Ctk.CTkLabel(
        topFrame,
        text="SwanShine",
        font=("Bahnschrift", 15),
        fg_color=current_theme["accent"],  # Cor de fundo do rótulo
        text_color=current_theme["background"],  # Cor do texto
        height=60,
        padx=20
    )
    homeLabel.pack(side="right", padx=10)

    # Botão de Navbar
    navbarBtn = Ctk.CTkButton(
        topFrame,
        image=navIcon,
        fg_color=current_theme["button_color"],  # Cor de fundo do botão
        hover_color=current_theme["highlight"],  # Cor de fundo do botão ao passar o mouse
        command=switch,
        width=40,
        height=40,
        text=""
    )
    navbarBtn.place(x=10, y=10)

# Tela de Login
def tela_login():
    global tela_login, input_usuario, input_senha
    
tela_login = Ctk.CTk()
tela_login.title("Login")
tela_login.config(bg="white")
tela_login.resizable(False, False)

bg_img = CTkImage(dark_image=Image.open("Logo_tela_de_login.png"), size=(500, 500))

bg_lab = CTkLabel(tela_login, image=bg_img, text="")
bg_lab.grid(row=0, column=0)

frame1 = CTkFrame(tela_login,fg_color="white", bg_color="white", height=350, width=300,corner_radius=20)
frame1.grid(row=0, column=1,padx=40)

title = CTkLabel(frame1,text="Login",text_color="Black",font=("Bahnschrift", 35))
title.grid(row=0,column=0,sticky="nw",pady=30,padx=100)

input_usuario = CTkEntry(frame1,text_color="black", placeholder_text="Username", fg_color="white", placeholder_text_color="black",
                         font=("Bahnschrift", 15), width=200, corner_radius=15, height=45)
input_usuario.grid(row=1,column=0,sticky="nwe",padx=30)

input_senha = CTkEntry(frame1,text_color="black",placeholder_text="Password",fg_color="white",placeholder_text_color="black",
                         font=("Bahnschrift", 15), width=200,corner_radius=15, height=45, show="*")
input_senha.grid(row=2,column=0,sticky="nwe",padx=30,pady=20)


l_btn = CTkButton(frame1,text="Login",font=("Bahnschrift", 15),height=40,width=60,fg_color="#FF66C4",cursor="hand2",
                  corner_radius=15,command=login_valido_tela_selecionar_usuario,)
l_btn.grid(row=3,column=0,sticky="ne",pady=20, padx=100)

tela_login.mainloop()