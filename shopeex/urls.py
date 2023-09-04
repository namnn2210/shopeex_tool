from django.urls import path
from . import views

urlpatterns = [
    path("", view=views.index, name="index"),
    path("rating", view=views.rating_order, name="rating"),
    path("accounts/login/", view=views.login, name="login"),
    path("register", view=views.register, name="register"),
    path("forgot", view=views.forgot, name="forgot")
]