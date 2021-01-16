from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .models import User, Restaurant, Food, Order

# Create your views here.
def index(request):
    try:
        if request.user.restaurant:
            restaurant = Restaurant.objects.get(user=request.user)
            orders = restaurant.orders.all()[::-1]
            p = Paginator(orders, 10)
            page = request.GET.get('page')

            if len(restaurant.orders.all()) == 0:
                no_orders = True
            else:
                no_orders = False

                if page != None:
                    try:
                        orders = p.page(page)
                    except:
                        orders = p.page(1)
                else:
                    orders = p.page(1)

            return render(request, "delivery/restaurant.html", {"no_orders":no_orders, "orders":orders, "p":p})
        else:
            restaurants = Restaurant.objects.all()
            p = Paginator(restaurants, 10)
            page = request.GET.get('page')
            if page != None:
                try:
                    restaurants = p.page(page)
                except:
                    restaurants = p.page(1)
            else:
                restaurants = p.page(1)
            return render(request, "delivery/index.html", {"restaurants":restaurants,"favorites": request.user.favorite.all(), "p":p})
   
    except Exception as e:
        print(e)
        return render(request, "delivery/index.html", {"restaurants":Restaurant.objects.all()})

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "delivery/login.html", {
                "message": "Invalid username and/or password."
                })
    else:
        return render(request, "delivery/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        restaurant = request.POST["restaurant"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "delivery/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            if restaurant == "True":
                user = User.objects.create_user(username, email, password, restaurant=True)
                user.save()
                restaurant = Restaurant(user=user)
                restaurant.save()

            elif restaurant == "False":
                user = User.objects.create_user(username, email, password, restaurant=False)
                user.save()

        except Exception as e:
            print(e)
            return render(request, "delivery/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "delivery/register.html")

def search(request):
    searched_item = request.GET["q"]
    restaurants = Restaurant.objects.all()
    searched = []

    for restaurant in restaurants:
        if searched_item.lower() == restaurant.user.username.lower():
            return HttpResponseRedirect(reverse("restaurant_view", kwargs={"restaurant_id":restaurant.id}))
        elif searched_item.lower() in restaurant.user.username.lower() or searched_item.lower()[:2] == restaurant.user.username.lower()[:2]:
            searched.append(restaurant)

    if len(searched) == 0:   
        return render(request, "delivery/search.html", {"restaurants":searched, "message":"No item matched your search"})
    
    p = Paginator(searched, 10)
    page = request.GET.get("page")
    if page != None:
        try:
            searched = p.page(page)
        except:
            searched = p.page(1)
    else:
        searched = p.page(1)
    return render(request, "delivery/search.html", {"restaurants":searched})
        

def restaurant_view(request, restaurant_id):
    restaurant = Restaurant.objects.get(pk=restaurant_id)
    menu = restaurant.food.all()
    return render(request, "delivery/restaurant_menu.html", {"restaurant":restaurant, "menu":menu})

@login_required
def add_cart(request, food_name):
    if request.method == "POST":
        food = Food.objects.get(name=food_name)
        quantity = int(request.POST["number"])
        cart = request.user.cart
        order = Order(quantity=quantity, food=food, user=request.user)
        order.save()

        for i in cart.all():
            if i.food.name == order.food.name:
                order.quantity += i.quantity
                order.save()
                i.delete()
        cart.add(order)

        return HttpResponseRedirect(reverse("cart"))

@login_required
def remove_item(request, food_name):
    if request.method == "POST":
        food = Food.objects.get(name=food_name)
        order = Order.objects.get(food=food, user=request.user)
        if order.quantity > 1:
            order.quantity -= 1
            order.save()
        else:
            order.delete()
        return HttpResponseRedirect(reverse("cart"))

@login_required
def cart(request):
    cart = request.user.cart.all()
    total = 0
    for item in cart:
        total += item.food.price * item.quantity
    total = round(total,2)
    return render(request, "delivery/cart.html", {"cart":cart, "total":total})

def edit_view(request):
    try:
        if request.user.restaurant:
            restaurant = Restaurant.objects.get(user=request.user)
            return render(request, "delivery/edit.html", {"menu":restaurant.food.all()})
        return HttpResponseRedirect(reverse("index"))
    except Exception as e:
        print(e)
        return HttpResponseRedirect(reverse("index"))

def delete_item(request, food_name):
    if request.method == "POST":
        food = Food.objects.get(name=food_name)
        food.delete()
        return HttpResponseRedirect(reverse("edit_view"))

def edit_item(request, food_name):
    if request.method == "POST":
        food = Food.objects.get(name=food_name)
        new_price = float(request.POST["price"])
        new_description = request.POST["description"]

        food.price = new_price
        food.description = new_description
        food.save()
        return HttpResponseRedirect(reverse("edit_view"))


def add_item(request):
    if request.method == "POST":
        restaurant = Restaurant.objects.get(user=request.user)
        name = request.POST["name"]
        description = request.POST["description"]
        price = float(request.POST["price"])

        try:
            for food in restaurant.food.all():
                if name == food.name:
                    raise IntegrityError
            food = Food(name=name, description=description, price=price, restaurant=restaurant)
            food.save()
            restaurant.food.add(food)
            return HttpResponseRedirect(reverse("edit_view"))
        except IntegrityError:
            return HttpResponseRedirect(reverse("index"))


def favorite(request, restaurant_id=0):
    if request.method == "GET":
        favorites = request.user.favorite.all()
        p = Paginator(favorites, 10)
        page = request.GET.get('page')

        if page != None:
            try:
                favorites = p.page(page)
            except:
                favorites = p.page(1)
        else:
            favorites = p.page(1)

        if len(request.user.favorite.all())>0:
            empty = False
        else:
            empty = True
        return render(request, "delivery/favorite.html", {"favorites": request.user.favorite.all(), "empty":empty})

    elif request.method == "POST":
        restaurant=Restaurant.objects.get(pk=restaurant_id)
        if restaurant in request.user.favorite.all():
            request.user.favorite.remove(restaurant)
        else:
            request.user.favorite.add(restaurant)

    return HttpResponseRedirect(reverse("favorite"))

def checkout(request):
    if request.method == "POST":
        cart = request.user.cart
        restaurants = set()

        #get all the restaurants that the user ordered from
        for item in cart.all():
            restaurants.add(item.food.restaurant)

        #add to each restaurant the order
        for restaurant in restaurants:
            for item in cart.all():
                if item.food.restaurant == restaurant:
                    restaurant.orders.add(item)
                    cart.remove(item)
                    request.user.orders.add(item)

        return HttpResponseRedirect(reverse("index"))

def accept(request, order_id):
    if request.method == "POST":
        order = Order.objects.get(pk=order_id)
        order.status = "accepted"
        order.viewed = True
        order.save()
        
    return HttpResponseRedirect(reverse("index"))

def decline(request, order_id):
    if request.method == "POST":
        order = Order.objects.get(pk=order_id)
        order.status = "declined"
        order.viewed = True
        order.save()

    return HttpResponseRedirect(reverse("index"))
    
def orders(request):
    return render(request, "delivery/orders.html",{"user":request.user, "orders":request.user.orders.all()})

    