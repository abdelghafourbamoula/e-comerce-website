from django.shortcuts import render
from django.http import JsonResponse
from .models import *
import json

def store(request):
    products = Product.objects.all()
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItem = order.get_cart_item
    else:
        items = []
        order = {"get_cart_item": 0,  "get_cart_total": 0 }
        cartItem = order['get_cart_total']
    
    context = {
        'products': products,
        'cartItem': cartItem   
    }
    
    return render(request, 'store/store.html', context)


def cart(request):
    # check if the user logged in or not
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItem = order.get_cart_item
           
    else:
        items = []   
        order = {"get_cart_item": 0,  "get_cart_total": 0 }
        cartItem = order['get_cart_total']
        
    context = {
        'items': items,
        'order': order,
        'cartItem': cartItem   
    }
    
    return render(request, 'store/cart.html', context)


def checkout(request):
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItem = order.get_cart_item
        
    else:
        items = []
        order = {"get_cart_item": 0, "get_cart_total": 0 }
        cartItem = order['get_cart_total']
        
    context = {
        'items': items,
        'order': order,
        'cartItem': cartItem   
    }
    
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    # get data posted on the request body
    data = json.loads(request.body)
    product_id = data['productId']
    action = data['action']
    
    customer = request.user.customer
    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    
    if action == 'add':
        orderItem.quantity = orderItem.quantity + 1
    elif action == 'remove':
        orderItem.quantity = orderItem.quantity - 1
    
    orderItem.save()
    
    if orderItem.quantity <= 0:
        orderItem.delete()
        
    return JsonResponse('Item added Successfully', safe=False)