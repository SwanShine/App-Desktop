import mysql.connector #Biblioteca para conexão com banco de dados
#conexão com o banco de dados
conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="glamtech"
)

if conexao.is_connected():
    print("Conectado com o banco de dados")




