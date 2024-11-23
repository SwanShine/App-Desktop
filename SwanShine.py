import tkinter as tk
from tkinter import Frame, PhotoImage, messagebox, ttk
import mysql.connector
from mysql.connector import Error
import customtkinter as Ctk
from customtkinter import CTkCanvas, CTkLabel, CTkEntry, CTkButton, CTkToplevel
from customtkinter import *
import PIL
from PIL import Image
from PIL import Image, ImageTk  
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
    usuario = input_usuario.get()  # Obtém o valor do campo de usuário
    senha = input_senha.get()  # Obtém o valor do campo de senha

    try:
        # Verifica se o login é válido
        if login(usuario, senha):
            tela_login.withdraw()  # Fecha a tela de login
            menu_inicial()  # Abre o menu inicial
        else:
            # Caso o login falhe, exibe uma mensagem de erro
            messagebox.showerror("Login", "Login falhou. Verifique suas credenciais.")
            initialize_window()  # Reabre a tela de login para nova tentativa
    except Exception as e:
        # Em caso de erro durante o processo, exibe uma mensagem de erro com a descrição
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
    finally:
        # adicionar qualquer operação de limpeza ou finalização necessária
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
        texto_sobre = CTkLabel(janela_sobre, text="Esse App é um exemplo de como funcionaria o sistema de administração Swan Shine",font=("Bahnschrift", 15))
        texto_sobre.pack(pady=(0, 5))
        
        texto_sobre1 = CTkLabel(janela_sobre, text="Competências e Capacidades", font=("Bahnschrift", 15))
        texto_sobre1.pack(pady=(0, 5))
        
        texto_sobre2 = CTkLabel(janela_sobre, text="Aplicativo destinado a administradores e gerentes Swan Shine",font=("Bahnschrift", 15))
        texto_sobre2.pack(pady=(0, 5))
        
        texto_sobre3 = CTkLabel(janela_sobre, text="Funções: Editar, Excluir e Adicionar",font=("Bahnschrift", 15))
        texto_sobre3.pack(pady=(10, 0))

def sair_menu():
    resposta = messagebox.askyesno("Confirmar Saída", "Você realmente deseja sair?",)
    if resposta:
        menu_inicial.quit()  # Fecha a aplicação

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

# Função para atualizar o Treeview com registros
def atualizar_treeview(cursor, rows):
    # Limpa o treeview
    for item in tree.get_children():
        tree.delete(item)

    # Atualiza as colunas do treeview
    colunas = [desc[0] for desc in cursor.description]
    tree["columns"] = colunas
    tree["show"] = "headings"

    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, width=120)

    # Insere os registros no Treeview
    for row in rows:
        tree.insert("", "end", values=row)

# Variável global para controle de exibição de senha
senha_censurada = True

# Função para obter o próximo ID disponível
def obter_proximo_id(tabela):
    conn = conectar_bd()
    if not conn:
        return None

    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT MAX(id) FROM {tabela}")
        max_id = cursor.fetchone()[0]  # Obtém o maior ID atual
        return max_id + 1 if max_id else 1  # Se não houver ID, inicia com 1
    except Error as e:
        messagebox.showerror("Erro ao obter ID", f"Erro: {e}")
        return None
    finally:
        conn.close()

def remover_nao_numericos(valor):
    """Remove todos os caracteres não numéricos da string."""
    return re.sub(r'\D', '', valor)

def aplicar_mascara(valor, tipo):
    """Aplica a máscara no valor de acordo com o tipo fornecido."""
    # Remove caracteres não numéricos
    valor = remover_nao_numericos(valor)
    
    if tipo == 'cpf':
        # Validação de comprimento para CPF (11 dígitos)
        if len(valor) == 11:
            return re.sub(r'(\d{3})(\d{3})(\d{3})(\d{2})', r'\1.\2.\3-\4', valor)
    
    elif tipo == 'telefone':
        # Validação de comprimento para telefone (10 ou 11 dígitos)
        if len(valor) == 10:  # Para números de telefone fixo
            return re.sub(r'(\d{2})(\d{4})(\d{4})', r'(\1) \2-\3', valor)
        elif len(valor) == 11:  # Para números de telefone celular
            return re.sub(r'(\d{2})(\d{5})(\d{4})', r'(\1) \2-\3', valor)
    
    elif tipo == 'cep':
        # Validação de comprimento para CEP (8 dígitos)
        if len(valor) == 8:
            return re.sub(r'(\d{5})(\d{3})', r'\1-\2', valor)
    
    # Retorna o valor sem máscara caso não tenha o comprimento esperado
    return valor

