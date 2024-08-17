import tkinter as tk
from tkinter import Frame, PhotoImage, messagebox, ttk
import mysql.connector
import customtkinter as Ctk
from customtkinter import CTkCanvas, CTkLabel, CTkEntry, CTkButton, CTkToplevel
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
            cursor = conn.cursor()
            if conn.is_connected():
                print("Conectado ao banco de dados")
            return conn, cursor
        except mysql.connector.Error as erro:
            print("Erro ao conectar ao MySQL:", erro)
            return None, None

    def exibir_registros():
        conn, cursor = conectar_bd()
        if conn and cursor:
            cursor.execute("SELECT Id_clientes, CPF, Email, Endereço, Nome, Telefone FROM clientes")
            rows = cursor.fetchall()
            for row in tree.get_children():
                tree.delete(row)
            for row in rows:
                tree.insert('', 'end', values=row)
            conn.close()

    def adicionar_registro():
        cpf = entry_cpf.get()
        email = entry_email.get()
        endereco = entry_endereco.get()
        nome = entry_nome.get()
        telefone = entry_telefone.get()
        conn, cursor = conectar_bd()
        if conn and cursor:
            try:
                cursor.execute(
                    "INSERT INTO clientes (CPF, Email, Endereço, Nome, Telefone) VALUES (%s, %s, %s, %s, %s)",
                    (cpf, email, endereco, nome, telefone)
                )
                conn.commit()
                exibir_registros()
            except mysql.connector.Error as erro:
                print("Erro ao adicionar registro:", erro)
            finally:
                conn.close()

    def deletar_registro():
        selected_item = tree.selection()
        if selected_item:
            conn, cursor = conectar_bd()
            if conn and cursor:
                try:
                    for item in selected_item:
                        id_registro = tree.item(item, 'values')[0]
                        cursor.execute("DELETE FROM clientes WHERE Id_clientes=%s", (id_registro,))
                        conn.commit()
                        tree.delete(item)
                except mysql.connector.Error as erro:
                    print("Erro ao deletar registro:", erro)
                finally:
                    conn.close()

    def editar_registro():
        selected_item = tree.selection()
        novo_valor = entry_novo_valor.get()
        campo = combo_campos.get()
        if selected_item and novo_valor and campo:
            conn, cursor = conectar_bd()
            if conn and cursor:
                try:
                    for item in selected_item:
                        id_registro = tree.item(item, 'values')[0]
                        cursor.execute(f"UPDATE clientes SET {campo}=%s WHERE Id_clientes=%s", (novo_valor, id_registro))
                        conn.commit()
                        valores_atuais = list(tree.item(item, 'values'))
                        indice_campo = ['Id_clientes', 'CPF', 'Email', 'Endereço', 'Nome', 'Telefone'].index(campo)
                        valores_atuais[indice_campo] = novo_valor
                        tree.item(item, values=valores_atuais)
                except mysql.connector.Error as erro:
                    print("Erro ao editar registro:", erro)
                finally:
                    conn.close()

    def filtrar_por_id_cliente():
        id_cliente = entry_id_cliente.get()
        conn, cursor = conectar_bd()
        if conn and cursor:
            cursor.execute("SELECT Id_clientes, CPF, Email, Endereço, Nome, Telefone FROM clientes WHERE Id_clientes = %s", (id_cliente,))
            rows = cursor.fetchall()
            for row in tree.get_children():
                tree.delete(row)
            for row in rows:
                tree.insert('', 'end', values=row)
            conn.close()
            
    def fechar_janela_admin():
        janela_admin.withdraw()
        menu_inicial.deiconify()

    janela_admin = tk.Toplevel(menu_inicial)
    janela_admin.title("Consulta e Edição de Registros")
    janela_admin.geometry("1280x720")

    estilo = ttk.Style()
    estilo.theme_use('clam')

    frame_input = ttk.Frame(janela_admin)
    frame_input.pack(pady=10, padx=10, fill='x')

    labels = ['Nome', 'CPF', 'Email', 'Endereço', 'Telefone', 'Campo', 'Novo Valor', 'Filtrar por ID Cliente']
    entries = {}
    for i, label in enumerate(labels):
        ttk.Label(frame_input, text=label).grid(row=i, column=0, padx=5, pady=5, sticky='e')
        if label == 'Campo':
            campos_disponiveis = ['Id_clientes', 'CPF', 'Email', 'Endereço', 'Nome', 'Telefone']
            combo_campos = ttk.Combobox(frame_input, values=campos_disponiveis, width=27)
            combo_campos.grid(row=i, column=1, padx=5, pady=5)
        else:
            entries[label] = ttk.Entry(frame_input, width=30)
            entries[label].grid(row=i, column=1, padx=5, pady=5)

    entry_nome, entry_cpf, entry_email, entry_endereco, entry_telefone, entry_novo_valor, entry_id_cliente = (
        entries['Nome'], entries['CPF'], entries['Email'], entries['Endereço'], entries['Telefone'], 
        entries['Novo Valor'], entries['Filtrar por ID Cliente']
    )


    frame_botoes = ttk.Frame(janela_admin)
    frame_botoes.pack(pady=10)
    

    btn_adicionar = CTkButton(frame_botoes, text="Adicionar", command=adicionar_registro)
    btn_adicionar.grid(row=0, column=0, padx=10)

    btn_editar = CTkButton(frame_botoes, text="Editar Campo Selecionado", command=editar_registro)
    btn_editar.grid(row=0, column=1, padx=10)

    btn_filtrar = CTkButton(frame_botoes, text="Filtrar por ID Cliente", command=filtrar_por_id_cliente)
    btn_filtrar.grid(row=0, column=2, padx=10)

    tree = ttk.Treeview(janela_admin, columns=('ID', 'CPF', 'Email', 'Endereço', 'Nome', 'Telefone'), show='headings')
    tree.heading('ID', text='ID')
    tree.heading('CPF', text='CPF')
    tree.heading('Email', text='Email')
    tree.heading('Endereço', text='Endereço')
    tree.heading('Nome', text='Nome')
    tree.heading('Telefone', text='Telefone')
    tree.pack(fill='both', expand=True, pady=10)

    frame_botoes_inferiores = ttk.Frame(janela_admin)
    frame_botoes_inferiores.pack(pady=10)

    btn_atualizar = CTkButton(frame_botoes_inferiores, text="Atualizar Lista", command=exibir_registros)
    btn_atualizar.grid(row=0, column=0, padx=20)

    btn_deletar = CTkButton(frame_botoes_inferiores, text="Deletar Selecionado", command=deletar_registro)
    btn_deletar.grid(row=0, column=1, padx=20)
    
    btn_voltar = CTkButton(frame_botoes_inferiores, text="Voltar", command=fechar_janela_admin)
    btn_voltar.grid(row=0, column=2, padx=20)

    exibir_registros()
