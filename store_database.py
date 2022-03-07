import mysql.connector
import os

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = os.environ["SECRET"], # password allowing me access to the database. stored in the enviroment variables
    database = "myStore" # server connects to store database
)


c = db.cursor()

'''creating database called store'''

c.execute("CREATE DATABASE IF NOT EXISTS myStore") # create store database if it does not exists that will contain all tables for store. ONE TIME COMMAND

'''Creating four tables within database

1) Users
2) User password - encrpyed(hashed and salted)
3) products table
4) Orders table
'''

c.execute('''CREATE TABLE IF NOT EXISTS myUsers(
    userID BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT, 
    name VARCHAR(50) NOT NULL,
    userName VARCHAR(20) NOT NULL,
    address VARCHAR(100) NOT NULL,
    creation_date DATE NOT NULL

)''')



c.execute('''CREATE TABLE IF NOT EXISTS userPassword(
    userID BIGINT UNSIGNED PRIMARY KEY,FOREIGN KEY(userID) REFERENCES myUsers(userID) ON DELETE CASCADE,
    passwd VARCHAR(200) NOT NULL 
)''')


c.execute('''CREATE TABLE IF NOT EXISTS productsTable(
    productID BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    productName VARCHAR(140) NOT NULL,
    productPrice DOUBLE NOT NULL,
    noStock INT UNSIGNED DEFAULT 10
)''')


c.execute('''CREATE TABLE IF NOT EXISTS ordersTable(
    OrderID BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    productID BIGINT UNSIGNED, FOREIGN KEY(productID) REFERENCES productsTable(productID) ON DELETE CASCADE,
    userId BIGINT UNSIGNED, FOREIGN KEY(userID) REFERENCES myUsers(userID) ON DELETE CASCADE
)''')



# c.execute("DROP TABLE IF EXISTS myUsers")
# c.execute("DROP TABLE IF EXISTS userPassword")
# c.execute("DROP DATABASE myStore")
# c.execute("SHOW TABLES")
c.execute("SELECT passwd FROM userPassword")
print(c.fetchall())