# Função para aplicar máscara no campo CPF
def mascara_cpf(event):
    cpf = event.widget.get()
    cpf_formatado = re.sub(r'(\d{3})(\d{3})(\d{3})(\d{2})', r'\1.\2.\3-\4', cpf)
    event.widget.delete(0, tk.END)
    event.widget.insert(0, cpf_formatado)

# Função para aplicar máscara no campo Telefone
def mascara_telefone(event):
    telefone = event.widget.get()
    telefone_formatado = re.sub(r'(\d{2})(\d{4})(\d{4})', r'(\1) \2-\3', telefone)
    event.widget.delete(0, tk.END)
    event.widget.insert(0, telefone_formatado)

# Função para aplicar máscara no campo CEP
def mascara_cep(event):
    cep = event.widget.get()
    cep_formatado = re.sub(r'(\d{5})(\d{3})', r'\1-\2', cep)
    event.widget.delete(0, tk.END)
    event.widget.insert(0, cep_formatado)

# Função para adicionar novos registros
def atualizar_aba_adicionar():
    # Remove todos os widgets existentes no frame
    for widget in frame_adicionar.winfo_children():
        widget.destroy()

    # Obtém a tabela selecionada no combobox
    tabela_selecionada = combo_tabelas.get()

    # Dicionário com os campos para cada tabela
    campos_por_tabela = {
        "clientes": [("Nome", "nome"), ("Endereço", "endereco"), ("Email", "email"),
                     ("CPF", "cpf"), ("Telefone", "telefone"), ("Gênero", "genero"),
                     ("Senha", "senha"), ("CEP", "cep")],
        "admins": [("Nome", "nome"), ("Usuário", "usuario"), ("Senha", "senha")],
        "profissionais": [
            ("Nome", "nome"),
            ("Email", "email"),
            ("Endereço", "endereco"),  # Novo campo adicionado aqui
            ("CPF", "cpf"),
            ("Senha", "senha"),
            ("Celular", "celular"),
            ("Gênero", "genero"),
            ("CEP", "cep")
        ]
    }

    # Obtém os campos da tabela selecionada
    campos = campos_por_tabela.get(tabela_selecionada, [])

    # Dicionário para armazenar as entradas
    entradas = {}

    # Definir as colunas por grupo (exemplo: dois campos por linha)
    campos_por_linha = 2  # Ajuste o número de campos por linha

    # Cria os widgets para cada campo
    for i, (label_text, entry_name) in enumerate(campos):
        # Calcula em qual linha e coluna o campo vai ser posicionado
        linha = i // campos_por_linha  # Divide a quantidade de campos por linha
        coluna = i % campos_por_linha  # Alterna entre as colunas (0 ou 1)

        # Cria o label
        ttk.Label(frame_adicionar, text=label_text).grid(row=linha, column=coluna * 2, padx=5, pady=5, sticky='e')
        
        # Cria a entrada
        entrada = ttk.Entry(frame_adicionar, width=30)

        # Aplica as máscaras específicas aos campos
        if entry_name == "cpf":
            entrada.bind("<KeyRelease>", mascara_cpf)
        elif entry_name == "telefone":
            entrada.bind("<KeyRelease>", mascara_telefone)
        elif entry_name == "cep":
            entrada.bind("<KeyRelease>", mascara_cep)

        # Cria a entrada ao lado do label
        entrada.grid(row=linha, column=coluna * 2 + 1, padx=5, pady=5)
        
        # Armazena a entrada no dicionário
        entradas[entry_name] = entrada

    # Botão para adicionar o registro
    ttk.Button(frame_adicionar, text="Adicionar Registro", 
               command=lambda: adicionar_registro(tabela_selecionada, entradas)).grid(row=linha + 1, columnspan=2, pady=10)

    # Ajusta o comportamento das colunas para ocupar menos espaço (de acordo com o conteúdo)
    for col in range(4):  # Agora temos 4 colunas para os labels e entradas (2 por linha)
        frame_adicionar.grid_columnconfigure(col, weight=1, minsize=150)

