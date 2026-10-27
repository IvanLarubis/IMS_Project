from django.urls import path
from . import views

urlpatterns = [
    path('', views.products_list, name='products_list'),
    path('products/', views.products_list, name='products_list'), # I-add kini aron mo-work ang /products/
    path('add/', views.add_product, name='add_product'),
]