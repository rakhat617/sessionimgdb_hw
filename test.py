import sqlite3

connection = sqlite3.connect("post.db")
cursor = connection.cursor()
cursor.execute(" SELECT * FROM post ")
posts = cursor.fetchall()



connection.commit()


for i in posts:
    print(i[4])

connection.close()