# Função para adicionar registro ao banco com verificação
def adicionar_registro(tabela, entradas):
    # Pergunta ao usuário se deseja adicionar o registro
    confirmar = messagebox.askyesno("Confirmação", "Deseja realmente adicionar este registro?")
    if not confirmar:
        return  # Sai da função caso o usuário cancele
    conn = conectar_bd()
    if not conn:
        return
    try:
        cursor = conn.cursor()

        # Extrai os valores das entradas
        valores = {campo: entrada.get() for campo, entrada in entradas.items()}

        # Obter o próximo ID disponível
        proximo_id = obter_proximo_id(tabela)
        if not proximo_id:
            return

        # Adiciona o id ao dicionário de valores
        valores['id'] = proximo_id

        # Cria a query de inserção dinamicamente (agora incluindo o 'id' manualmente)
        campos = ", ".join(valores.keys())
        placeholders = ", ".join(["%s" for _ in valores])
        query = f"INSERT INTO {tabela} ({campos}) VALUES ({placeholders})"

        # Executa a query
        cursor.execute(query, tuple(valores.values()))
        conn.commit()

        messagebox.showinfo("Sucesso", "Registro adicionado com sucesso!")
        
        # Atualiza a exibição da tabela após a inserção
        exibir_registros()
    except Error as e:
        messagebox.showerror("Erro ao adicionar registro", f"Erro: {e}")
    finally:
        # Fecha a conexão com o banco
        conn.close()

# Função para aplicar máscara no campo CPF
def mascara_cpf(event):
    cpf = event.widget.get()
    cpf_formatado = re.sub(r'(\d{3})(\d{3})(\d{3})(\d{2})', r'\1.\2.\3-\4', cpf)
    event.widget.delete(0, tk.END)
    event.widget.insert(0, cpf_formatado)

# Função para aplicar máscara no campo Telefone
def mascara_telefone(event):
    telefone = event.widget.get()
    telefone_formatado = re.sub(r'(\d{2})(\d{4})(\d{4})', r'(\1) \2-\3', telefone)
    event.widget.delete(0, tk.END)
    event.widget.insert(0, telefone_formatado)

# Função para aplicar máscara no campo CEP
def mascara_cep(event):
    cep = event.widget.get()
    cep_formatado = re.sub(r'(\d{5})(\d{3})', r'\1-\2', cep)
    event.widget.delete(0, tk.END)
    event.widget.insert(0, cep_formatado)

