from django.urls import path
from . import views

urlpatterns = [
    path("", view=views.index, name="index"),
    path("rating", view=views.add_rating_order, name="rating"),
    path("rating/list", view=views.list_rating_order, name="list_rating"),
    path("accounts/login/", view=views.login_view, name="login"),
    path("accounts/logout/", view=views.logout_view, name="logout"),
    # path("get_info", view=views.get_info, name="get_info"),
    # path("get_orders", view=views.get_orders, name="get_orders"), 
    path("register", view=views.register, name="register"),
    path("forgot", view=views.forgot, name="forgot"),
    path("data/insert",view=views.save_data, name="save_data")
]