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