# Função para atualizar registros existentes
def atualizar_aba_editar():
    # Remove todos os widgets existentes no frame
    for widget in frame_editar.winfo_children():
        widget.destroy()

    # Obtém a tabela selecionada no combobox
    tabela_selecionada = combo_tabelas.get()

    # Dicionário com os campos para cada tabela
    campos_por_tabela = {
        "clientes": [("Nome", "nome"), ("Endereço", "endereco"), ("Email", "email"),
                     ("CPF", "cpf"), ("Telefone", "telefone"), ("Gênero", "genero"),
                     ("Senha", "senha"), ("CEP", "cep")],
        "admins": [("Nome", "nome"), ("Usuário", "usuario"), ("Senha", "senha")],
        "profissionais": [
            ("Nome", "nome"),
            ("Email", "email"),
            ("Endereço", "endereco"),  # Novo campo adicionado aqui
            ("CPF", "cpf"),
            ("Senha", "senha"),
            ("Celular", "celular"),
            ("Gênero", "genero"),
            ("CEP", "cep")
        ]
    }

    # Obtém os campos da tabela selecionada
    campos = campos_por_tabela.get(tabela_selecionada, [])

    # Dicionário para armazenar as entradas
    entradas = {}

    # Definir as colunas por grupo (exemplo: dois campos por linha)
    campos_por_linha = 2  # Ajuste o número de campos por linha

    # Cria os widgets para o campo de ID, tratando-o como um campo normal
    ttk.Label(frame_editar, text="ID do Registro").grid(row=0, column=0, padx=5, pady=5, sticky='e')
    entrada_id = ttk.Entry(frame_editar, width=30)
    entrada_id.grid(row=0, column=1, padx=5, pady=5)
    entradas['id'] = entrada_id  # Armazena a entrada do ID

    # Cria os widgets para os campos da tabela
    for i, (label_text, entry_name) in enumerate(campos, start=1):
        # Calcula em qual linha e coluna o campo vai ser posicionado
        linha = (i + 1) // campos_por_linha  # A linha começa em 1, pois o ID já ocupa a primeira linha
        coluna = (i + 1) % campos_por_linha  # Alterna entre as colunas (0 ou 1)

        # Cria o label
        ttk.Label(frame_editar, text=label_text).grid(row=linha, column=coluna * 2, padx=5, pady=5, sticky='e')
        
        # Cria a entrada
        entrada = ttk.Entry(frame_editar, width=30)

        # Aplica as máscaras específicas aos campos
        if entry_name == "cpf":
            entrada.bind("<KeyRelease>", mascara_cpf)
        elif entry_name == "telefone" or entry_name == "celular":
            entrada.bind("<KeyRelease>", mascara_telefone)
        elif entry_name == "cep":
            entrada.bind("<KeyRelease>", mascara_cep)

        # Cria a entrada ao lado do label
        entrada.grid(row=linha, column=coluna * 2 + 1, padx=5, pady=5)
        
        # Armazena a entrada no dicionário
        entradas[entry_name] = entrada

    # Botão para editar o registro
    ttk.Button(frame_editar, text="Editar Registro", 
               command=lambda: editar_registro(tabela_selecionada, entradas)).grid(row=linha + 1, columnspan=2, pady=10)



# Função para editar um registro no banco
def editar_registro(tabela, entradas):
    conn = conectar_bd()
    if not conn:
        return

    try:
        cursor = conn.cursor()

        # Extrai os valores das entradas
        valores = {campo: entrada.get() for campo, entrada in entradas.items()}

        # Obtém o ID do registro a ser editado
        id_registro = valores.get('id')
        if not id_registro:
            messagebox.showerror("Erro", "ID não fornecido para edição.")
            return

        # Filtra os valores para remover o campo 'id' da atualização
        valores_sem_id = {campo: valor for campo, valor in valores.items() if campo != 'id'}

        # Cria uma lista de campos a serem atualizados (somente os que foram preenchidos)
        campos_a_atualizar = [(campo, valor) for campo, valor in valores_sem_id.items() if valor]

        if not campos_a_atualizar:
            messagebox.showwarning("Aviso", "Nenhum campo foi alterado.")
            return

        # Solicita confirmação do usuário antes de editar
        confirmacao = messagebox.askyesno("Confirmação", "Deseja realmente editar este registro?")
        if not confirmacao:
            messagebox.showinfo("Ação cancelada", "A edição foi cancelada.")
            return

        # Cria a query de atualização dinamicamente
        set_clause = ", ".join([f"{campo} = %s" for campo, _ in campos_a_atualizar])
        query = f"UPDATE {tabela} SET {set_clause} WHERE id = %s"

        # Executa a query com os valores para os campos alterados, mais o ID
        cursor.execute(query, tuple(valor for _, valor in campos_a_atualizar) + (id_registro,))
        conn.commit()

        messagebox.showinfo("Sucesso", "Registro editado com sucesso!")
        
        # Atualiza a exibição da tabela após a edição
        exibir_registros()
    except Error as e:
        messagebox.showerror("Erro ao editar registro", f"Erro: {e}")
    finally:
        # Fecha a conexão com o banco
        conn.close()
    
