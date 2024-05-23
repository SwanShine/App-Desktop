import mysql.connector #Biblioteca para conexão com banco de dados
#conexão com o banco de dados

try:
    # Conexão com o banco de dados
    conn = mysql.connector.connect(
        host="swanshine.cpkoaos0ad68.us-east-2.rds.amazonaws.com",
        user="admin",
<<<<<<< HEAD
        password="gLAHqWkvUoaxwBnm9wKD",
        database="swanshine"
=======
        password="swanshine2024",
        database="SwanShine"
>>>>>>> f6ce484a7742c8fb55723f8eca126093d3da84c0
    )

    # Criar um objeto cursor
    cursor = conn.cursor()

    if conn.is_connected():
        print("Conectado ao banco de dados")

  

   
    cursor.close()
    conn.close()

except mysql.connector.Error as e:
    print("Erro ao conectar ao banco de dados:", e)

