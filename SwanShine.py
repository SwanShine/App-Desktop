import tkinter as tk
from tkinter import Frame, PhotoImage, messagebox, ttk
import mysql.connector
from mysql.connector import Error
import customtkinter as Ctk
from customtkinter import CTkCanvas, CTkLabel, CTkEntry, CTkButton, CTkToplevel
from customtkinter import *
from PIL import ImageTk, Image
import pyglet

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
        
#Função para os botoes navbar     
def check_for_updates():
    # Função para verificar atualizações
    # Este é um exemplo fictício; você deve substituir isso pelo código real
    print("Verificando atualizações...")

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

def open_profile():
    global janela_profile
    # Verifica se a janela está definida e se ainda existe
    if janela_profile is None or not janela_profile.winfo_exists():
        janela_profile = Ctk.CTkToplevel(menu_inicial)
        janela_profile.title("Perfil")
        janela_profile.geometry("400x300")

        # Adiciona o perfil do usuário na janela
        profile_usuario = Ctk.CTkLabel(janela_profile, text="usuario")
        profile_usuario.pack(pady=10)
        
        # Adiciona um botão para fechar a janela
        close_button = Ctk.CTkButton(janela_profile, text="Fechar", command=fechar_profile)
        close_button.pack(pady=10)
    else:
        janela_profile.lift()  # Traz a janela para o topo se já existir
        

def open_configuracoes():
    global theme_button
    global janela_configuracoes

    def fechar_config():
        janela_configuracoes.destroy()

    if janela_configuracoes is None or not janela_configuracoes.winfo_exists():
        janela_configuracoes = Ctk.CTkToplevel(menu_inicial)
        janela_configuracoes.title("Configurações")
        janela_configuracoes.geometry("400x300")

        Ctk.CTkLabel(janela_configuracoes, text="Configurações").pack(pady=10)

        theme_button = Ctk.CTkButton(janela_configuracoes, text="Tema Escuro", command=switch_theme)
        theme_button.pack(pady=10)

        update_button = Ctk.CTkButton(janela_configuracoes, text="Buscar Atualizações", command=check_for_updates)
        update_button.pack(pady=10)

        close_button = Ctk.CTkButton(janela_configuracoes, text="Fechar",command=fechar_config)
        close_button.pack(pady=10)

        # Forçar atualização dos widgets
        menu_inicial.update()

def open_contato():
    global janela_contato
    if janela_contato is None or not janela_contato.winfo_exists():
        janela_contato = Ctk.CTkToplevel(menu_inicial)
        janela_contato.title("Contato")

def open_sobre():
    global janela_sobre
    if janela_sobre is None or not janela_sobre.winfo_exists():
        janela_sobre = Ctk.CTkToplevel(menu_inicial)
        janela_sobre.title("Sobre")
        
def sair_menu():
    resposta = messagebox.askyesno("Confirmar Saída", "Você realmente deseja sair?")
    if resposta:
        menu_inicial.quit()  # Fecha a aplicação
    

