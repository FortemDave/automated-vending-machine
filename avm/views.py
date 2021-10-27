from django.shortcuts import render
from django.http import HttpResponse
from .models import Item, order
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
    if request.method == "POST":
        itemJson = request.POST.get('itemsJson','')
        phoneNo = request.POST.get('phone','')
        orders =  order(items_json = itemJson, phone_no = phoneNo)
        orders.save()
        thank = True
        id = orders.id
        context = {
            'thank' : thank,
            'id':id
        }
        return render(request, 'avm/checkout.html', context)

    return render(request, 'avm/checkout.html')