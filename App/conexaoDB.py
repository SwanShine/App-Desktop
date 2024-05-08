import mysql.connector #Biblioteca para conexão com banco de dados
#conexão com o banco de dados

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="glamtech"
)

cursor = conn.cursor.execute()

if conn.is_connected():
    print("Conectado com o banco de dados")




