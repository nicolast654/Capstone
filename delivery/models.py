from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

objects = models.Manager()

class User(AbstractUser):
	restaurant = models.BooleanField(default=False)
	cart = models.ManyToManyField("Order", blank=True, related_name="cart")
	favorite = models.ManyToManyField("Restaurant", blank=True, related_name="favorites")
	orders = models.ManyToManyField("Order", blank=True, related_name="orders")

class Food(models.Model):
	name = models.CharField(max_length=64)
	price = models.FloatField()
	description = models.TextField(blank=True)
	restaurant = models.ForeignKey("Restaurant", on_delete=models.CASCADE, related_name="food_restaurant")

	def __str__(self):
		return f"{self.name}"

class Restaurant(models.Model):
	NUMBERS = ((1,"1"),(2,"2"),(3,"3"),(4,"4"),(5,"5"))
	user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="restaurant_user")
	food = models.ManyToManyField("Food", related_name="food")
	orders = models.ManyToManyField("Order", related_name="restaurant_order")
	
	def __str__(self):
		return f"{self.user.username}"

class Order(models.Model):
	quantity = models.IntegerField()
	food = models.ForeignKey("Food", on_delete=models.CASCADE, related_name="ordered_food")
	user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="order_user")
	status = models.CharField(max_length=64, blank=True, null=True)
	viewed = models.BooleanField(default=False)

	def __str__(self):
		return f"{self.quantity} {self.food.name}"