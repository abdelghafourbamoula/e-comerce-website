import json
from .models import *


def cookieCart(request) :
    ''' load guest user (AnonymousUser) cart informations from cookies '''
    
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
        
    print("---> cart:", cart)

    #Create empty cart for now for non-logged in user
    items = []
    order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
    cartItems = order['get_cart_items']
    
    #calc total cart items
    for i in cart:
        try:
            cartItems += cart[i]['quantity']
            
            product = Product.objects.get(id=i)
            total = product.price * cart[i]['quantity']

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']

            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'imageURL': product.imageURL
                },
                'quantity': cart[i]['quantity'],
                'get_total': total
            }
            items.append(item)

            if product.digital == False:
                order['shipping'] == True
        except:
            print('>>> Exception ! ')
            pass
        
    return {
        'items':items, 
        'order':order, 
        'cartItems':cartItems
    }