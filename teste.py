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

