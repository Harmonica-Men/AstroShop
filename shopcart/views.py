from django.shortcuts import render, get_object_or_404
from .shopcart import Cart
from store.models import Product
from django.http import JsonResponse
from django.contrib import messages

def shopcart_summary(request):
	# Get the cart
	shopcart = Cart(request)
	
def cart_add(request):
	pass

def cart_delete(request):
    pass

def cart_update(request):
	pass