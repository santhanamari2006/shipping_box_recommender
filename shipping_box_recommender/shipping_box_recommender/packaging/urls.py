
from django.urls import path
from . import views

urlpatterns = [
    # Home page
    path("", views.home, name="home"),

    # Customer pages
    path("register/", views.register, name="register"),
    path("login/", views.customer_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("products/", views.product_list, name="product_list"),

    # Customer purchasing
    path(
        "buy/<int:product_id>/",
        views.buy_product,
        name="buy_product"
    ),
    path(
        "finish-purchase/",
        views.finish_purchase,
        name="finish_purchase"
    ),
    path(
        "order-summary/<int:order_id>/",
        views.order_summary,
        name="order_summary"
    ),

    # Packaging staff pages
    path(
        "create-staff/",
        views.create_staff,
        name="create_staff"
    ),
    path(
        "staff-login/",
        views.staff_login,
        name="staff_login"
    ),
    path(
        "warehouse-dashboard/",
        views.warehouse_dashboard,
        name="warehouse_dashboard"
    ),
    path(
        "warehouse-packing/<int:order_id>/",
        views.warehouse_packing,
        name="warehouse_packing"
    ),
]
