import mysql.connector

#################################################################################################

def add_customer(db, id, name, pwd):
    cursor = db.cursor()
    cursor.execute("USE Vending_DB;")
    cursor.execute(f"""
    INSERT INTO customer
    VALUES ({id}, "{name}", "{pwd}");
""")
    db.commit()

#################################################################################################

def commit_transaction(db, trans_ID, product_id, customer_id, quant):
    cursor = db.cursor()
    cursor.execute("USE Vending_DB;")
    cursor.execute(f"""
        SELECT product_quantity
        FROM stock
        WHERE product_id = {product_id};
    """)
    available = cursor.fetchall()
    available = available[0][0]

    cursor.execute(f"""
        SELECT * FROM customer
        WHERE customer_ID = {customer_id};
    """)

    customer_info = cursor.fetchall()
    customer_info = customer_info[0]

    cursor.execute(f"""
        SELECT * FROM stock
        WHERE product_ID = {product_id};
    """)

    product_info = cursor.fetchall()
    product_info = product_info[0]

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

    db.commit()

#################################################################################################

def add_product(db, id, name, quant):
    cursor = db.cursor()
    cursor.execute("USE Vending_DB;")
    cursor.execute(f"""
        INSERT INTO stock
        VALUES ({id}, "{name}", {quant});
    """)
    db.commit()

#################################################################################################

def restock(db):
    cursor = db.cursor()
    cursor.execute("USE Vending_DB;")
    cursor.execute(f"""
        UPDATE stock
        SET product_quantity = 15
        WHERE product_quantity < 15;
    """)
    db.commit()

#################################################################################################

def get_customer_details(db, id):
    cursor = db.cursor()
    cursor.execute("USE Vending_DB;")
    cursor.execute(f"""
        SELECT * FROM customer
        WHERE customer_ID = {id};
    """)

    info = cursor.fetchall()
    info = info[0]

    print("==================Customer Details======================")
    print("ID: ", info[0])
    print("Name: ", info[1])
    print("========================================================")

#################################################################################################

def get_product_details(db, id):
    cursor = db.cursor()
    cursor.execute("USE Vending_DB;")
    cursor.execute(f"""
        SELECT * FROM stock
        WHERE product_ID = {id};
    """)

    info = cursor.fetchall()
    info = info[0]

    print("==================Product Details======================")
    print("ID: ", info[0])
    print("Name: ", info[1])
    print("Quantity: ", info[2])
    print("=======================================================")

#################################################################################################

def transaction_info(db, id):
    cursor = db.cursor()
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
    info = info[0]

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
    password = "greatboy"
)

mycursor = mydb.cursor()
mycursor.execute("USE Vending_DB;")


