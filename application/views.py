from django.shortcuts import render, redirect
from .models import Pizza, Drink, Topping, User, Cart, CartItem, Size, PizzaPrice, Order, OrderItem
from django.contrib.auth import update_session_auth_hash, authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponseBadRequest
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


def home(request):
   all_pizzas = Pizza.objects.filter(available=True)
   
   return render(request, "home.html", {"pizzas": all_pizzas})

def menu(request):
   all_pizzas = Pizza.objects.filter(available=True)
   all_drinks = Drink.objects.filter(available=True)
   return render(request, "menu.html", {"pizzas": all_pizzas, "drinks": all_drinks})

def select_pizza(request, pizza_id):
   pizza = Pizza.objects.get(id=pizza_id)
   drinks = Drink.objects.filter(available=True)
   toppings = Topping.objects.all()
   available_topping_ids = pizza.available_toppings.values_list('id', flat=True)
   
   sizes = Size.objects.all()
   for size in sizes:
    size.calculated_price = round(pizza.base_price * size.multiplier, 2)
   
   return render(request, "select-pizza.html", {
      "pizza": pizza, 
      "drinks": drinks, 
      "toppings": toppings,
      "sizes": sizes,
      "available_topping_ids": set(available_topping_ids),
   })

def login(request):
   if request.method == "POST":
      username = request.POST.get("username")
      password = request.POST.get("password")
      
      user = authenticate(request, username=username, password=password)

      if user is not None:
         auth_login(request, user) 
         return redirect("/")
      else:
         return render(request, "login.html", {"error": "Invalid credentials."})

   return render(request, "login.html")

def signup(request):
   if request.method == "POST":
      firstname = request.POST.get("firstname")
      lastname = request.POST.get("lastname")
      email = request.POST.get("email")
      username = request.POST.get("username")
      password = request.POST.get("password")
      
      user = User.objects.create_user(username, password, email)
      user.last_name = lastname
      user.first_name = firstname
      user.save()
      
      auth_login(request, user)
      return redirect("/")
      
   return render(request, "signup.html")

def logout(request):
   auth_logout(request)
   return redirect("/")

def profile(request):
    if not request.user.is_authenticated:
        return redirect("/login")

    password_form = PasswordChangeForm(user=request.user)

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()

        # Validation
        name_valid = name.isalpha()
        try:
            validate_email(email)
            email_valid = True
        except ValidationError:
            email_valid = False

        if not name_valid:
            messages.error(request, "Name must only contain letters.")
        if not email_valid:
            messages.error(request, "Enter a valid email address.")

        if name_valid and email_valid:
            request.user.first_name = name
            request.user.email = email
            request.user.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("/profile")

    return render(request, "profile.html", {
        "password_form": password_form,
        "user": request.user
    })


def change_password(request):
   password_form = PasswordChangeForm(data=request.POST, user=request.user)
   if password_form.is_valid():
      user = password_form.save()
      update_session_auth_hash(request, user)
      return redirect("/profile")


def cart(request):
   # handle add to cart
   if request.method == "POST":
      # check if user is logged in
      if not request.user.is_authenticated:
         return redirect("/login")
      
      # get the details from the form (from frontend)
      quantity = request.POST.get("quantity") or 1
      size = request.POST.get("size") or "medium"
      extra_toppings = request.POST.get("extra-toppings")
      if extra_toppings:
         extra_toppings = extra_toppings.split(",")
      
      # get the pizza from the database
      pizza_id = request.POST.get("pizza-id")
      pizza = Pizza.objects.get(id=pizza_id)
      
      # do the same with drink if it is added
      drink_id = request.POST.get("drink-id")
      drink = None # default
      if drink_id:
         drink = Drink.objects.get(id=drink_id)
         
      print("DRINK", drink, drink_id)
      print("SIZE", size)
      
      # get the size from the database
      size = Size.objects.get(name=size)
      
      # get or create 'pizza price' from the database
      pizza_price, _ = PizzaPrice.objects.get_or_create(pizza=pizza, size=size, price=pizza.base_price)
      
      # add to the cart (or create a new one)
      cart, _ = Cart.objects.get_or_create(user=request.user)
      cart_item = CartItem.objects.create(cart=cart, pizza=pizza_price, quantity=quantity, drink=drink)
      
      if extra_toppings:
         toppings_in_db = Topping.objects.filter(id__in=extra_toppings)
         cart_item.toppings.set(toppings_in_db)
      
      # show the cart
      return redirect("/cart")
   
   # get the user's cart
   try:
      cart = Cart.objects.get(user=request.user)
   
      # get the cart items
      items = CartItem.objects.filter(cart=cart)
   except:
      cart = None
      items = []
   
   for item in items:
      print(item)
   
   return render(request, "cart.html", {"cart": cart, "items": items})

def delete_cart_item(request):
   if request.method == "POST":
        cart_item_id = request.POST.get("id")

        try:
            cart_item = CartItem.objects.get(id=cart_item_id, cart__user=request.user)
        except CartItem.DoesNotExist:
            return HttpResponseBadRequest("Bro dont try to delete another bro's mukbang, dude.")

        cart_item.delete()
        return redirect("/cart")


def order(request):
   if request.method == "POST":
      # get the user's cart
      cart = Cart.objects.get(user=request.user)
      
      # get the cart items
      items = CartItem.objects.filter(cart=cart)
      
      # create order from cart
      new_order = Order.objects.create(user=request.user, total_price=cart.total_price())
      
      # add order items to order from cart
      for item in items:
         # create order item
         new_order_item = OrderItem.objects.create(
            order=new_order, 
            pizza=item.pizza, 
            drink=item.drink, 
            quantity=item.quantity
         )
         
         new_order_item.toppings.set(item.toppings.all())
         new_order_item.save()
         
      # clear / delete the cart
      cart.delete()
      
      return redirect("/order")
   
   return render(request, "order.html", {"message": "Thank you for your order"})

def past_orders(request):
    if not request.user.is_authenticated:
        return redirect("/login")
    
    orders = (
        Order.objects.filter(user=request.user)
        .prefetch_related("orderitems__pizza", "orderitems__drink", "orderitems__toppings")
        .order_by("-created_at")
    )
    
    return render(request, "past-orders.html", {"orders": orders})