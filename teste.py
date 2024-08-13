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
        cursor = conn.cursor()
        if conn.is_connected():
            print("Conectado ao banco de dados")
        return conn, cursor
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None, None

def open_administracao():
    def exibir_registros():
        conn, cursor = conectar_bd()
        if conn and cursor:
            try:
                tabela_selecionada = combo_tabelas.get()
                query = {
                    "admins": "SELECT Id, Nome, Usuario, Senha FROM admins",
                    "clientes": "SELECT Id_clientes, Nome, Endereço, Email, cpf, Telefone, senha FROM clientes",
                    "imagens": "SELECT id, descricao FROM imagens",
                    "profissionais": "SELECT id, nome, email, cpf FROM profissionais",
                    "serv_pro": "SELECT d_profissionais FROM serv_pro",
                    "serviços": "SELECT Nome, Preço, Descrição, Id_clientes, id_profissionais FROM serviços"
                }
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

        if combo_tabelas.get() == "clientes":
            if not all([nome, endereco, email, cpf, telefone, senha]):
                messagebox.showwarning("Campos Vazios", "Por favor, preencha todos os campos antes de adicionar.")
                return
            query = "INSERT INTO clientes (Nome, Endereço, Email, cpf, Telefone, senha) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (nome, endereco, email, cpf, telefone, senha)
        elif combo_tabelas.get() == "admins":
            if not all([nome, usuario, senha]):
                messagebox.showwarning("Campos Vazios", "Por favor, preencha todos os campos antes de adicionar.")
                return
            query = "INSERT INTO admins (Nome, Usuario, Senha) VALUES (%s, %s, %s)"
            values = (nome, usuario, senha)
        elif combo_tabelas.get() == "profissionais":
            if not all([nome, email, cpf]):
                messagebox.showwarning("Campos Vazios", "Por favor, preencha todos os campos antes de adicionar.")
                return
            query = "INSERT INTO profissionais (nome, email, cpf) VALUES (%s, %s, %s)"
            values = (nome, email, cpf)
        else:
            messagebox.showwarning("Tabela Não Suportada", "Adicionar registros não é suportado para esta tabela.")
            return
        
        if messagebox.askokcancel("Confirmação", "Você realmente deseja adicionar este registro?"):
            conn, cursor = conectar_bd()
            if conn and cursor:
                try:
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
            conn, cursor = conectar_bd()
            if conn and cursor:
                try:
                    tabela_selecionada = combo_tabelas.get()
                    for item in selected_item:
                        id_registro = tree.item(item, 'values')[0]
                        if tabela_selecionada == "clientes":
                            cursor.execute("DELETE FROM clientes WHERE Id_clientes=%s", (id_registro,))
                        elif tabela_selecionada == "admins":
                            cursor.execute("DELETE FROM admins WHERE Id=%s", (id_registro,))
                        elif tabela_selecionada == "profissionais":
                            cursor.execute("DELETE FROM profissionais WHERE id=%s", (id_registro,))
                        # Adicione lógica para outras tabelas conforme necessário
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
                conn, cursor = conectar_bd()
                if conn and cursor:
                    try:
                        tabela_selecionada = combo_tabelas.get()
                        for item in selected_item:
                            id_registro = tree.item(item, 'values')[0]
                            if tabela_selecionada == "clientes":
                                cursor.execute(f"UPDATE clientes SET {campo}=%s WHERE Id_clientes=%s", (novo_valor, id_registro))
                            elif tabela_selecionada == "admins":
                                cursor.execute(f"UPDATE admins SET {campo}=%s WHERE Id=%s", (novo_valor, id_registro))
                            elif tabela_selecionada == "profissionais":
                                cursor.execute(f"UPDATE profissionais SET {campo}=%s WHERE id=%s", (novo_valor, id_registro))
                            # Adicione lógica para outras tabelas conforme necessário
                            conn.commit()
                            valores_atuais = list(tree.item(item, 'values'))
                            indice_campo = tree["columns"].index(campo)
                            valores_atuais[indice_campo] = novo_valor
                            tree.item(item, values=valores_atuais)
                    except Error as e:
                        print(f"Erro ao editar registro: {e}")
                    finally:
                        conn.close()

    def filtrar_por_id_cliente():
        id_cliente = entry_id_cliente.get()
        conn, cursor = conectar_bd()
        if conn and cursor:
            try:
                tabela_selecionada = combo_tabelas.get()
                if tabela_selecionada == "clientes":
                    cursor.execute("SELECT Id_clientes, Nome, Endereço, Email, cpf, Telefone, senha FROM clientes WHERE Id_clientes = %s", (id_cliente,))
                # Adicione lógica para filtrar outras tabelas conforme necessário
                rows = cursor.fetchall()
                for row in tree.get_children():
                    tree.delete(row)
                for row in rows:
                    tree.insert('', 'end', values=row)
            except Error as e:
                print(f"Erro ao filtrar registros: {e}")
            finally:
                conn.close()

    def fechar_janela_admin():
        janela_administracao.destroy()

    janela_administracao = tk.Tk()
    janela_administracao.title("Consulta e Edição de Registros")
    janela_administracao.geometry("1280x720")

    estilo = ttk.Style()
    estilo.theme_use('clam')

    frame_input = ttk.Frame(janela_administracao)
    frame_input.pack(pady=10, padx=10, fill='x')

    labels = ['Nome', 'CPF', 'Email', 'Endereço', 'Telefone', 'Campo', 'Novo Valor', 'Filtrar por ID Cliente', 'Selecionar Tabela', 'Usuário', 'Senha']
    entries = {}
    for i, label in enumerate(labels):
        ttk.Label(frame_input, text=label).grid(row=i, column=0, padx=5, pady=5, sticky='e')
        if label == 'Campo':
            campos_disponiveis = ['cpf', 'Email', 'Endereço', 'Nome', 'Telefone', 'Usuario', 'Senha']
            combo_campos = ttk.Combobox(frame_input, values=campos_disponiveis, width=27)
            combo_campos.grid(row=i, column=1, padx=5, pady=5)
        elif label == 'Selecionar Tabela':
            tabelas_disponiveis = ['admins', 'clientes', 'imagens', 'profissionais', 'serv_pro', 'serviços']
            combo_tabelas = ttk.Combobox(frame_input, values=tabelas_disponiveis, width=27)
            combo_tabelas.grid(row=i, column=1, padx=5, pady=5)
            combo_tabelas.current(0)  # Seleciona a primeira tabela por padrão
        else:
            entries[label] = ttk.Entry(frame_input, width=30)
            entries[label].grid(row=i, column=1, padx=5, pady=5)

    entry_nome = entries['Nome']
    entry_cpf = entries['CPF']
    entry_email = entries['Email']
    entry_endereco = entries['Endereço']
    entry_telefone = entries['Telefone']
    entry_novo_valor = entries['Novo Valor']
    entry_id_cliente = entries['Filtrar por ID Cliente']
    entry_usuario = entries['Usuário']
    entry_senha = entries['Senha']

    tree = ttk.Treeview(janela_administracao, columns=(1, 2, 3, 4, 5, 6, 7, 8, 9), show='headings')
    tree.pack(pady=20, padx=20, fill='both', expand=True)

    for col in tree['columns']:
        tree.heading(col, text=col)

    frame_botoes = ttk.Frame(janela_administracao)
    frame_botoes.pack(pady=10, padx=10)

    botoes = [
        ('Adicionar', adicionar_registro),
        ('Deletar', deletar_registro),
        ('Editar', editar_registro),
        ('Filtrar', filtrar_por_id_cliente),
        ('Exibir', exibir_registros),
        ('Fechar', fechar_janela_admin)
    ]

    for i, (nome_botao, comando) in enumerate(botoes):
        ttk.Button(frame_botoes, text=nome_botao, command=comando).grid(row=0, column=i, padx=5, pady=5)

    exibir_registros()
    janela_administracao.mainloop()

if __name__ == "__main__":
    open_administracao()
