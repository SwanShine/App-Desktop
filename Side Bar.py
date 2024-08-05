import tkinter as tk
from tkinter import Frame, PhotoImage, messagebox, ttk
import mysql.connector
import customtkinter as Ctk
from customtkinter import CTkCanvas, CTkLabel, CTkEntry, CTkButton, CTkToplevel
from PIL import ImageTk, Image
import pyglet

# Dicionário de cores para os temas
colors_light = {
    "background": "#FFFFFF",
    "foreground": "#000000",
    "accent": "#FF8700",
    "button_color": "#D1D1D1"  # Cor fixa dos botões no tema claro
}

colors_dark = {
    "background": "#2E2E2E",
    "foreground": "#FFFFFF",
    "accent": "#FF8700",
    "button_color": "#D1D1D1"  # Cor fixa dos botões no tema escuro
}

current_theme = colors_light  # Tema inicial

# Estado do botão de alternância
btnState = False

# Função para alterar a cor de fundo dos botões quando o mouse passa sobre eles
def on_enter(button):
    button.configure(fg_color=current_theme["accent"])

def on_leave(button):
    button.configure(fg_color=current_theme["button_color"])

# Função para alternar o estado do Navbar
def switch():
    global btnState
    if btnState:
        close_animation(-300)
    else:
        open_animation(0)

# Função para animar o fechamento da Navbar
def close_animation(x):
    if x >= -300:
        navmenu_inicial.place(x=x, y=0)
        menu_inicial.after(10, close_animation, x - 10)
    else:
        update_ui_for_navbar_closed()

# Função para animar a abertura da Navbar
def open_animation(x):
    if x <= 0:
        navmenu_inicial.place(x=x, y=0)
        menu_inicial.after(10, open_animation, x + 10)
    else:
        update_ui_for_navbar_open()

# Atualizar a interface quando a Navbar estiver fechada
def update_ui_for_navbar_closed():
    homeLabel.configure(fg_color=current_theme["accent"], text_color=current_theme["background"])
    topFrame.configure(fg_color=current_theme["accent"])
    menu_inicial.configure(fg_color=current_theme["background"])
    global btnState
    btnState = False

# Atualizar a interface quando a Navbar estiver aberta
def update_ui_for_navbar_open():
    homeLabel.configure(fg_color=current_theme["background"], text_color=current_theme["foreground"])
    topFrame.configure(fg_color=current_theme["background"])
    menu_inicial.configure(fg_color=current_theme["background"])
    global btnState
    btnState = True

# Função para alternar entre temas claro e escuro
def toggle_theme():
    global current_theme
    if current_theme == colors_light:
        current_theme = colors_dark
        theme_button.configure(text="Tema Claro")
    else:
        current_theme = colors_light
        theme_button.configure(text="Tema Escuro")
    update_ui_for_navbar_open()
    update_ui_for_navbar_closed()

# Função para buscar atualizações
def check_for_updates():
    messagebox.showinfo("Atualizações", "Você está usando a versão mais recente.")

# Função principal para criar o menu inicial
def menu_inicial():
    global menu_inicial, navmenu_inicial, topFrame, homeLabel, theme_button
    
    menu_inicial = Ctk.CTkToplevel()
    menu_inicial.title("SwanShine")
    menu_inicial.geometry("400x600+850+50")
    
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
    Ctk.CTkLabel(navmenu_inicial, text="Menu", font=("Bahnschrift", 15), fg_color=current_theme["accent"], text_color=current_theme["background"], height=60, width=300).place(x=0, y=0)

    # Coordenada y dos widgets da Navbar
    y = 80

    # Opções no Navbar
    options = ["Profile", "Configurações", "Contato", "Sobre", "Administração"]

    # Botões de opções no Navbar
    for option in options:
        button = Ctk.CTkButton(navmenu_inicial, text=option, font=("Bahnschrift Light", 15), fg_color=current_theme["button_color"], hover_color=current_theme["accent"], text_color=current_theme["foreground"], width=250, height=40)
        button.place(x=25, y=y)
        
        # Adicionar eventos de hover
        button.bind("<Enter>", lambda event, btn=button: on_enter(btn))
        button.bind("<Leave>", lambda event, btn=button: on_leave(btn))
        
        y += 50

    # Botão de fechar Navbar
    closeBtn = Ctk.CTkButton(navmenu_inicial, text="", image=closeIcon, fg_color=current_theme["button_color"], hover_color=current_theme["accent"], command=switch, width=40, height=40)
    closeBtn.place(x=250, y=10)

    # Barra de navegação superior
    topFrame = Ctk.CTkFrame(menu_inicial, fg_color=current_theme["accent"], height=60)
    topFrame.pack(side="top", fill="x")

    # Rótulo de cabeçalho
    homeLabel = Ctk.CTkLabel(topFrame, text="SwanShine", font=("Bahnschrift", 15), fg_color=current_theme["accent"], text_color=current_theme["background"], height=60, padx=20)
    homeLabel.pack(side="right", padx=10)

    # Botão de Navbar
    navbarBtn = Ctk.CTkButton(topFrame, image=navIcon, fg_color=current_theme["button_color"], hover_color=current_theme["accent"], command=switch, width=40, height=40, text="")
    navbarBtn.place(x=10, y=10)

    # Botão para alternar o tema e verificar atualizações
    theme_button = Ctk.CTkButton(topFrame, text="Tema Escuro", command=toggle_theme, width=100)
    theme_button.pack(side="left", padx=10)

    check_updates_button = Ctk.CTkButton(topFrame, text="Verificar Atualizações", command=check_for_updates, width=150)
    check_updates_button.pack(side="left", padx=10)

