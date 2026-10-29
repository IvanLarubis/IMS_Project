
from django.urls import path
from . import views


urlpatterns = [

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

    # Add new product
    path(
        'add/',
        views.add_product,
        name='add_product'
    ),

    # Edit existing product
    path(
        'edit/<int:pk>/',
        views.edit_product,
        name='edit_product'
    ),

    # Delete product
    path(
        'delete/<int:pk>/',
        views.delete_product,
        name='delete_product'
    ),

    # =====================================
    # CUSTOMER ORDER MANAGEMENT
    # =====================================

    # Display all customer orders
    path(
        'orders/',
        views.customer_orders,
        name='customer_orders'
    ),

    # Add new customer order
    path(
        'orders/add/',
        views.add_customer_order,
        name='add_customer_order'
    ),

    # Update customer order status
    path(
        'orders/status/<int:pk>/',
        views.update_order_status,
        name='update_order_status'
    ),

    # =====================================
    # PRINT CUSTOMER RECEIPT
    # =====================================

    # View and print receipt
    path(
        'orders/receipt/<int:pk>/',
        views.print_receipt,
        name='print_receipt'
    ),

]
