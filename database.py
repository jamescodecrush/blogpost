import mysql.connector


# Let create database connection
db = mysql.connector.connect(
    host='localhost',
    user = 'root',
    password = '',
    database = 'blogging'
)

cursor = db.cursor()


# Here, I created the table 

cursor.execute("CREATE TABLE IF NOT EXISTS blog_posts (id INT AUTO_INCREMENT PRIMARY KEY,   title VARCHAR (255) NOT NULL, content TEXT NOT NULL)")
print("table created successfully")

