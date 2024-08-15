import mysql.connector
from mysql.connector import Error

try:
    conn = mysql.connector.connect(
        host = "localhost",
        database = "todolist",
        user = "user",
        password = "123456"
    )
    cursor = conn.cursor()
except Error as err:
    print(f"Houve um erro na conexão com o banco de dados, {err}")