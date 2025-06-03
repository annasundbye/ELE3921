from django.urls import path
from . import views

app_name = "application"
urlpatterns = [
    path("", views.home, name="home"),
    path("menu", views.menu, name="menu"),
    path("pizza/<int:pizza_id>/", views.select_pizza, name="select-pizza"),
    path("login", views.login, name="login"),
    path("signup", views.signup, name="signup"),
    path("profile", views.profile, name="profile"),
    path("change-password/", views.change_password, name="change_password"),
    path("cart", views.cart, name="cart"),
    path("logout", views.logout, name="logout"),
    path("order", views.order, name="order"),
    path("order/history", views.past_orders, name="past_orders"),
    path("order/<int:order_id>/re-order/", views.reorder, name="reorder"),
    path("cart/delete-item", views.delete_cart_item, name="delete-cart-item"),
]
