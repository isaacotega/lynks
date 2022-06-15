import mysql.connector

conn = mysql.connector.connect(host="sql3.freemysqlhosting.net", user="sql3499421", password="3gWdBJvTJE", database="sql3499421")

cursor = conn.cursor(dictionary=True)