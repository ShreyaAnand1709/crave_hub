from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    mobile = models.CharField(max_length=100)
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.username
    
class Restaurant(models.Model):
    name = models.CharField(max_length=50)
    picture = models.URLField(max_length=200, default='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR_Iajzp-onUeDOfrpk3zO0QNPzIXXoEBCWXw&s')
    cusine = models.CharField(max_length=200)
    rating = models.FloatField(max_length=20)

class Item(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="items")
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    price = models.FloatField()
    veg = models.BooleanField(default = False)
    picture = models.URLField(max_length=400, default='https://media.gettyimages.com/id/1829241109/photo/enjoying-a-brunch-together.jpg?s=612x612&w=gi&k=20&c=SFRYlKrWD84RMNV_c8fIliBep7WHoV-0s6IBc5FJsmE=')

class Cart(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart")

    def total_price(self):
        return sum(ci.item.price * ci.quantity
            for ci in self.cart_items.all() )
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def total_price(self):
        return self.item.price * self.quantity
    