# Chama a função principal para criar o menu inicial
if __name__ == "__main__":
    menu_inicial()
# Função para conectar ao banco de dados
def conectar_bd():
    try:
        conn = mysql.connector.connect(
            host="swanshine.cpkoaos0ad68.us-east-2.rds.amazonaws.com",
            user="admin",
            password="gLAHqWkvUoaxwBnm9wKD",
            database="swanshine"
        )
        cursor = conn.cursor()
        return conn, cursor
    except mysql.connector.Error as erro:
        messagebox.showerror("Erro de Conexão", f"Erro ao conectar ao MySQL: {erro}")
        return None, None

# Função para abrir a tela administrativa
def tela_administrativa():
    global janela_admin
    if 'janela_admin' in globals() and janela_admin.winfo_exists():
        janela_admin.lift()
        return

    print("Abrindo tela administrativa...")

    def exibir_registros():
        conn, cursor = conectar_bd()
        if conn and cursor:
            try:
                cursor.execute("SELECT Id_clientes, CPF, Email, Endereco, Nome, Telefone FROM clientes")
                rows = cursor.fetchall()
                for row in tree.get_children():
                    tree.delete(row)
                for row in rows:
                    tree.insert('', 'end', values=row)
            except mysql.connector.Error as erro:
                messagebox.showerror("Erro", f"Erro ao exibir registros: {erro}")
            finally:
                conn.close()

    def adicionar_registro():
        cpf = entry_cpf.get()
        email = entry_email.get()
        endereco = entry_endereco.get()
        nome = entry_nome.get()
        telefone = entry_telefone.get()
        if not all([cpf, email, endereco, nome, telefone]):
            messagebox.showwarning("Campos Inválidos", "Todos os campos devem ser preenchidos.")
            return
        conn, cursor = conectar_bd()
        if conn and cursor:
            try:
                cursor.execute("INSERT INTO clientes (CPF, Email, Endereco, Nome, Telefone) VALUES (%s, %s, %s, %s, %s)", (cpf, email, endereco, nome, telefone))
                conn.commit()
                exibir_registros()
            except mysql.connector.Error as erro:
                messagebox.showerror("Erro", f"Erro ao adicionar registro: {erro}")
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
                    messagebox.showerror("Erro", f"Erro ao deletar registro: {erro}")
                finally:
                    conn.close()

    def editar_registro():
        selected_item = tree.selection()
        novo_valor = entry_novo_valor.get()
        campo = combo_campos.get()
        if not (selected_item and novo_valor and campo):
            messagebox.showwarning("Campos Inválidos", "Selecione um registro e preencha o novo valor e campo.")
            return
        conn, cursor = conectar_bd()
        if conn and cursor:
            try:
                for item in selected_item:
                    id_registro = tree.item(item, 'values')[0]
                    cursor.execute(f"UPDATE clientes SET {campo}=%s WHERE Id_clientes=%s", (novo_valor, id_registro))
                    conn.commit()
                    valores_atuais = list(tree.item(item, 'values'))
                    indice_campo = ['Id_clientes', 'CPF', 'Email', 'Endereco', 'Nome', 'Telefone'].index(campo)
                    valores_atuais[indice_campo] = novo_valor
                    tree.item(item, values=valores_atuais)
            except mysql.connector.Error as erro:
                messagebox.showerror("Erro", f"Erro ao editar registro: {erro}")
            finally:
                conn.close()

    def filtrar_por_id_cliente():
        id_cliente = entry_id_cliente.get()
        if not id_cliente:
            messagebox.showwarning("Campo Vazio", "O ID do cliente deve ser preenchido.")
            return
        conn, cursor = conectar_bd()
        if conn and cursor:
            try:
                cursor.execute("SELECT Id_clientes, CPF, Email, Endereco, Nome, Telefone FROM clientes WHERE Id_clientes = %s", (id_cliente,))
                rows = cursor.fetchall()
                for row in tree.get_children():
                    tree.delete(row)
                for row in rows:
                    tree.insert('', 'end', values=row)
            except mysql.connector.Error as erro:
                messagebox.showerror("Erro", f"Erro ao filtrar por ID Cliente: {erro}")
            finally:
                conn.close()

    def fechar_janela_admin():
        global janela_admin
        janela_admin.destroy()
        del janela_admin

    janela_admin = Ctk.CTkToplevel(menu_inicial)
    janela_admin.title("Consulta e Edição de Registros")
    janela_admin.geometry("1280x720")

    frame_input = Ctk.CTkFrame(janela_admin)
    frame_input.pack(pady=10, padx=10, fill='x')

    labels = ['Nome', 'CPF', 'Email', 'Endereço', 'Telefone', 'Campo', 'Novo Valor', 'Filtrar por ID Cliente']
    entries = {}
    for i, label in enumerate(labels):
        Ctk.CTkLabel(frame_input, text=label).grid(row=i, column=0, padx=5, pady=5, sticky='e')
        if label == 'Campo':
            campos_disponiveis = ['Id_clientes', 'CPF', 'Email', 'Endereco', 'Nome', 'Telefone']
            combo_campos = Ctk.CTkComboBox(frame_input, values=campos_disponiveis, width=27)
            combo_campos.grid(row=i, column=1, padx=5, pady=5)
        else:
            entries[label] = Ctk.CTkEntry(frame_input, width=30)
            entries[label].grid(row=i, column=1, padx=5, pady=5)

    entry_nome, entry_cpf, entry_email, entry_endereco, entry_telefone, entry_novo_valor, entry_id_cliente = (
        entries['Nome'], entries['CPF'], entries['Email'], entries['Endereço'], entries['Telefone'], 
        entries['Novo Valor'], entries['Filtrar por ID Cliente']
    )

    btn_adicionar = Ctk.CTkButton(frame_input, text="Adicionar", command=adicionar_registro)
    btn_adicionar.grid(row=len(labels), column=1, padx=5, pady=5, sticky='e')

    frame_botoes = Ctk.CTkFrame(janela_admin)
    frame_botoes.pack(pady=10)

    btn_editar = Ctk.CTkButton(frame_botoes, text="Editar Campo Selecionado", command=editar_registro)
    btn_editar.grid(row=0, column=0, padx=10)

    btn_filtrar = Ctk.CTkButton(frame_botoes, text="Filtrar por ID Cliente", command=filtrar_por_id_cliente)
    btn_filtrar.grid(row=0, column=1, padx=10)

    tree = tk.Treeview(janela_admin, columns=('Id_clientes', 'CPF', 'Email', 'Endereco', 'Nome', 'Telefone'), show='headings')
    tree.heading('Id_clientes', text='ID')
    tree.heading('CPF', text='CPF')
    tree.heading('Email', text='Email')
    tree.heading('Endereco', text='Endereço')
    tree.heading('Nome', text='Nome')
    tree.heading('Telefone', text='Telefone')
    tree.pack(fill='both', expand=True, pady=10)

    frame_botoes_inferiores = Ctk.CTkFrame(janela_admin)
    frame_botoes_inferiores.pack(pady=10)

    btn_atualizar = Ctk.CTkButton(frame_botoes_inferiores, text="Atualizar Lista", command=exibir_registros)
    btn_atualizar.grid(row=0, column=0, padx=20)

    btn_deletar = Ctk.CTkButton(frame_botoes_inferiores, text="Deletar Selecionado", command=deletar_registro)
    btn_deletar.grid(row=0, column=1, padx=20)
    
    btn_voltar = Ctk.CTkButton(frame_botoes_inferiores, text="Voltar", command=fechar_janela_admin)
    btn_voltar.grid(row=0, column=2, padx=20)

    exibir_registros()

