from django.urls import path

from . import views

urlpatterns = [
	path("", views.index, name="index"),
	path("login", views.login_view, name="login"),
	path("register", views.register, name="register"),
	path("logout", views.logout_view, name="logout"),
	path("search", views.search, name="search"),
	path("cart", views.cart, name="cart"),
	path("edit", views.edit_view, name="edit_view"),
	path("add_item", views.add_item, name="add_item"),
	path("favorite", views.favorite, name="favorite"),
	path("checkout", views.checkout, name="checkout"),
	path("orders", views.orders, name="orders"),
	path("add_favorite/<str:restaurant_id>", views.favorite, name="add_favorite"),
	path("edit/<str:food_name>", views.edit_item, name="edit_item"),
	path("add/<str:food_name>", views.add_cart, name="add"),
	path("rem/<str:food_name>", views.remove_item, name="remove"),
	path("delete/<str:food_name>", views.delete_item, name="delete"),
	path("accept/<int:order_id>", views.accept, name="accept"),
	path("decline/<int:order_id>", views.decline, name="decline"),
	path("restaurants/<int:restaurant_id>", views.restaurant_view, name="restaurant_view")
]