# Tela de Administração
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

    def exibir_registros():
        conn = conectar_bd()
        if conn:
            try:
                cursor = conn.cursor()
                tabela_selecionada = combo_tabelas.get()
                id_cliente = entry_id_cliente.get()
                query = {
                    "admins": "SELECT Id, Nome, Usuario, Senha FROM admins",
                    "clientes": "SELECT id, Nome, endereco, Email, cpf, Telefone, senha FROM clientes",
                    "imagens": "SELECT id, descricao FROM imagens",
                    "profissionais": "SELECT id, nome, email, cpf FROM profissionais",
                    "serv_pro": "SELECT Id_profissionais FROM serv_pro",
                    "serviços": "SELECT Nome, Preço, Descrição, Id_clientes, Id_profissionais FROM serviços"
                }
                
                if tabela_selecionada == "clientes" and id_cliente:
                    cursor.execute(f"{query[tabela_selecionada]} WHERE id = %s", (id_cliente,))
                else:
                    cursor.execute(query[tabela_selecionada])
                    
                rows = cursor.fetchall()
                tree.delete(*tree.get_children())
                for row in rows:
                    tree.insert('', 'end', values=row)
            except Error as e:
                print(f"Erro ao executar consulta: {e}")
            finally:
                conn.close()

    def adicionar_registro():
        nome = entry_nome.get()
        cpf = entry_cpf.get()
        email = entry_email.get()
        endereco = entry_endereco.get()
        telefone = entry_telefone.get()
        senha = entry_senha.get()
        usuario = entry_usuario.get()

        tabela_selecionada = combo_tabelas.get()
        
        if tabela_selecionada == "clientes":
            if not all([nome, endereco, email, cpf, telefone, senha]):
                messagebox.showwarning("Campos Vazios", "Por favor, preencha todos os campos antes de adicionar.")
                return
            query = "INSERT INTO clientes (Nome, endereco, Email, cpf, Telefone, senha) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (nome, endereco, email, cpf, telefone, senha)
        elif tabela_selecionada == "admins":
            if not all([nome, usuario, senha]):
                messagebox.showwarning("Campos Vazios", "Por favor, preencha todos os campos antes de adicionar.")
                return
            query = "INSERT INTO admins (Nome, Usuario, Senha) VALUES (%s, %s, %s)"
            values = (nome, usuario, senha)
        elif tabela_selecionada == "profissionais":
            if not all([nome, email, cpf]):
                messagebox.showwarning("Campos Vazios", "Por favor, preencha todos os campos antes de adicionar.")
                return
            query = "INSERT INTO profissionais (nome, email, cpf) VALUES (%s, %s, %s)"
            values = (nome, email, cpf)
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
                    for entry in [entry_cpf, entry_email, entry_endereco, entry_nome, entry_telefone, entry_usuario, entry_senha]:
                        entry.delete(0, tk.END)
                except Error as e:
                    print(f"Erro ao adicionar registro: {e}")
                finally:
                    conn.close()

    def deletar_registro():
        selected_item = tree.selection()
        if selected_item and messagebox.askokcancel("Confirmação", "Você realmente deseja deletar o(s) registro(s) selecionado(s)?"):
            conn = conectar_bd()
            if conn:
                try:
                    cursor = conn.cursor()
                    tabela_selecionada = combo_tabelas.get()
                    for item in selected_item:
                        id_registro = tree.item(item, 'values')[0]
                        if tabela_selecionada == "clientes":
                            cursor.execute("DELETE FROM clientes WHERE id=%s", (id_registro,))
                        elif tabela_selecionada == "admins":
                            cursor.execute("DELETE FROM admins WHERE Id=%s", (id_registro,))
                        elif tabela_selecionada == "profissionais":
                            cursor.execute("DELETE FROM profissionais WHERE id=%s", (id_registro,))
                        conn.commit()
                        tree.delete(item)
                except Error as e:
                    print(f"Erro ao deletar registro: {e}")
                finally:
                    conn.close()

    def editar_registro():
        selected_item = tree.selection()
        novo_valor = entry_novo_valor.get()
        campo = combo_campos.get()
        if selected_item and novo_valor and campo:
            if messagebox.askokcancel("Confirmação", "Você realmente deseja editar o campo selecionado?"):
                conn = conectar_bd()
                if conn:
                    try:
                        cursor = conn.cursor()
                        tabela_selecionada = combo_tabelas.get()
                        for item in selected_item:
                            id_registro = tree.item(item, 'values')[0]
                            if tabela_selecionada == "clientes":
                                cursor.execute(f"UPDATE clientes SET {campo}=%s WHERE id=%s", (novo_valor, id_registro))
                            elif tabela_selecionada == "admins":
                                cursor.execute(f"UPDATE admins SET {campo}=%s WHERE Id=%s", (novo_valor, id_registro))
                            elif tabela_selecionada == "profissionais":
                                cursor.execute(f"UPDATE profissionais SET {campo}=%s WHERE id=%s", (novo_valor, id_registro))
                            conn.commit()
                            valores_atuais = list(tree.item(item, 'values'))
                            indice_campo = tree["columns"].index(campo)
                            valores_atuais[indice_campo] = novo_valor
                            tree.item(item, values=valores_atuais)
                    except Error as e:
                        print(f"Erro ao editar registro: {e}")
                    finally:
                        conn.close()

    def confirmar_filtro():
        exibir_registros()

    def fechar_janela_admin():
        janela_administracao.destroy()

    # Criando a interface
    janela_administracao = tk.Tk()
    janela_administracao.title("Consulta e Edição de Registros")
    janela_administracao.geometry("1280x720")
    janela_administracao.attributes('-fullscreen', True)

    estilo = ttk.Style()
    estilo.theme_use('clam')

    notebook = ttk.Notebook(janela_administracao)
    notebook.pack(pady=10, expand=True, fill='both')

    # Abas
    aba_adicionar = ttk.Frame(notebook)
    aba_deletar = ttk.Frame(notebook)
    aba_editar = ttk.Frame(notebook)

    notebook.add(aba_adicionar, text="Adicionar")
    notebook.add(aba_deletar, text="Deletar")
    notebook.add(aba_editar, text="Editar")

    # Frame comum para selecionar tabela e exibir registros
    frame_input = ttk.Frame(janela_administracao)
    frame_input.pack(pady=10, padx=10, fill='x')

    ttk.Label(frame_input, text="Selecionar Tabela").grid(row=0, column=0, padx=5, pady=5, sticky='e')
    tabelas_disponiveis = ['admins', 'clientes', 'imagens', 'profissionais', 'serv_pro', 'serviços']
    combo_tabelas = ttk.Combobox(frame_input, values=tabelas_disponiveis, width=27)
    combo_tabelas.grid(row=0, column=1, padx=5, pady=5)
    combo_tabelas.current(0)
    combo_tabelas.bind("<<ComboboxSelected>>", lambda event: exibir_registros())  # Atualiza automaticamente ao selecionar

    ttk.Label(frame_input, text="Filtrar por ID Cliente").grid(row=0, column=2, padx=5, pady=5, sticky='e')
    entry_id_cliente = ttk.Entry(frame_input, width=20)
    entry_id_cliente.grid(row=0, column=3, padx=5, pady=5)

    # Árvore para exibir registros
    tree = ttk.Treeview(janela_administracao, columns=(1, 2, 3, 4, 5, 6, 7, 8, 9), show='headings')
    tree.pack(pady=20, padx=20, fill='both', expand=True)

    for col in tree['columns']:
        tree.heading(col, text=col)

    frame_botoes = ttk.Frame(janela_administracao)
    frame_botoes.pack(pady=10, padx=10)

    # Botões Fechar e Atualizar
    CTkButton(frame_botoes, text="Fechar", command=fechar_janela_admin).pack(side='right', padx=5)
    CTkButton(frame_botoes, text="Atualizar", command=exibir_registros).pack(side='right', padx=5)

    # Aba Adicionar
    labels_adicionar = ['Nome', 'CPF', 'Email', 'endereço', 'Telefone', 'Usuário', 'Senha']
    entries_adicionar = {}
    for i, label in enumerate(labels_adicionar):
        ttk.Label(aba_adicionar, text=label).grid(row=i, column=0, padx=5, pady=5, sticky='e')
        entries_adicionar[label] = ttk.Entry(aba_adicionar, width=30)
        entries_adicionar[label].grid(row=i, column=1, padx=5, pady=5)

    entry_nome = entries_adicionar['Nome']
    entry_cpf = entries_adicionar['CPF']
    entry_email = entries_adicionar['Email']
    entry_endereco = entries_adicionar['endereço']
    entry_telefone = entries_adicionar['Telefone']
    entry_usuario = entries_adicionar['Usuário']
    entry_senha = entries_adicionar['Senha']

    CTkButton(aba_adicionar, text="Adicionar", command=adicionar_registro).grid(row=len(labels_adicionar), column=1, pady=10)

    # Aba Deletar
    CTkButton(aba_deletar, text="Deletar", command=deletar_registro).pack(pady=10)

    # Aba Editar
    labels_editar = ['Campo', 'Novo Valor']
    entries_editar = {}
    for i, label in enumerate(labels_editar):
        ttk.Label(aba_editar, text=label).grid(row=i, column=0, padx=5, pady=5, sticky='e')
        if label == 'Campo':
            campos_disponiveis = ['cpf', 'Email', 'endereco', 'Nome', 'Telefone', 'Usuario', 'Senha']
            combo_campos = ttk.Combobox(aba_editar, values=campos_disponiveis, width=27)
            combo_campos.grid(row=i, column=1, padx=5, pady=5)
        else:
            entries_editar[label] = ttk.Entry(aba_editar, width=30)
            entries_editar[label].grid(row=i, column=1, padx=5, pady=5)

    entry_novo_valor = entries_editar['Novo Valor']

    CTkButton(aba_editar, text="Editar", command=editar_registro).grid(row=len(labels_editar), column=1, pady=10)

    exibir_registros()
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
    options = ["Profile", "Configurações", "Contato", "Sobre", "Administração", "Sair"]
    commands = [open_profile, open_configuracoes, open_contato, open_sobre, open_administracao, sair_menu]

    # Botões de opções no Navbar
    for option, command in zip(options, commands):
        button = Ctk.CTkButton(
            navmenu_inicial,
            text=option,
            font=("Bahnschrift Light", 15),
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

title = CTkLabel(frame1,text="Login",text_color="Black",font=("",35))
title.grid(row=0,column=0,sticky="nw",pady=30,padx=100)

input_usuario = CTkEntry(frame1,text_color="black", placeholder_text="Username", fg_color="white", placeholder_text_color="black",
                         font=("",16), width=200, corner_radius=15, height=45)
input_usuario.grid(row=1,column=0,sticky="nwe",padx=30)

input_senha = CTkEntry(frame1,text_color="black",placeholder_text="Password",fg_color="white",placeholder_text_color="black",
                         font=("",16), width=200,corner_radius=15, height=45, show="*")
input_senha.grid(row=2,column=0,sticky="nwe",padx=30,pady=20)


l_btn = CTkButton(frame1,text="Login",font=("",15),height=40,width=60,fg_color="#FF66C4",cursor="hand2",
                  corner_radius=15,command=login_valido_tela_selecionar_usuario,)
l_btn.grid(row=3,column=0,sticky="ne",pady=20, padx=100)

tela_login.mainloop()