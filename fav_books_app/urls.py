from django.urls import path

from . import views

import login

urlpatterns = [
    path('welcome', views.welcome),
    path('add_book', views.add_book),
    path('book/<int:bookId>/fav', views.fav),
    path('book/<int:bookId>', views.read_book),
    path('book/<int:bookId>/delete', views.delete_book),
    path('book/<int:bookId>/edit', views.read_book),
    path('book/<int:bookId>/un_fav', views.un_fav),
    path('book/<int:bookId>/fav_inside', views.fav_inside),
]