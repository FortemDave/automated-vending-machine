from django.shortcuts import render
from django.http import HttpResponse
from .models import Item
# Create your views here.

def index(request):
    return HttpResponse("Hello !!! This is an automated vending machine")

def home(request):
    return HttpResponse("You are at Machine 1 . Click Enter to proceed forward")

def cart(request):
    item_list = Item.objects.all()
    context = {
        'item_list': item_list
    }
    return render(request, 'avm/cart.html', context)