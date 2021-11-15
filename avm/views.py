from django.shortcuts import render
from django.http import HttpResponse
from .models import Item, order
import json
import sqlite3
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

        phoneNo = request.POST.get('phone','')
        orders =  order(items_json = itemJson, phone_no = phoneNo)
        orders.save()
        thank = True
        id = orders.id
        context = {
            'thank' : thank,
            'id':id
        }
        # print(keys)
        return render(request, 'avm/checkout.html', context)

    return render(request, 'avm/checkout.html')

def paytm(request):
    return render(request, 'avm/paytm.html')