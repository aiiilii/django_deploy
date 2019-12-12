from django.shortcuts import render, redirect, HttpResponse

from django.contrib import messages

from .models import User, Book

import bcrypt

import fav_books_app.urls

# Create your views here.
def index(request):
    return render(request, "login.html")

def register(request):
    if len(User.objects.filter(email=request.POST["email"])):
        return redirect("/")
    else:
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
        else:
            hash1 = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt()).decode()
            print(hash1)
            newuser = User.objects.create(first_name=request.POST["first_name"], last_name=request.POST["last_name"], email=request.POST["email"], password=hash1)
            request.session["userid"] = newuser.id
            #messages.success(request, "User successfully registered!")
            return redirect("/welcome")
    return redirect("/")

def login(request):
    try:
        User.objects.get(email=request.POST["email"])
    except:
        messages.error(request,"User does not exist.")
        return redirect("/")
    email_match = User.objects.get(email=request.POST["email"]) 
    if bcrypt.checkpw(request.POST["password"].encode(), email_match.password.encode()):
        request.session["userid"] = email_match.id
        #messages.success(request, "Successfully logged in!")
        return redirect("/welcome")
    else:
        messages.error(request, "Incorrect password.")
        return redirect("/")

def logout(request):
    request.session.clear()
    return redirect("/")