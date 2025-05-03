from django.urls import path
from . import views

app_name = "application"
urlpatterns = [
    path("", views.home, name="home"),
    path("menu", views.menu, name="menu"),
    path("menu/select-pizza/<int:pizza_id>/", views.select_pizza, name="select-pizza"),
    path("login", views.login, name="login"),
    path("signup", views.signup, name="signup"),
    path("cart", views.cart, name="cart"),
    path("logout", views.logout, name="logout")
]
