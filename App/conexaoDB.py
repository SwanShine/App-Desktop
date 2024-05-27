import mysql.connector #Biblioteca para conexão com banco de dados
#conexão com o banco de dados

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

  

   
    cursor.close()
    conn.close()

except mysql.connector.Error as e:
    print("Erro ao conectar ao banco de dados:", e)

