import tkinter as tk
from getpass import getpass
import mysql.connector

class GraphicalLogin:
    def __init__(self, master):
        self.master = master
        self.master.geometry("300x300")
        self.master.title("Login")
        self.master.config(bg="purple")

        self.username_label = tk.Label(master, text="Usuário:", bg="purple", fg="white")
        self.username_label.place(relx=0.05, rely=0.3)

        self.username_entry = tk.Entry(master, width=20, bd=2, bg="white")
        self.username_entry.place(relx=0.3, rely=0.3)

        self.password_label = tk.Label(master, text="Senha:", bg="purple", fg="white")
        self.password_label.place(relx=0.05, rely=0.5)

        self.password_entry = tk.Entry(master, width=20, bd=2, bg="white", show="*")
        self.password_entry.place(relx=0.3, rely=0.5)

        self.login_button = tk.Button(master, text="Login", command=self.validate_credentials)
        self.login_button.place(relx=0.4, rely=0.7)

    def consultar_adm(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="glam"
            )

            query = "SELECT glam FROM id"
            cursor = conn.cursor()
            cursor.execute(query)

            # Processar os resultados (se necessário)
            for row in cursor.fetchall():
                print(row[0])

            # Fechar a conexão
            conn.close()
        except mysql.connector.Error as err:
            print(f"Erro ao conectar ao banco de dados: {err}")
#back end
    from getpass import getpass  # Importar a função getpass para ocultar a entrada da senha

    def validate_credentials(self):
        try:
            username = self.username_entry.get()
            query = f"SELECT COUNT(1) FROM glam WHERE id = '{username}'"

            # Supondo que 'connection' seja o objeto de conexão com o MySQL
            if connection.is_connected():
                print("Conexão ao banco de dados MySQL estabelecida com sucesso!")
                cursor = connection.cursor()
                cursor.execute(query)
                result = cursor.fetchone()
                count = result[0]  # Obtendo o resultado da contagem
                cursor.close()
                if count == 1:
                    print("Credenciais válidas!")
                    # Execute a próxima ação, por exemplo, abrir uma nova janela
                else:
                    print("Credenciais inválidas.")
                    # Trate o caso de credenciais inválidas, como mostrar uma mensagem de erro ao usuário
            else:
                print("Não foi possível conectar ao banco de dados.")

        except Exception as e:
            print(f"Erro ao validar credenciais: {e}")
            # Trate o erro de acordo com suas necessidades

        # Solicitar a senha do usuário após tentar validar as credenciais no banco de dados
        password = getpass("Digite a senha: ")

        if username == "seu_nome_de_usuario" and password == "sua_senha":
            print("Login bem-sucedido")
        else:
            print("Nome de usuário ou senha inválidos")


if __name__ == "__main__":
    root = tk.Tk()
    login_system = GraphicalLogin(root)
    root.mainloop()
import tkinter as tk
from getpass import getpass
import mysql.connector

class GraphicalLogin:
    def __init__(self, master):
        self.master = master
        self.master.geometry("300x300")
        self.master.title("Login")
        self.master.config(bg="purple")

        self.username_label = tk.Label(master, text="Usuário:", bg="purple", fg="white")
        self.username_label.place(relx=0.05, rely=0.3)

        self.username_entry = tk.Entry(master, width=20, bd=2, bg="white")
        self.username_entry.place(relx=0.3, rely=0.3)

        self.password_label = tk.Label(master, text="Senha:", bg="purple", fg="white")
        self.password_label.place(relx=0.05, rely=0.5)

        self.password_entry = tk.Entry(master, width=20, bd=2, bg="white", show="*")
        self.password_entry.place(relx=0.3, rely=0.5)

        self.login_button = tk.Button(master, text="Login", command=self.validate_credentials)
        self.login_button.place(relx=0.4, rely=0.7)

    def consultar_adm(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="glam"
            )

            query = "SELECT glam FROM id"
            cursor = conn.cursor()
            cursor.execute(query)

            # Processar os resultados (se necessário)
            for row in cursor.fetchall():
                print(row[0])

            # Fechar a conexão
            conn.close()
        except mysql.connector.Error as err:
            print(f"Erro ao conectar ao banco de dados: {err}")
#back end
    from getpass import getpass  # Importar a função getpass para ocultar a entrada da senha

    def validate_credentials(self):
        try:
            username = self.username_entry.get()
            query = f"SELECT COUNT(1) FROM glam WHERE id = '{username}'"

            # Supondo que 'connection' seja o objeto de conexão com o MySQL
            if connection.is_connected():
                print("Conexão ao banco de dados MySQL estabelecida com sucesso!")
                cursor = connection.cursor()
                cursor.execute(query)
                result = cursor.fetchone()
                count = result[0]  # Obtendo o resultado da contagem
                cursor.close()
                if count == 1:
                    print("Credenciais válidas!")
                    # Execute a próxima ação, por exemplo, abrir uma nova janela
                else:
                    print("Credenciais inválidas.")
                    # Trate o caso de credenciais inválidas, como mostrar uma mensagem de erro ao usuário
            else:
                print("Não foi possível conectar ao banco de dados.")

        except Exception as e:
            print(f"Erro ao validar credenciais: {e}")
            # Trate o erro de acordo com suas necessidades

        # Solicitar a senha do usuário após tentar validar as credenciais no banco de dados
        password = getpass("Digite a senha: ")

        if username == "seu_nome_de_usuario" and password == "sua_senha":
            print("Login bem-sucedido")
        else:
            print("Nome de usuário ou senha inválidos")


if __name__ == "__main__":
    root = tk.Tk()
    login_system = GraphicalLogin(root)
    root.mainloop()
