from django.shortcuts import render, redirect
from .models import Pizza, Drink, Topping, User
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
   if request.method == "POST":
      if not request.user.is_authenticated:
         return redirect("/login")
      
      # do more stuff here later
      quantity = request.POST.get("quantity")
      size = request.POST.get("size")
      extra_toppings = request.POST.get("extra-toppings")
      
      print(request.POST)
      
      return render(request, "cart.html")
      
   if request.method == "GET":
      return render(request, "cart.html")