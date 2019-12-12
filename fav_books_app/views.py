from django.shortcuts import render, redirect, HttpResponse

from django.contrib import messages

from login.models import User, Book

# Create your views here.
def welcome(request):
    if not "userid" in request.session:
        messages.error(request, "You are not logged in.")
        return redirect("/")
    else:
        context = {
            "user": User.objects.get(id=request.session["userid"]),
            "books": Book.objects.all(),
        }
    return render(request, "show_fav_books.html", context)

def add_book(request):
    if not "userid" in request.session:
        messages.error(request, "You are not logged in.")
        return redirect("/")

    print("*" *20)
    print(request.POST)
    errors2 = Book.objects.basic_validator(request.POST)
    if len(errors2) > 0:
        for key, value in errors2.items():
            messages.error(request, value)
    else:
        b = Book.objects.create(title=request.POST["title"], desc=request.POST["desc"], uploaded_by=User.objects.get(id=request.session["userid"]))
        b.users_who_like.add(User.objects.get(id=request.session["userid"]))
        b.save()
        
    return redirect("/welcome")

def fav_helper(request, bookId):
    b = Book.objects.get(id=bookId)
    u = User.objects.get(id=request.session["userid"])
    b.users_who_like.add(u)
    b.save()

def fav(request, bookId):
    if not "userid" in request.session:
        messages.error(request, "You are not logged in.")
        return redirect("/")

    fav_helper(request, bookId)
    return redirect("/welcome")

def fav_inside(request, bookId):
    if not "userid" in request.session:
        messages.error(request, "You are not logged in.")
        return redirect("/")

    fav_helper(request, bookId)
    return redirect("/book/"+ str(bookId))

def read_book(request, bookId):
    if not "userid" in request.session:
        messages.error(request, "You are not logged in.")
        return redirect("/")

    # print("*" *40)
    # print(request.POST)
    if request.method == "POST":    
        errors2 = Book.objects.basic_validator(request.POST)
        if len(errors2) > 0:
            for key, value in errors2.items():
                messages.error(request, value)
                print(len(request.POST["desc"]))
        else:
            print("*" *40)
            print(request.POST["title"])
            b = Book.objects.get(id=bookId)
            b.title = request.POST["title"]
            b.desc = request.POST["desc"]
            b.save()
            return redirect("/welcome")
            #return redirect("/book/"+ str(bookId))

    context = {
            "user": User.objects.get(id=request.session["userid"]),
            "book": Book.objects.get(id=bookId),
        }
    
    return render(request, "edit_book.html", context)

def un_fav(request, bookId):
    if not "userid" in request.session:
        messages.error(request, "You are not logged in.")
        return redirect("/")
    
    b = Book.objects.get(id=bookId)
    u = User.objects.get(id=request.session["userid"])
    b.users_who_like.remove(u)
    b.save()
    return redirect("/book/"+ str(bookId))

# def edit_book(request, bookId):
#     if not "userid" in request.session:
#         messages.error(request, "You are not logged in.")
#         return redirect("/")

#     context = {
#             "user": User.objects.get(id=request.session["userid"]),
#             "book": Book.objects.get(id=bookId),
#         }
    
#     return render(request, "edit_book.html", context)

def delete_book(request, bookId):
    if not "userid" in request.session:
        messages.error(request, "You are not logged in.")
        return redirect("/")
    
    Book.objects.get(id=bookId).delete()

    return redirect("/welcome")