# Função para configurar a aba de exclusão de registros
def atualizar_aba_deletar():
    # Remove todos os widgets existentes no frame
    for widget in frame_deletar.winfo_children():
        widget.destroy()

    # Obtém a tabela selecionada no combobox
    tabela_selecionada = combo_tabelas.get()

    # Cria o campo para inserir o ID do registro a ser deletado
    ttk.Label(frame_deletar, text="ID do Registro").grid(row=0, column=0, padx=5, pady=5, sticky='e')
    entrada_id = ttk.Entry(frame_deletar, width=30)
    entrada_id.grid(row=0, column=1, padx=5, pady=5)

    # Botão para deletar o registro
    ttk.Button(
        frame_deletar,
        text="Deletar Registro",
        command=lambda: confirmar_exclusao(tabela_selecionada, entrada_id.get())
    ).grid(row=1, columnspan=2, pady=10)

# Função para exibir a mensagem de confirmação antes de excluir
def confirmar_exclusao(tabela, id_registro):
    if not id_registro:
        messagebox.showerror("Erro", "ID não fornecido para exclusão.")
        return

    resposta = messagebox.askyesno("Confirmação", f"Tem certeza que deseja deletar o registro com ID {id_registro} da tabela '{tabela}'?")
    if resposta:
        deletar_registro(tabela, id_registro)

# Função para deletar um registro no banco
def deletar_registro(tabela, id_registro):
    conn = conectar_bd()
    if not conn:
        return
    try:
        cursor = conn.cursor()

        # Query para deletar o registro pelo ID
        query = f"DELETE FROM {tabela} WHERE id = %s"

        # Executa a query
        cursor.execute(query, (id_registro,))
        conn.commit()

        if cursor.rowcount > 0:
            messagebox.showinfo("Sucesso", "Registro deletado com sucesso!")
        else:
            messagebox.showwarning("Aviso", "Nenhum registro encontrado com o ID fornecido.")
        
        # Atualiza a exibição da tabela após a exclusão
        exibir_registros()
    except Error as e:
        messagebox.showerror("Erro ao deletar registro", f"Erro: {e}")
    finally:
        # Fecha a conexão com o banco
        conn.close()

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
                "clientes": f"SELECT id, Nome, endereco, cep, email, cpf, telefone, genero, {'REPEAT(\'*\', CHAR_LENGTH(senha)) AS senha' if senha_censurada else 'senha'} FROM clientes",
                "profissionais": f"SELECT id, nome, endereco, email, cpf, {'REPEAT(\'*\', CHAR_LENGTH(senha)) AS senha' if senha_censurada else 'senha'}, celular, genero, cep FROM profissionais"  # Campo 'endereco' adicionado
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
            atualizar_aba_adicionar()
            atualizar_aba_editar()
            atualizar_aba_deletar()
 
