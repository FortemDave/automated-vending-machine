import sqlite3 as sql
import json

global SPACE
SPACE = "\t\t"

def transac_info(db):
    cur = db.cursor()
    cur.execute('''
    SELECT * FROM avm_order;
    '''
    )

    for row in cur.fetchall():
        total_cost = 0
        transac_id = row[0]
        print(transac_id)
        phone_num = row[1]
        json_string = row[2]
        data = json.loads(json_string)
        names = data.values()
        names = [len(name[1]) for name in names]
        max_name_length = max(names)
        product_ids = list(data.keys())
        product_ids = [string_id[2:] for string_id in product_ids]
        # print(product_ids)
        # print(data)
        print("===================================================================")
        name_title = "NAME" + " "*(max_name_length-4)
        print(f'PID{SPACE}{name_title}{SPACE}QUANTITY{SPACE}PRICE')
        for id in product_ids:
            cur.execute(f'''
                SELECT item_price FROM avm_item
                WHERE id = {id};
            ''')

            product_per_price = cur.fetchall()[0][0]
            product_quantity = data['pr'+ id][0]
            product_name = data['pr'+ id][1]
            product_name = product_name + " "*(max_name_length - len(product_name))
            # print(product_per_price)
            # print(product_quantity)
            product_overall_price = product_per_price*product_quantity
            total_cost += product_overall_price

            print(f"{id}{SPACE}{product_name}{SPACE}{product_quantity}{SPACE}\t{product_overall_price}")
        print(f"\nOVERALL TRANSACTION COST = {total_cost}")
        print("====================================================================")

def reStock(db, pr_id, reStkAmount):
    cur = db.cursor()
    cur.execute(f''' 
        SELECT item_quantity_available, item_name
        FROM avm_item
        WHERE id = {pr_id};
    ''')
    
    avalQuantity, item_name = cur.fetchall()[0]
    # print(avalQuantity)
    
    cur.execute(f''' 
        UPDATE avm_item 
        SET item_quantity_available = {avalQuantity + reStkAmount}
        WHERE id = {pr_id};
    ''')
    db.commit()
    print("====================================================================\n")
    print(f"The quantity of the Item Id {pr_id} and Item Name {item_name} is updated to {avalQuantity + reStkAmount}\n")
    print("====================================================================")

    
def lowStockRestock(db):
    cur = db.cursor()
    cur.execute(''' 
        SELECT id, item_name, item_quantity_available
        FROM avm_item
    ''')

    lowStockItems = []
    defRestock = 10
    item_count = 0
    print("====================================================================")
    for item in cur.fetchall():
        if item[2] <= 5:
            lowStockItems.append([item[0], item[1], item[2]])
            reStock(db, item[0], defRestock)
            item_count += 1
    
    if item_count == 0:
        print("No items are in the need of restock")
    else:
        print(f"{item_count} items have been successfully restocked")
    print("====================================================================")
    # print(lowStockItems)
    db.commit()


def priceCalc(db, order_id):
    cur = db.cursor()
    cur.execute(f''' 
        SELECT items_json
        FROM avm_order
        WHERE id = {order_id};
    ''')

    json_string = cur.fetchall()[0][0]
    raw_dict = json.loads(json_string)
    # print(raw_dict)
    
    orderPrice = []
    for keys, values in raw_dict.items():
        keys = keys[2:]
        itemQuantity = values[0]
        cur.execute(f''' 
            SELECT item_price, item_name
            FROM avm_item
            WHERE id = {keys};
        ''')
        indvPrice, item_name = cur.fetchall()[0]
        itemPrice = indvPrice * itemQuantity
        orderPrice.append([keys, itemPrice, item_name])
    print("====================================================================")
    print(f"Pricing of the items purchased in order {order_id} : ")
    for i in range(len(orderPrice)):
        print(f"Item ID : {orderPrice[i][0]} \tItem Name :  {orderPrice[i][2]} \t\tPurchase : {orderPrice[i][1]}")
    print("====================================================================")
    return orderPrice


def productInfo(db, item_id):
    cur = db.cursor()
    cur.execute(f''' 
        SELECT * 
        FROM avm_item
        WHERE id = {item_id};
    ''')

    rawInfo = cur.fetchall()[0]
    itemName, itemPrice, itemQuantity = rawInfo[1], rawInfo[2], rawInfo[3]
    print("====================================================================")
    print(f"Item Name : {itemName}, Item ID : {item_id}, Item Price : {itemPrice}, Item Quantity : {itemQuantity}")
    print("====================================================================")
    return itemName, item_id, itemQuantity, itemPrice
    # print(rawInfo)

def add_product(db, product_name, price, quantity, img_url = " "):
    cur = db.cursor()

    with db:
        cur.execute(f'''INSERT INTO avm_item (item_price, item_quantity_available, item_name, item_picture_url)
                        VALUES ({price}, {quantity}, '{product_name}', '{img_url}');
            ''')

    # cur.execute(f'''INSERT INTO avm_item ({price}, {quantity}, {product_name})
    #                 VALUES (item_price, item_quantity_available, item_name);
    #     ''')


# db = sql.connect('db.sqlite3')
# cur = db.cursor()
# # transac_info(db)
# reStock(db, 2, 15)
# # priceCalc(db, 2)
# # productInfo(db, 5)
# # add_product(db, 'pepsi', 20, 10)
# # lowStockRestock(db)

def menu():
    
    print('''\nEnter the operation to perform : 
             \n1. Transaction Directory
             \n2. Restock Item
             \n3. Order Information
             \n4. Item Information
             \n5. Add Product
             \n6. Check and Restock
             \n7. Exit admin access
    ''')

def main():

    db = sql.connect('db.sqlite3')
    # cur = db.cursor()
    
    while True:
        menu()
        choice = int(input())
        if choice == 1:
            print("| Transaction Directory |")
            transac_info(db)
        
        elif choice == 2:
            item_id = int(input("Enter the item id to restock : "))
            item_quantity = int(input("Enter the quantity of the item to restock : "))
            reStock(db, item_id, item_quantity)

        elif choice == 3:
            order_id = int(input("Enter the order id to calculate price : "))
            priceCalc(db, order_id)

        elif choice == 4:
            item_id = int(input("Enter the item id to get information : "))
            productInfo(db, item_id)
            
        elif choice == 5:
            item_name = input("Enter the new product name : ")
            item_price = int(input("Enter the product price : "))
            item_quantity = int(input("Enter the initial quantity to stock : "))
            add_product(db, item_name, item_quantity, item_price)

        elif choice == 6:
            lowStockRestock(db)

        elif choice == 7:
            print("=====================================================")
            print("Successfully exited\n")
            print("=====================================================")
            break
        
        else:
            print("=====================================================")
            print("!! Enter a valid operation number !!")
            print("=====================================================")

if __name__ == "__main__":
    main()

