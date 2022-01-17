from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    
    user = models.OneToOneField(User,on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50, null=True)
    email = models.EmailField(max_length=254, null=True)

    def __str__(self):
        return self.name
    

class Product(models.Model):  
    
    name = models.CharField(max_length=50)
    price = models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=False)
    image = models.ImageField(null=False, blank=True)
        
    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
        

class Order(models.Model):

    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self): 
        return False in [o.product.digital for o in self.orderitem_set.all()]

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):

    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return "Order "+str(self.order)+" - "+str(self.product)

    @property
    def get_total(self):
        return self.product.price * self.quantity
    

class ShippingAddress(models.Model):

    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(null=False, max_length=150)
    city = models.CharField(null=False, max_length=100)
    srate = models.CharField(null=False, max_length=100)
    zipcode = models.CharField(null=False, max_length=50)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.address

   