# Função para abrir a tela de configurações
def tela_configuracoes():
    global janela_configuracoes
    if 'janela_configuracoes' in globals() and janela_configuracoes.winfo_exists():
        janela_configuracoes.lift()
        return

    print("Abrindo tela de configurações...")

    def salvar_configuracoes():
        toggle_theme()

    def buscar_atualizacoes():
        check_for_updates()

    janela_configuracoes = Ctk.CTkToplevel(menu_inicial)
    janela_configuracoes.title("Configurações")
    janela_configuracoes.geometry("400x300")

    Ctk.CTkLabel(janela_configuracoes, text="Configurações").pack(pady=10)

    global theme_button
    theme_button = Ctk.CTkButton(janela_configuracoes, text="Tema Claro", command=salvar_configuracoes)
    theme_button.pack(pady=10)

    update_button = Ctk.CTkButton(janela_configuracoes, text="Buscar Atualizações", command=buscar_atualizacoes)
    update_button.pack(pady=10)

    close_button = Ctk.CTkButton(janela_configuracoes, text="Fechar", command=janela_configuracoes.destroy)
    close_button.pack(pady=10)

# Adicionar funcionalidade ao botão "Configurações" no Navbar
for button in navmenu_inicial.winfo_children():
    if button.cget("text") == "Configurações":
        button.configure(command=tela_configuracoes)

