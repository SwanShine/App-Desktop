import tkinter as tk
from tkinter import ttk
import mysql.connector

# Função para criar a conexão com o banco de dados MySQL
def conectar_bd():
    try:
        # Conexão com o banco de dados
        conn = mysql.connector.connect(
            host="swanshine.cpkoaos0ad68.us-east-2.rds.amazonaws.com",
            user="admin",
            password="gLAHqWkvUoaxwBnm9wKD",
            database="swanshine"
        )

        # Criar um objeto cursor
        cursor = conn.cursor()

        if conn.is_connected():
            print("Conectado ao banco de dados")

        return conn, cursor

    except mysql.connector.Error as erro:
        print("Erro ao conectar ao MySQL:", erro)
        return None, None

# Função para exibir os registros na Treeview
def exibir_registros():
    conn, cursor = conectar_bd()
    if conn and cursor:
        cursor.execute("SELECT Id_clientes, CPF, Email, Endereço, Nome, Telefone FROM clientes")
        rows = cursor.fetchall()

        # Limpa a Treeview antes de inserir novos registros
        for row in tree.get_children():
            tree.delete(row)

        # Insere os novos registros na Treeview
        for row in rows:
            tree.insert('', 'end', values=row)

        conn.close()

# Função para adicionar um novo registro
def adicionar_registro():
    cpf = entry_cpf.get()
    email = entry_email.get()
    endereco = entry_endereco.get()
    nome = entry_nome.get()
    telefone = entry_telefone.get()

    conn, cursor = conectar_bd()
    if conn and cursor:
        cursor.execute("INSERT INTO clientes (CPF, Email, Endereço, Nome, Telefone) VALUES (%s, %s, %s, %s, %s)", (cpf, email, endereco, nome, telefone))
        conn.commit()
        conn.close()
        exibir_registros()

# Função para deletar um registro selecionado
def deletar_registro():
    selected_item = tree.selection()
    if selected_item:
        conn, cursor = conectar_bd()
        if conn and cursor:
            try:
                for item in selected_item:
                    # Obtém o ID do registro selecionado
                    id_registro = tree.item(item, 'values')[0]
                    cursor.execute("DELETE FROM clientes WHERE Id_clientes=%s", (id_registro,))
                    conn.commit()
                    tree.delete(item)
            except mysql.connector.Error as erro:
                print("Erro ao deletar registro:", erro)
            finally:
                conn.close()

# Função para editar um dado específico de um registro selecionado
def editar_registro():
    selected_item = tree.selection()
    novo_valor = entry_novo_valor.get()
    campo = combo_campos.get()

    if selected_item and novo_valor and campo:
        conn, cursor = conectar_bd()
        if conn and cursor:
            try:
                for item in selected_item:
                    # Obtém o ID do registro selecionado
                    id_registro = tree.item(item, 'values')[0]

                    # Atualiza o valor do campo desejado no banco de dados
                    cursor.execute(f"UPDATE clientes SET {campo}=%s WHERE Id_clientes=%s", (novo_valor, id_registro))
                    conn.commit()

                    # Atualiza a exibição na Treeview apenas para o campo editado
                    valores_atuais = list(tree.item(item, 'values'))
                    indice_campo = ['ID', 'CPF', 'Email', 'Endereço', 'Nome', 'Telefone'].index(campo)
                    valores_atuais[indice_campo] = novo_valor
                    tree.item(item, values=valores_atuais)

            except mysql.connector.Error as erro:
                print("Erro ao editar registro:", erro)
            finally:
                conn.close()

# Função para filtrar registros por Id_cliente
def filtrar_por_id_cliente():
    id_cliente = entry_id_cliente.get()
    conn, cursor = conectar_bd()
    if conn and cursor:
        cursor.execute("SELECT Id_clientes, CPF, Email, Endereço, Nome, Telefone FROM clientes WHERE Id_clientes = %s", (id_cliente,))
        rows = cursor.fetchall()

        # Limpa a Treeview antes de inserir o resultado da filtragem
        for row in tree.get_children():
            tree.delete(row)

        # Insere os registros filtrados na Treeview
        for row in rows:
            tree.insert('', 'end', values=row)

        conn.close()

# Configuração da interface gráfica
root = tk.Tk()
root.title("Consulta e Edição de Registros")

