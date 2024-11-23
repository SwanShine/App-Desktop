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
                     ("Senha", "senha"),("CEP", "cep")],
        "admins": [("Nome", "nome"), ("Usuário", "usuario"), ("Senha", "senha")],
        "profissionais": [
            ("Nome", "nome"),
            ("Email", "email"),
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

    # Cria os widgets para cada campo
    for i, (label_text, entry_name) in enumerate(campos):
        ttk.Label(frame_adicionar, text=label_text).grid(row=i, column=0, padx=5, pady=5, sticky='e')
        entrada = ttk.Entry(frame_adicionar, width=30)
        entrada.grid(row=i, column=1, padx=5, pady=5)
        entradas[entry_name] = entrada

    # Botão para adicionar o registro
    ttk.Button(frame_adicionar, text="Adicionar Registro", 
               command=lambda: adicionar_registro(tabela_selecionada, entradas)).grid(row=len(campos), columnspan=2, pady=10)

# Função para adicionar registro ao banco
def adicionar_registro(tabela, entradas):
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
    except Error as e:
        messagebox.showerror("Erro ao adicionar registro", f"Erro: {e}")
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
"profissionais": f"SELECT id, nome, email, cpf, {'REPEAT(\'*\', CHAR_LENGTH(senha)) AS senha' if senha_censurada else 'senha'}, celular, genero, cep FROM profissionais"

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

    # Criação da barra lateral (Navbar) com posição fixa
    navmenu_inicial = Ctk.CTkFrame(menu_inicial, fg_color=main_color, height=720, width=300)
    navmenu_inicial.place(x=-300, y=0)  # Posição inicial fora da tela

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
    
    # Criando a área de abas (tabs) agora na parte superior
    notebook = ttk.Notebook(menu_inicial)
    notebook.pack(pady=10, padx=10, fill='both', expand=True)

    # Abas para navegação
    aba_adicionar = ttk.Frame(notebook)
    # Frame para adicionar registros
    frame_adicionar = ttk.Frame(aba_adicionar)
    frame_adicionar.pack(pady=20, padx=20, expand=True)
    aba_editar = ttk.Frame(notebook)
    aba_desativar = ttk.Frame(notebook)

    notebook.add(aba_adicionar, text="Adicionar")
    notebook.add(aba_editar, text="Editar")
    notebook.add(aba_desativar, text="Desativar")

    # Frame de entrada para adicionar, editar e desativar (agora na parte superior)
    frame_input = ttk.Frame(menu_inicial)  # Agora o frame_input está acima da tabela
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
    frame_exibir = ttk.Frame(menu_inicial)  # A tabela foi movida para a parte inferior
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

# Inicializa o menu inicial
menu_inicial()
