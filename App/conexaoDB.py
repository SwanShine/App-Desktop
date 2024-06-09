import mysql.connector  # Biblioteca para conexão com banco de dados

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

    # Seu código aqui...

except mysql.connector.Error as erro:
    print("Erro ao conectar ao MySQL:", erro)

finally:
    # Garantindo que a conexão com o banco de dados seja sempre fechada
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()



def consultar_clientes():
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

        # Consulta SQL para selecionar todos os clientes
        consulta = "SELECT CPF, Email, Endereço, Id_clientes, Nome, Telefone FROM clientes"

        # Executar a consulta
        cursor.execute(consulta)

        # Recuperar todos os resultados
        resultados = cursor.fetchall()

        # Mostrar os resultados
        for resultado in resultados:
            cpf, email, endereco, id_cliente, nome, telefone = resultado
            print("CPF:", cpf)
            print("Email:", email)
            print("Endereço:", endereco)
            print("ID:", id_cliente)
            print("Nome:", nome)
            print("Telefone:", telefone)
            print()

    except mysql.connector.Error as erro:
        print("Erro ao conectar ao MySQL:", erro)

    finally:
        # Garantir que a conexão com o banco de dados seja sempre fechada
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

# Chamada da função para consultar e mostrar os clientes
consultar_clientes()