# Função principal para criar o menu inicial
def menu_inicial():
    global menu_inicial, navmenu_inicial, topFrame, homeLabel, theme_button, navIcon, closeIcon
    global combo_tabelas, frame_adicionar, tree, frame_exibir, entry_id_cliente, notebook, frame_editar, aba_adicionar, aba_deletar, frame_deletar

    # Função para alternar a exibição da senha
    def alternar_senha():
        global senha_censurada
        senha_censurada = not senha_censurada
        exibir_registros()

    # Função para alternar a visibilidade da barra lateral
    def toggle_sidebar():
        if navmenu_inicial.winfo_x() < 0:
            navmenu_inicial.place(x=0, y=0)
            navmenu_inicial.lift()
        else:
            navmenu_inicial.place(x=-300, y=0)
            navmenu_inicial.lower()

    # Criação da janela principal
    menu_inicial = Ctk.CTkToplevel()
    menu_inicial.title("Swan Shine")
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

    # Criação da barra lateral (Navbar) com posição fixa
    navmenu_inicial = Ctk.CTkFrame(menu_inicial, fg_color=main_color, height=720, width=300, corner_radius=10)
    navmenu_inicial.place(x=-300, y=0)  # Inicialmente fora da tela

    # Cabeçalho da barra lateral
    Ctk.CTkLabel(
        navmenu_inicial,
        text="Menu",
        font=("Bahnschrift", 18, "bold"),
        fg_color=main_color,
        text_color="white",
        height=60,
        width=300,
        corner_radius=10
    ).place(x=0, y=0)

    # Opções no Navbar
    options = ["Configurações", "Contato", "Sobre", "Sair"]
    commands = [lambda: print("Configurações"), lambda: print("Contato"), lambda: print("Sobre"), menu_inicial.destroy]

    y = 80  # Posição vertical inicial para os botões
    for option, command in zip(options, commands):
        button = Ctk.CTkButton(
            navmenu_inicial,
            text=option,
            font=("Bahnschrift", 16),
            fg_color=main_color,
            hover_color=hover_color,
            text_color="white",
            width=250,
            height=40,
            corner_radius=8,
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
        command=toggle_sidebar,  # Agora usamos toggle_sidebar para alternar
        width=40,
        height=40,
        corner_radius=20
    )
    closeBtn.place(x=250, y=10)

    # Barra superior de navegação
    topFrame = Ctk.CTkFrame(menu_inicial, fg_color=main_color, height=60)
    topFrame.pack(side="top", fill="x")

    # Rótulo do nome da aplicação na barra superior
    homeLabel = Ctk.CTkLabel(
        topFrame,
        text="SwanShine",
        font=("Bahnschrift", 18, "bold"),
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
        command=toggle_sidebar,
        width=40,
        height=40,
        text="",
        corner_radius=20
    )
    navbarBtn.place(x=10, y=10)

    # Criando a área de abas (tabs) agora na parte superior
    notebook = ttk.Notebook(menu_inicial)
    notebook.pack(pady=10, padx=10, fill='both', expand=True)

    # Abas para navegação
    aba_adicionar = ttk.Frame(notebook)
    frame_adicionar = ttk.Frame(aba_adicionar)
    frame_adicionar.pack(pady=20, padx=20, expand=True)
    notebook.add(aba_adicionar, text="Adicionar")

    aba_editar = ttk.Frame(notebook)
    frame_editar = ttk.Frame(aba_editar)
    frame_editar.pack(pady=20, padx=20, expand=True)
    notebook.add(aba_editar, text="Editar")

    aba_deletar = ttk.Frame(notebook)
    frame_deletar = ttk.Frame(aba_deletar)
    frame_deletar.pack(pady=20, padx=20, expand=True)
    notebook.add(aba_deletar, text="Deletar")

    # Frame de entrada para adicionar, editar e desativar (agora na parte superior)
    frame_input = ttk.Frame(menu_inicial)
    frame_input.pack(pady=10, padx=10, fill='x')

    # Adicionando os labels e entradas ao frame_input
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

    # Frame para exibir a tabela com scrollbar agora na parte inferior
    frame_exibir = ttk.Frame(menu_inicial)
    frame_exibir.pack(pady=10, expand=True, fill='both')

    tree_scroll = ttk.Scrollbar(frame_exibir, orient="vertical")
    tree_scroll.pack(side="right", fill="y")

    tree = ttk.Treeview(frame_exibir, columns=[], show='headings', yscrollcommand=tree_scroll.set)
    tree.pack(fill="both", expand=True)

    tree_scroll.config(command=tree.yview)

    # Associar a função 'exibir_registros' à mudança de seleção do ComboBox
    combo_tabelas.bind("<<ComboboxSelected>>", lambda event: exibir_registros())

    # Exibir os registros ao iniciar
    exibir_registros()

# Tela de Login
def tela_login():
    global tela_login, input_usuario, input_senha
    
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