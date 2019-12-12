from django.urls import path

from . import views

import fav_books_app

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),

]