
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import (
    Sum,
    F,
    DecimalField,
    ExpressionWrapper
)
from django.db.models.deletion import ProtectedError
from django.contrib import messages

from .models import Product, CustomerOrder
from .forms import ProductForm, CustomerOrderForm


# ==========================================
# PRODUCT LIST AND DASHBOARD STATISTICS
# ==========================================
@login_required
def products_list(request):

    query = request.GET.get('q', '').strip()

    all_products = Product.objects.all()

    total_products = all_products.count()

    total_stock = all_products.aggregate(
        total=Sum('quantity')
    )['total'] or 0

    low_stock = all_products.filter(
        quantity__lt=5
    ).count()

    stock_value = ExpressionWrapper(
        F('price') * F('quantity'),
        output_field=DecimalField(
            max_digits=18,
            decimal_places=2
        )
    )

    inventory_value = all_products.aggregate(
        total=Sum(stock_value)
    )['total'] or 0

    if query:
        products = all_products.filter(
            name__icontains=query
        )
    else:
        products = all_products

    return render(
        request,
        'Invapp/products_list.html',
        {
            'products': products,
            'total_products': total_products,
            'total_stock': total_stock,
            'low_stock': low_stock,
            'inventory_value': inventory_value,
        }
    )


# ==========================================
# ADD NEW PRODUCT WITH IMAGE UPLOAD
# ==========================================
@login_required
def add_product(request):

    if request.method == 'POST':

        form = ProductForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Product added successfully!'
            )

            return redirect('products_list')

    else:
        form = ProductForm()

    return render(
        request,
        'Invapp/add_product.html',
        {
            'form': form
        }
    )


# ==========================================
# EDIT PRODUCT WITH IMAGE UPDATE
# ==========================================
@login_required
def edit_product(request, pk):

    product = get_object_or_404(
        Product,
        pk=pk
    )

    if request.method == 'POST':

        form = ProductForm(
            request.POST,
            request.FILES,
            instance=product
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Product updated successfully!'
            )

            return redirect('products_list')

    else:

        form = ProductForm(
            instance=product
        )

    return render(
        request,
        'Invapp/edit_product.html',
        {
            'form': form,
            'product': product
        }
    )


# ==========================================
# DELETE PRODUCT
# ==========================================
@login_required
@require_POST
def delete_product(request, pk):

    product = get_object_or_404(
        Product,
        pk=pk
    )

    product_name = product.name

    try:

        product.delete()

        messages.success(
            request,
            f'{product_name} deleted successfully!'
        )

    except ProtectedError:

        messages.error(
            request,
            f'Cannot delete {product_name} because it has existing customer orders.'
        )

    return redirect('products_list')


# ==========================================
# DISPLAY CUSTOMER ORDERS
# ==========================================
@login_required
def customer_orders(request):

    orders = CustomerOrder.objects.select_related(
        'product'
    ).order_by('-order_date', '-id')

    total_orders = orders.count()

    total_sales = orders.exclude(
        status='Cancelled'
    ).aggregate(
        total=Sum('total_price')
    )['total'] or 0

    return render(
        request,
        'Invapp/customer_orders.html',
        {
            'orders': orders,
            'total_orders': total_orders,
            'total_sales': total_sales,
        }
    )


# ==========================================
# ADD NEW CUSTOMER ORDER
# ==========================================
@login_required
def add_customer_order(request):

    if request.method == 'POST':

        form = CustomerOrderForm(request.POST)

        if form.is_valid():

            with transaction.atomic():

                order = form.save(commit=False)

                product = get_object_or_404(
                    Product.objects.select_for_update(),
                    pk=order.product_id
                )

                if order.quantity < 1:

                    form.add_error(
                        'quantity',
                        'Quantity must be at least 1.'
                    )

                elif order.quantity > product.quantity:

                    form.add_error(
                        'quantity',
                        'Not enough stock available. '
                        f'Only {product.quantity} left.'
                    )

                else:

                    order.price = product.price

                    order.total_price = (
                        order.price * order.quantity
                    )

                    order.status = 'Pending'

                    product.quantity -= order.quantity

                    product.save(
                        update_fields=['quantity']
                    )

                    order.save()

                    messages.success(
                        request,
                        'Customer order saved successfully!'
                    )

                    return redirect('customer_orders')

    else:

        form = CustomerOrderForm()

    product_data = {
        str(product.id): {
            'name': product.name,
            'price': str(product.price),
            'stock': product.quantity,
        }
        for product in Product.objects.all()
    }

    return render(
        request,
        'Invapp/add_customer_order.html',
        {
            'form': form,
            'product_data': product_data,
        }
    )


# ==========================================
# UPDATE CUSTOMER ORDER STATUS
# ==========================================
@login_required
@require_POST
def update_order_status(request, pk):

    new_status = request.POST.get('status')

    valid_statuses = [
        'Pending',
        'Completed',
        'Cancelled'
    ]

    if new_status not in valid_statuses:

        messages.error(
            request,
            'Invalid order status.'
        )

        return redirect('customer_orders')

    with transaction.atomic():

        order = get_object_or_404(
            CustomerOrder.objects.select_for_update(),
            pk=pk
        )

        old_status = order.status

        if old_status == new_status:

            messages.info(
                request,
                'Order status is already updated.'
            )

            return redirect('customer_orders')

        if new_status == 'Cancelled':

            if old_status != 'Cancelled':

                product = Product.objects.select_for_update().get(
                    pk=order.product_id
                )

                product.quantity += order.quantity

                product.save(
                    update_fields=['quantity']
                )

        elif old_status == 'Cancelled':

            messages.error(
                request,
                'Cancelled orders cannot be reactivated. '
                'Please create a new order.'
            )

            return redirect('customer_orders')

        order.status = new_status

        order.save(
            update_fields=['status']
        )

    messages.success(
        request,
        f'Order #{pk} updated to {new_status}!'
    )

    return redirect('customer_orders')


# ==========================================
# PRINT CUSTOMER RECEIPT
# ==========================================
@login_required
def print_receipt(request, pk):

    order = get_object_or_404(
        CustomerOrder.objects.select_related('product'),
        pk=pk
    )

    return render(
        request,
        'Invapp/receipt.html',
        {
            'order': order
        }
    )
