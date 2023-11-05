import mysql.connector

db = mysql.connector.connect(

    host ='localhost',
    user = 'root',
    passwd = '168990'

)

cursor = db.cursor()

cursor.execute('CREATE DATABASE PLAYER_WEB')
