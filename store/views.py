from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime

from .models import *
from .utils import *


def store(request):

	products = Product.objects.all()
	cartItems = cartData(request).get('cartItems')
 
	context = {
        'products':products, 
        'cartItems':cartItems
    }
 
	return render(request, 'store/store.html', context)


def store_digital(request):

	products = Product.objects.all()
	cartItems = cartData(request).get('cartItems')
 
	context = {
        'products':products, 
        'cartItems':cartItems
    }
 
	return render(request, 'store/store-digital.html', context)

   
def cart(request):

	user_data = cartData(request)
	items = user_data.get('items')
	order = user_data.get('order')
	cartItems = user_data.get('cartItems')
  
	context = {
        'items':items, 
        'order':order, 
        'cartItems':cartItems
    }
 
	return render(request, 'store/cart.html', context)


def checkout(request):

	user_data = cartData(request)
	items = user_data.get('items')
	order = user_data.get('order')
	cartItems = user_data.get('cartItems')

	context = {
        'items':items, 
        'order':order, 
        'cartItems':cartItems
    }
 
	return render(request, 'store/checkout.html', context)


def updateItem(request):
    
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)


def processOrder(request):

    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated :
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        
    else:
        customer, order = guestOrder(request, data)
        
    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total) :
        order.complete = True
    order.save()
    
    if order.shipping == True :
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            srate=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
            country=data['shipping']['country']
        )
        
    return JsonResponse('Payment submitted...', safe=False)


def login(request):
    
    return render(request, 'login.html', {})


def register(request):
    
    return render(request, 'register.html', {})