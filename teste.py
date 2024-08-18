import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error

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
            for row in tree.get_children():
                tree.delete(row)
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
ttk.Button(frame_botoes, text="Fechar", command=fechar_janela_admin).pack(side='right', padx=5)
ttk.Button(frame_botoes, text="Atualizar", command=exibir_registros).pack(side='right', padx=5)

# Aba Adicionar
labels_adicionar = ['Nome', 'CPF', 'Email', 'endereco', 'Telefone', 'Usuário', 'Senha']
entries_adicionar = {}
for i, label in enumerate(labels_adicionar):
    ttk.Label(aba_adicionar, text=label).grid(row=i, column=0, padx=5, pady=5, sticky='e')
    entries_adicionar[label] = ttk.Entry(aba_adicionar, width=30)
    entries_adicionar[label].grid(row=i, column=1, padx=5, pady=5)

entry_nome = entries_adicionar['Nome']
entry_cpf = entries_adicionar['CPF']
entry_email = entries_adicionar['Email']
entry_endereco = entries_adicionar['endereco']
entry_telefone = entries_adicionar['Telefone']
entry_usuario = entries_adicionar['Usuário']
entry_senha = entries_adicionar['Senha']

ttk.Button(aba_adicionar, text="Adicionar", command=adicionar_registro).grid(row=len(labels_adicionar), column=1, pady=10)

# Aba Deletar
ttk.Button(aba_deletar, text="Deletar", command=deletar_registro).pack(pady=10)

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


ttk.Button(aba_editar, text="Editar", command=editar_registro).grid(row=len(labels_editar), column=1, pady=10)

exibir_registros()
janela_administracao.mainloop()
