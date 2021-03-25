from django.shortcuts import render, redirect

# Create your views here.
from category.models import Category
from product.forms import ProductForm
from product.models import Product
from sellorder.models import Order


def add_product(request):
    if request.method == 'GET':
        productform = ProductForm()
    elif request.method == 'POST':
        productform = ProductForm(request.POST, request.FILES)
        if productform.is_valid():
            product = productform.save()
            return redirect("product:all_product_list")
    context = {'productform': productform}
    return render(request, 'product/add_product.html', context)


# from add buyorder we can product
def add_product_buyorder(request):
    if request.method == 'GET':
        productform = ProductForm()
    elif request.method == 'POST':
        productform = ProductForm(request.POST, request.FILES)
        print("----------------BUY ORDER ADD PRODUCT")
        if productform.is_valid():
            product = productform.save()
            return redirect("buyorder:create_buyorder")
    context = {'productform': productform}
    return render(request, 'product/add_product.html', context)

# def product_list(request, pk):
#     category = Category.objects.get(id=pk)
#     products = Product.objects.all().filter(category=category)
#     context = {
#         'products': products,
#     }
#     return render(request, 'product/list_product.html', context)


def all_product_list(request):
    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'product/all_product_list.html', context)


def update_product(request, pk):
    product = Product.objects.get(id=pk)
    productform = ProductForm(instance=product)
    if request.method == 'POST':
        productform = ProductForm(request.POST, request.FILES, instance=product)
        if productform.is_valid():
            productform.save()
            return redirect('/')
    context = {'productform': productform}
    return render(request, 'product/add_product.html', context)


def detail_product(request, pk):
    product = Product.objects.get(id=pk)
    all_sellorders = Order.objects.all().filter(confirmed=True)
    chosen_orders = Order.objects.none()
    for order in all_sellorders:
        for item in order.items.all():
            if item.stockproduct.product == product:
                chosen_orders |= Order.objects.all().filter(id=order.id)

    context = {
        'product': product,
        'chosen_orders': chosen_orders,
    }
    return render(request, 'product/details.html', context)

def delete_product(request, pk):
    product = Product.objects.get(id=pk)
    context = {'product': product}
    if request.method == 'POST':
        product.delete()
        return redirect('/')
    return render(request, 'product/delete.html', context)
