from django.urls import path
from . import views

urlpatterns = [
    path("", view=views.index, name="index"),
    path("rating", view=views.rating_order, name="rating"),
    path("accounts/login/", view=views.login_view, name="login"),
    path("accounts/logout/", view=views.logout_view, name="logout"),
    path("get_info", view=views.get_info, name="get_info"), 
    path("register", view=views.register, name="register"),
    path("forgot", view=views.forgot, name="forgot")
]