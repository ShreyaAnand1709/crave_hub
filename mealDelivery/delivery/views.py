from django.http import HttpResponse
from mealDelivery import settings
from django.contrib.auth.decorators import login_required

import razorpay
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .models import Cart, CartItem, Item, Restaurant, User
# Create your views here.
def index(request):
    return render(request, "index.html")

def open_signup(request):
    return render(request, "signup.html")

def open_signin(request):
    return render(request, "signin.html")

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')

        if User.objects.filter(email=email).exists():
            return HttpResponse("Email alreay existing")
        user=User(username=username, password = password, email=email, mobile=mobile, address=address)
        user.save()
        # return HttpResponse("Sign up successful with the username {username} and the email ID {email}")
        return render (request, 'signin.html')
    else :
        return HttpResponse("Sign up is invalid")
    
def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
    try : 
        user = User.objects.get(username=username, password=password)

        request.session['user_id'] = user.id

        if username == 'admin':
            return render(request, 'admin_homt.html')
        
        else:
            restaurantList = Restaurant.objects.all()
        return render(request,'customer_home.html',{"restaurantList": restaurantList,"username": username})

    except User.DoesNotExist:
        messages.error(request, "Invalid username and password")
        return redirect('open_signin')
    
def admin_home(request):
    return render(request,'admin_homt.html')
    
def add_rest(request):
    return render(request, "add_rest.html")

def add_restaurant(request): 
    if request.method == 'POST':
        name = request.POST.get('name')
        picture = request.POST.get('picture')
        cusine =  request.POST.get('cusine')
        rating =  request.POST.get('rating')

        try:
            Restaurant.objects.get(name=name)
            messages.error(request, "Restaurant with this name already exists!")
            return redirect('add_rest')
        
        except:
            Restaurant.objects.create(
                name = name,
                picture = picture,
                cusine = cusine,
                rating = rating,
            )
        messages.success(request,"Successfully added")
    return redirect('admin_home')

def show_restaurant(request):
    restaurant = Restaurant.objects.all()
    return render(request, 'show_restaurants.html', {"restaurant": restaurant})

def update_menu(request, restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    return render(request, "update_menu.html", {"restaurant" : restaurant})

def updating_menu(request, restaurant_id):
    if request.method == "POST":
        restaurant = Restaurant.objects.get(id=restaurant_id)
        name = request.POST.get("cname")
        description = request.POST.get("description")
        price = float(request.POST.get("price"))
        veg = request.POST.get("veg") == "True"
        picture = request.POST.get("picture")

        try:
            Item.objects.get(name=name)
            return HttpResponse("Duplicate dish")
        
        except:
            Item.objects.create(
                restaurant = restaurant,
                name = name,
                description = description,
                price = price,
                veg = veg,
                picture = picture,
            )
    return HttpResponse("Updated the menu")

def show_restaurant_cust(request):
    restaurant = Restaurant.objects.all()
    return render(request, 'show_restarant_cust.html', {"restaurant": restaurant})

def place_order(request, restaurant_id):
    items = Item.objects.filter(restaurant_id = restaurant_id)
    return render(request, 'place_order.html', {"items": items})

def update_restaurant_info(request, restaurant_id):
    restaurant = Restaurant.objects.get(id = restaurant_id)
    return render(request, 'open_update_restaurant_info.html', {"restaurant": restaurant})

def open_update_restaurant(request, restaurant_id) :
    restaurant = Restaurant.objects.get(id = restaurant_id)
    if request.method == "POST":
        name = request.POST.get('name')
        picture = request.POST.get('picture')
        cusine = request.POST.get('cusine')
        rating = request.POST.get('rating')

        restaurant.name = name
        restaurant.picture = picture
        restaurant.cusine = cusine
        restaurant.rating = rating

        restaurant.save()

        restaurantList = Restaurant.objects.all()
        return redirect('show_restaurant')
    return redirect('update_restaurant_info', restaurant_id=restaurant_id)

def delete_rest(request, restaurant_id) :
    restaurant = Restaurant.objects.get(id = restaurant_id)
    restaurant.delete()
    restaurant = Restaurant.objects.all()
    return render(request, 'show_restaurants.html', {"restaurant":restaurant})

def add_to_cart(request, item_id):
    # get item
    item = Item.objects.get(id=item_id)

    # get logged-in custom user from session
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('open_signin')

    customer = User.objects.get(id=user_id)

    # get or create cart
    cart, _ = Cart.objects.get_or_create(customer=customer)

    # get or create cart item
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        item=item
    )

    # if already exists, increase quantity
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('view_cart')

def view_cart(request) :
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('open_signin')

    customer = User.objects.get(id=user_id)

    # 2️⃣ Get cart
    try:
        cart = Cart.objects.get(customer=customer)
    except Cart.DoesNotExist:
        cart = None

    # 3️⃣ Get cart items
    cart_items = cart.cart_items.all() if cart else []

    # 4️⃣ Calculate total
    total_price = sum(
        ci.item.price * ci.quantity for ci in cart_items
    )

    return render(request, 'view_Cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'username' : customer.username,
    })

def checkout(request, username):
    customer = get_object_or_404(User, username=username)

    cart = Cart.objects.filter(customer=customer).first()
    items = cart.cart_items.all() if cart else []
    total_price = cart.total_price() if cart else 0

    # Razorpay client setup
    client = razorpay.Client(auth=(
        settings.RAZORPAY_KEY_ID,
        settings.RAZORPAY_KEY_SECRET
    ))

    order_data = {
        'amount': int(total_price * 100),  # amount in paise
        'currency': 'INR',
        'payment_capture': 1,
    }

    order = client.order.create(data=order_data)

    return render(request, 'checkout.html', {
        'username': username,
        'cart_items': items,
        'total_price': total_price,
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'order_id': order['id'],
    })