# Frame para entrada de dados
frame_input = ttk.Frame(root)
frame_input.pack(pady=10)

# Entradas de texto
label_nome = ttk.Label(frame_input, text="Nome:")
label_nome.grid(row=0, column=0, padx=5, pady=5, sticky='e')
entry_nome = ttk.Entry(frame_input, width=30)
entry_nome.grid(row=0, column=1, padx=5, pady=5)

label_cpf = ttk.Label(frame_input, text="CPF:")
label_cpf.grid(row=1, column=0, padx=5, pady=5, sticky='e')
entry_cpf = ttk.Entry(frame_input, width=30)
entry_cpf.grid(row=1, column=1, padx=5, pady=5)

label_email = ttk.Label(frame_input, text="Email:")
label_email.grid(row=2, column=0, padx=5, pady=5, sticky='e')
entry_email = ttk.Entry(frame_input, width=30)
entry_email.grid(row=2, column=1, padx=5, pady=5)

label_endereco = ttk.Label(frame_input, text="Endereço:")
label_endereco.grid(row=3, column=0, padx=5, pady=5, sticky='e')
entry_endereco = ttk.Entry(frame_input, width=30)
entry_endereco.grid(row=3, column=1, padx=5, pady=5)

label_telefone = ttk.Label(frame_input, text="Telefone:")
label_telefone.grid(row=4, column=0, padx=5, pady=5, sticky='e')
entry_telefone = ttk.Entry(frame_input, width=30)
entry_telefone.grid(row=4, column=1, padx=5, pady=5)

# Combobox para selecionar o campo a ser editado
label_campos = ttk.Label(frame_input, text="Campo:")
label_campos.grid(row=5, column=0, padx=5, pady=5, sticky='e')
campos_disponiveis = ['Id_clientes', 'CPF', 'Email', 'Endereço', 'Nome', 'Telefone']
combo_campos = ttk.Combobox(frame_input, values=campos_disponiveis, width=27)
combo_campos.grid(row=5, column=1, padx=5, pady=5)

# Entrada de texto para o novo valor
label_novo_valor = ttk.Label(frame_input, text="Novo Valor:")
label_novo_valor.grid(row=6, column=0, padx=5, pady=5, sticky='e')
entry_novo_valor = ttk.Entry(frame_input, width=30)
entry_novo_valor.grid(row=6, column=1, padx=5, pady=5)

# Entrada de texto para filtro por ID
label_id_cliente = ttk.Label(frame_input, text="Filtrar por ID Cliente:")
label_id_cliente.grid(row=7, column=0, padx=5, pady=5, sticky='e')
entry_id_cliente = ttk.Entry(frame_input, width=10)
entry_id_cliente.grid(row=7, column=1, padx=5, pady=5)

# Botão para adicionar novo registro
btn_adicionar = ttk.Button(frame_input, text="Adicionar", command=adicionar_registro)
btn_adicionar.grid(row=8, column=1, padx=5, pady=5, sticky='e')

# Botão para editar registro selecionado
btn_editar = ttk.Button(root, text="Editar Campo Selecionado", command=editar_registro)
btn_editar.pack(pady=5)

# Botão para filtrar por ID Cliente
btn_filtrar = ttk.Button(root, text="Filtrar por ID Cliente", command=filtrar_por_id_cliente)
btn_filtrar.pack(pady=5)

# Treeview para exibir os registros
tree = ttk.Treeview(root, columns=('ID', 'CPF', 'Email', 'Endereço', 'Nome', 'Telefone'), show='headings')
tree.heading('ID', text='ID')
tree.heading('CPF', text='CPF')
tree.heading('Email', text='Email')
tree.heading('Endereço', text='Endereço')
tree.heading('Nome', text='Nome')
tree.heading('Telefone', text='Telefone')
tree.pack()

# Botão para atualizar a lista
btn_atualizar = ttk.Button(root, text="Atualizar Lista", command=exibir_registros)
btn_atualizar.pack(pady=10)

# Botão para deletar um registro selecionado
btn_deletar = ttk.Button(root, text="Deletar Selecionado", command=deletar_registro)
btn_deletar.pack()

# Exibir os registros iniciais ao abrir a aplicação
exibir_registros()

# Rodar a aplicação
root.mainloop()
