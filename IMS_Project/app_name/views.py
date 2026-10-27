
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.db.models import Sum, F, DecimalField, ExpressionWrapper

from .models import Product
from .forms import ProductForm


# DISPLAY PRODUCTS, SEARCH, AND DASHBOARD STATISTICS
def products_list(request):
    query = request.GET.get('q', '')

    # All products in database
    all_products = Product.objects.all()

    # Total number of products
    total_products = all_products.count()

    # Total quantity of all products
    total_stock = all_products.aggregate(
        total=Sum('quantity')
    )['total'] or 0

    # Products with quantity below 5
    low_stock = all_products.filter(
        quantity__lt=5
    ).count()

    # Calculate price multiplied by quantity
    stock_value = ExpressionWrapper(
        F('price') * F('quantity'),
        output_field=DecimalField(
            max_digits=18,
            decimal_places=2
        )
    )

    # Total inventory value
    inventory_value = all_products.aggregate(
        total=Sum(stock_value)
    )['total'] or 0

    # Search products by name
    if query:
        products = all_products.filter(
            name__icontains=query
        )
    else:
        products = all_products

    return render(request, 'Invapp/products_list.html', {
        'products': products,
        'total_products': total_products,
        'total_stock': total_stock,
        'low_stock': low_stock,
        'inventory_value': inventory_value,
    })


# ADD NEW PRODUCT
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('products_list')
    else:
        form = ProductForm()

    return render(request, 'Invapp/add_product.html', {
        'form': form
    })


# EDIT EXISTING PRODUCT
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(
            request.POST,
            instance=product
        )

        if form.is_valid():
            form.save()
            return redirect('products_list')
    else:
        form = ProductForm(instance=product)

    return render(request, 'Invapp/edit_product.html', {
        'form': form,
        'product': product
    })


# DELETE PRODUCT
@require_POST
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()

    return redirect('products_list')
