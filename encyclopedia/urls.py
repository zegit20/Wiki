from django.contrib import admin 
from django.urls import path, include 


from . import views
app_name = "encyclopedia"
urlpatterns = [
    path('', views.index, name="index"),
    path('wiki/<str:name>',views.show, name="show"),
      path('search/', views.search, name="search"),
    path('create/', views.create, name="create"),
    path('edit/<str:name>', views.edit, name="edit"),
    path('wiki/', views.random1, name="random1")
]
