import mysql.connector

#################################################################################################

def add_customer(cursor, id, name, pwd):
    cursor.execute("USE Vending_DB;")
    cursor.execute(f"""
    INSERT INTO customer
    VALUES ({id}, {name}, {pwd});
""")

#################################################################################################

def commit_transaction(cursor, trans_ID, product_id, customer_id, quant):
    cursor.execute("USE Vending_DB;")
    cursor.execute(f"""
        SELECT product_quantity
        FROM stock
        WHERE product_id = {product_id};
    """)
    available = cursor.fetchall()[0]

    cursor.execute(f"""
        SELECT * FROM customer
        WHERE customer_ID = {customer_id};
    """)

    customer_info = cursor.fetchall()

    cursor.execute(f"""
        SELECT * FROM stock
        WHERE product_ID = {product_id};
    """)

    product_info = cursor.fetchall()

    if quant <= available:
        cursor.execute(f"""
            INSERT INTO transactions
            VALUES ({trans_ID}, {customer_info[0]}, {product_info[0]}, {quant}, TRUE);
        """)
        cursor.execute(f"""
            UPDATE stock
            SET product_quantity = {available-quant}
            WHERE product_ID = {product_info[0]};
        """)
        print(f"Transaction for {product_info[0]}: {product_info[1]} SUCCESSFULL.")
    else:
        print(f"Transaction for {product_info[0]}: {product_info[1]} FAILED.")
        cursor.execute(f"""
            INSERT INTO transactions
            VALUES ({trans_ID}, {customer_info[0]}, {product_info[0]}, {quant}, FALSE);
        """)

#################################################################################################

def add_product(cursor, id, name, quant):
    cursor.execute("USE Vending_DB;")
    cursor.execute(f"""
        INSERT INTO stock
        VALUES ({id}, {name}, {quant});
    """)

#################################################################################################

def restock(cursor):
    cursor.execute("USE Vending_DB;")
    cursor.execute(f"""
        UPDATE stock
        SET product_quantity = 15
        WHERE product_quantity < 15;
    """)

#################################################################################################

def get_customer_details(cursor, id):
    cursor.execute("USE Vending_DB;")
    cursor.execute(f"""
        SELECT * FROM customer
        WHERE customer_ID = {id};
    """)

    info = cursor.fetchall()

    print("==================Customer Details======================")
    print("ID: ", info[0])
    print("Name: ", info[1])
    print("========================================================")

#################################################################################################

def get_product_details(cursor, id):
    cursor.execute("USE Vending_DB;")
    cursor.execute(f"""
        SELECT * FROM product
        WHERE product_ID = {id};
    """)

    info = cursor.fetchall()

    print("==================Product Details======================")
    print("ID: ", info[0])
    print("Name: ", info[1])
    print("=======================================================")

#################################################################################################

def transaction_info(cursor, id):
    cursor.execute("USE Vending_DB;")
    cursor.execute(f"""
        SELECT transactions.transaction_ID, stock.product_ID, stock.product_name, transactions.quantity, transactions.customer_ID,
             customer.customer_name, transactions.check
        FROM transactions
        INNER JOIN customer ON transactions.customer_ID = customer.customer_ID
        INNER JOIN stock ON transactions.product_ID = stock.product_ID
        WHERE transaction_ID = {id};
    """)

    info = cursor.fetchall()

    print("==================Transaction Details======================")
    print("ID: ", info[0])
    print("Product ID: ", info[1])
    print("Product: ", info[2])
    print("Quantity: ", info[3])
    print("Customer ID: ", info[4])
    print("Customer Name: ", info[5])
    print("Passed? :", info[6])
    print("============================================================")

#################################################################################################

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "pwd"
)

mycursor = mydb.cursor()
mycursor.execute("USE Vending_DB;")
