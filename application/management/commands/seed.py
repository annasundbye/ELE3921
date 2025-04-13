from django.core.management.base import BaseCommand
from application.models import Pizza, Drink

DEFAULT_PIZZAS = [
   Pizza(name="Basic AF (Margherita)", base_price=259.99, icon="🍅", description="Safe choice. Boring tho."),
   Pizza(name="You can't take this (Pepperoni)", base_price=229.99, icon="🍕", description="Loaded with pepperoni for when you're feeling extra. No cap."),
   Pizza(name="This one hot (Nduja)", base_price=299.99, icon="🌶️", description="Bro. Bro. Bro! This is hot."),
   Pizza(name="Cheesy x 4 (Quatro Formaggi)", base_price=219.99, icon="🧀", description="Just cheese. No explanation needed. It's giving simplicity."),
   Pizza(name="No nothing (Vegan (none slayed))", base_price=119.99, icon="🥦", description="Veggies on veggies on veggies. It's the responsible choice."),
   Pizza(name="All the good stuff (Hella meat)", base_price=319.99, icon="🥩", description="Hella meat."),
]

DEFAULT_DRINKS = [
   Drink(name="Orange juice", price=39.99, icon="🍊", description="I see you're thirsty..."),
   Drink(name="Lemonade", price=59.99, icon="🍋", description="I see you're thirsty..."),
   Drink(name="Ice Tea", price=45.99, icon="🌱", description="I see you're thirsty..."),
   Drink(name="Coca Cola", price=49.99, icon="🥤", description="I see you're thirsty..."),
   Drink(name="Water", price=49.99, icon="💦", description="I see you're thirsty..."),
   Drink(name="Sparkling Water", price=49.99, icon="🫧", description="I see you're thirsty..."),
]


class Command(BaseCommand):
    help = "Seed the database with default pizzas and drinks"

    def handle(self, *args, **kwargs):
        print("Inserting pizzas...")
        for pizza in DEFAULT_PIZZAS:
            pizza.save()

        print("Inserting drinks...")
        for drink in DEFAULT_DRINKS:
            drink.save()

        print("Done!")
