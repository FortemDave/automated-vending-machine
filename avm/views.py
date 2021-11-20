from django.shortcuts import render
from django.http import HttpResponse
from .models import Item, order
import json
import sqlite3
import random
import requests

# Create your views here.

def index(request):
    return HttpResponse("Hello !!! This is an automated vending machine")

def home(request):
    return render(request,'avm/index.html')
    # return HttpResponse("You are at Machine 1 . Click Enter to proceed forward")

def cart(request):
    item_list = Item.objects.all()

    context = {
        'item_list': item_list
    }
    return render(request, 'avm/cart.html', context)

def checkout(request):
    # item_list = Item.objects.all()
    db = sqlite3.connect('db.sqlite3')
    cursor = db.cursor()
    if request.method == "POST":
        itemJson = request.POST.get('itemsJson','')

        dict_obj = json.loads(itemJson)

        keys = dict_obj.keys()
        ids = [key[2:] for key in keys]

        for id in ids:
            dict_key = 'pr' + id
            dict_list = dict_obj[dict_key]
            quantity = dict_list[0]

            cursor.execute(f'''
            SELECT item_quantity_available FROM avm_item
            WHERE id = {id};
            ''')

            avail = cursor.fetchall()[0][0]
            
            cursor.execute(f'''
            UPDATE avm_item
            SET item_quantity_available = {avail-quantity}
            WHERE id = {id};
            ''')

            db.commit()

        # Using the website to execute API commands
        url = "https://www.fast2sms.com/dev/bulk"

        #Sending a 4 digit verification number, use it for authentication
        verification_code = random.randint(1000,9999)


        phoneNo = request.POST.get('phone','')
        def valindIndianNum(number):
            if len(number) != 10:
                return 0
            elif number[0:3] == "040":
                #IF A LANDLINE NUMBER IS GIVEN
                return 0
            elif number[0] not in ["6","7","8","9"]:
                #Non INDIAN number
                return 0
            return 1

        # Take the input here, you decide how
        print(phoneNo)
        indian_number = str(phoneNo)
        print(type(phoneNo))
        indian_number = indian_number.strip()

        message = "Your AVM OTP is : {a}. If you did not intend to recieve this message, kindly ignore it.".format(a = verification_code)

        # API SPECIFIC INFORMATION--------------------------------
        my_data = {
            'sender_id': 'FTSMS',
            'message': message,
            'language': 'english',
            'route':'p',
            'numbers': '{}'.format(indian_number)
        }

        # DO NOT MODIFY or SHARE this data WITH ANYONE, contains personal information
        # of a colleage. 
        headers = {
            'authorization': 'GbwHQzC2yWKlPLajAUOxFc6ZSknTprMthNBmJgER903v5fos8ibB8PIhDVXefSqCunL3EpxZUGtWQkl6',
            'Content-Type': "application/x-www-form-urlencoded",
            'Cache-Control': "no-cache"
        }
        #---------------------------------------------------------

        if(valindIndianNum(phoneNo)):
            response = requests.request("POST",
                                        url,
                                        data = my_data,
                                        headers = headers)

            returned_msg = json.loads(response.text)
        
            # Uncomment if you want to see the transaction status
            # print(returned_msg['message'])
        else:
            # Do what you want to, dummy code here
            print("INVALID NUMBER")

        print(verification_code)
        orders =  order(items_json = itemJson, phone_no = phoneNo)
        orders.save()
        thank = True
        id = orders.id
        context = {
            'thank' : thank,
            'id':id,
            'code':verification_code
        }
        # print(keys)
        return render(request, 'avm/checkout.html', context)

    return render(request, 'avm/checkout.html')

def paytm(request):
    return render(request, 'avm/paytm.html')