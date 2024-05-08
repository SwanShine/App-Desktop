import mysql.connector #Biblioteca para conexão com banco de dados
#conexão com o banco de dados

try:
    # Conexão com o banco de dados
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="glamtech"
    )

    # Criar um objeto cursor
    cursor = conn.cursor()

    if conn.is_connected():
        print("Conectado ao banco de dados")

  

   
    cursor.close()
    conn.close()

except mysql.connector.Error as e:
    print("Erro ao conectar ao banco de dados:", e)

