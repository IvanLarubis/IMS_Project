from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [

    # =====================================
    # LOGIN AND LOGOUT
    # =====================================

    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='Invapp/login.html'
        ),
        name='login'
    ),

    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),

    # =====================================
    # DASHBOARD AND PRODUCT LIST
    # =====================================

    path(
        '',
        views.products_list,
        name='products_list'
    ),

    path(
        'products/',
        views.products_list,
        name='products'
    ),

    # =====================================
    # PRODUCT MANAGEMENT
    # =====================================

    path(
        'add/',
        views.add_product,
        name='add_product'
    ),

    path(
        'edit/<int:pk>/',
        views.edit_product,
        name='edit_product'
    ),

    path(
        'delete/<int:pk>/',
        views.delete_product,
        name='delete_product'
    ),

    # =====================================
    # CUSTOMER ORDER MANAGEMENT
    # =====================================

    path(
        'orders/',
        views.customer_orders,
        name='customer_orders'
    ),

    path(
        'orders/add/',
        views.add_customer_order,
        name='add_customer_order'
    ),

    path(
        'orders/status/<int:pk>/',
        views.update_order_status,
        name='update_order_status'
    ),

    # =====================================
    # PRINT CUSTOMER RECEIPT
    # =====================================

    path(
        'orders/receipt/<int:pk>/',
        views.print_receipt,
        name='print_receipt'
    ),

]