# Função principal para criar o menu inicial
def menu_inicial():
    global menu_inicial, navmenu_inicial, topFrame, homeLabel, theme_button, navIcon, closeIcon
    
    menu_inicial = Ctk.CTkToplevel()
    menu_inicial.title("SwanShine")
    menu_inicial.geometry("1280x720")
    
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
tela_login._set_appearance_mode("System")
tela_login.geometry("500x500")
tela_login.title("Login")
tela_login.maxsize(width=500, height=500)
tela_login.minsize(width=500, height=500)

rightframe = Frame(tela_login, width=250, height=500, relief="raise", bg="orange")
rightframe.pack(side="right", fill="both")

label_usuario = CTkLabel(rightframe, width=250, height=50, text="Usuario", font=("Inter-Regular", 16,"italic"))
label_usuario.pack(pady=10)

input_usuario = CTkEntry(rightframe, width=250, height=50, fg_color="white", font=("Inter-Regular", 16, "italic"))
input_usuario.pack(pady=10)

label_senha = CTkLabel(rightframe, width=250, height=50, text="Senha", font=("Inter-Regular", 16, "italic"))
label_senha.pack(pady=10)

input_senha = CTkEntry(rightframe, width=250, height=50, fg_color="white", font=("Inter-Regular", 16, "italic"))
input_senha.pack(pady=10)

button_entrar = CTkButton(rightframe, text="Entrar!", fg_color="black", command=login_valido_tela_selecionar_usuario, font=("Inter-Regular", 16, "italic"))
button_entrar.place(x=50, y=330)

leftframe = Frame(tela_login, width=250, height=500, relief="raise", bg="orange")
leftframe.pack(side="left", fill="both")

label_imagem = CTkLabel(leftframe, width=250, height=250,text="")
label_imagem.place(x=-100, y=-10)

tela_login.mainloop()