# Adicionar funcionalidade ao botão "Administração" no Navbar
for button in navmenu_inicial.winfo_children():
    if button.cget("text") == "Administração":
        button.configure(command=tela_administrativa)


# Função para fazer login
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

        if cursor.fetchone():
            return True
        else:
            return False

    except mysql.connector.Error as erro:
        print("Erro ao conectar ao MySQL:", erro)
        return False

    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

# Função para validar o login
def validar_login():
    usuario = input_usuario.get()
    senha = input_senha.get()

    if login(usuario, senha):
        messagebox.showinfo("Login", "Login bem-sucedido!")
        return True
    else:
        messagebox.showerror("Login", "Login falhou. Verifique suas credenciais.")
        return False
    
def validar_login_print():
    usuario = input_usuario.get()
    senha = input_senha.get()

    if login(usuario, senha):
        print("Login", "Login bem-sucedido!")
        return True
    else:
        print("Login", "Login falhou. Verifique suas credenciais.")
        return False

def login_valido_tela_selecionar_usuario():
    try:
        if validar_login():
            tela_administrativa()
    except validar_login: 
        janela_principal.withdraw()  
        messagebox.showerror("Login", "Login falhou. Verifique suas credenciais.")
    finally:
        if validar_login_print():
            janela_principal.withdraw()
        pass

#Configuração da tela
janela_principal = Ctk.CTk()
janela_principal._set_appearance_mode("System")
janela_principal.geometry("500x500")
janela_principal.title("Login")
janela_principal.maxsize(width=500, height=500)
janela_principal.minsize(width=500, height=500)

# Tela
rightframe = Frame(janela_principal, width=250, height=500, relief="raise", bg="orange")
rightframe.pack(side="right", fill="both")

label_usuario = Ctk.CTkLabel(rightframe, width=250, height=50, text="Usuario", font=("Inter-Regular", 16,"italic"))
label_usuario.pack(pady=10)

input_usuario = Ctk.CTkEntry(rightframe, width=250, height=50, fg_color="white", font=("Inter-Regular", 16, "italic"))
input_usuario.pack(pady=10)

label_senha = Ctk.CTkLabel(rightframe, width=250, height=50, text="Senha", font=("Inter-Regular", 16, "italic"))
label_senha.pack(pady=10)

input_senha = Ctk.CTkEntry(rightframe, width=250, height=50, fg_color="white", font=("Inter-Regular", 16, "italic"))
input_senha.pack(pady=10)

button_entrar = Ctk.CTkButton(rightframe, text="Entrar!", fg_color="black", command=login_valido_tela_selecionar_usuario, font=("Inter-Regular", 16, "italic"))
button_entrar.place(x=50, y=330)

leftframe = Frame(janela_principal, width=250, height=500, relief="raise", bg="orange")
leftframe.pack(side="left", fill="both")

label_imagem = CTkLabel(leftframe, width=250, height=250, text="")
label_imagem.place(x=-100, y=-10)

janela_principal.mainloop()
# Iniciar o loop principal da janela

