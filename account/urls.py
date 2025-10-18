from django.contrib import admin
from django.urls import path
from .views import*

urlpatterns = [
    path("",login_view,name="login"),
    path("register/",register,name="register"),
    path("notes/",notes,name="notes"),
    path("admin_panel",admin_panel,name="admin_panel")
]
