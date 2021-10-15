import mysql.connector
from Codigo.main import lista1
from Codigo.main import lista2
from Codigo.main import lista3

#Se establece la conexión con MySQL
#En "user" coloque su usuario (p.e root) y en "passwd" su contraseña (p.e 1234)
conexion1=mysql.connector.connect(host="localhost", user="", passwd="", database="gmail")

print(conexion1)
cursor1=conexion1.cursor()

#Crear la base de datos gmail si no existe.
cursor1.execute("CREATE DATABASE IF NOT EXISTS gmail")

#Mostrar las bases de datos existentes.

cursor1.execute("show databases")
for i in cursor1:
    print(i)

#En caso de que no exista la tabla gmaildevops la crea.
cursor1.execute("CREATE TABLE IF NOT EXISTS gmaildevops (fecha VARCHAR(60) NOT NULL,remitente VARCHAR(60) NOT NULL, asunto VARCHAR(60) NOT NULL, PRIMARY KEY (fecha, remitente, asunto))")

#Agregamos los valores definidos en datos a la tabla gmaildevops.
sql = "INSERT IGNORE INTO gmaildevops (fecha, remitente, asunto) VALUES (%s, %s, %s)"

#En datos vamos a agregar los elementos que se encuentran en las 3 listas recolectadas en el archivo main
#El codigo trae los 5 primeros elementos de las listas, pueden agregarse cuantos registros se desee teniendo en cuenta el tamaño de la lista
#Por ejemplo si la lista1 tiene 10 elementos podremos agregar lista1[5], lista1[6],..., y asi sucesivamente hasta llegar al elemento 10

datos = [
    (lista1[0], lista2[0], lista3[0]),
    (lista1[1], lista2[1], lista3[1]),
    (lista1[2], lista2[2], lista3[2]),
    (lista1[3], lista2[3], lista3[3]),
    (lista1[len(lista1)-1], lista2[len(lista2)-1], lista3[len(lista3)-1])
]

cursor1.executemany(sql, datos)

conexion1.commit()
conexion1.close()
