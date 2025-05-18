from django.shortcuts import render, redirect
from .models import Pizza, Drink, Topping, User, Cart, CartItem, Size, PizzaPrice, Order, OrderItem
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

def home(request):
   all_pizzas = Pizza.objects.all()
   
   return render(request, "home.html", {"pizzas": all_pizzas})

def menu(request):
   all_pizzas = Pizza.objects.all()
   all_drinks = Drink.objects.all()
   return render(request, "menu.html", {"pizzas": all_pizzas, "drinks": all_drinks})

def select_pizza(request, pizza_id):
   pizza = Pizza.objects.get(id=pizza_id)
   drinks = Drink.objects.all()
   toppings = Topping.objects.all()
   available_topping_ids = pizza.available_toppings.values_list('id', flat=True)
   
   return render(request, "select-pizza.html", {
      "pizza": pizza, 
      "drinks": drinks, 
      "toppings": toppings,
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
      

def cart(request):
   # handle add to cart
   if request.method == "POST":
      # check if user is logged in
      if not request.user.is_authenticated:
         return redirect("/login")
      
      # get the details from the form (from frontend)
      quantity = request.POST.get("quantity")
      size = request.POST.get("size")
      extra_toppings = request.POST.get("extra-toppings")
      
      # get the pizza from the database
      pizza_id = request.POST.get("pizza-id")
      pizza = Pizza.objects.get(id=pizza_id)
      
      # get the size from the database
      size = Size.objects.get(name=size)
      
      # get or create 'pizza price' from the database
      pizza_price, _ = PizzaPrice.objects.get_or_create(pizza=pizza, size=size, price=pizza.base_price)
      
      # add to the cart (or create a new one)
      cart, _ = Cart.objects.get_or_create(user=request.user)
      CartItem.objects.create(cart=cart, pizza=pizza_price, quantity=quantity)
      
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
      