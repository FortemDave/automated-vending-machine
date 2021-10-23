import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "pwd"
)

mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE IF NOT EXISTS Vending_DB;")
mycursor.execute("USE Vending_DB;")

mycursor.execute("""
CREATE TABLE IF NOT EXISTS customer(

        customer_ID INT NOT NULL,
        customer_name VARCHAR(255) NOT NULL,
        pwd VARCHAR(255) NOT NULL,
        PRIMARY KEY(customer_ID)
);
""")

mycursor.execute("""
CREATE TABLE IF NOT EXISTS stock(

    product_ID INT NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    product_quantity INT NOT NULL,
    PRIMARY KEY(product_ID)
);
""")

mycursor.execute("""
CREATE TABLE IF NOT EXISTS transactions(

    transaction_ID INT NOT NULL,
    customer_ID INT NOT NULL,
    product_ID INT NOT NULL,
    quantity INT NOT NULL,
    passed BOOLEAN NOT NULL,

    PRIMARY KEY(transaction_ID),
    FOREIGN KEY(customer_ID) REFERENCES customer(customer_ID),
    FOREIGN KEY(product_ID) REFERENCES stock(product_ID)
)
""")
