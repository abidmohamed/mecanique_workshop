from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from buyorder.models import BuyOrder
from category.models import Category
from product.forms import ProductForm
from product.models import Product
from sellorder.models import Order, OrderItem


def delete_duplicated(request):
    # assuming which duplicate is removed doesn't matter...
    for current_prod in Product.objects.all().reverse():
        if Product.objects.filter(ref=current_prod.ref).count() > 1:
            current_prod.delete()

    return HttpResponse("Duplicate Deleted")


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
    all_buyorders = BuyOrder.objects.all()

    chosen_orders = Order.objects.none()
    chosen_buyorders = BuyOrder.objects.none()

    pieces = OrderItem.objects.none()
    buy_pieces = OrderItem.objects.none()

    quantities = []
    buy_quantities = []

    sell_quantity = 0
    buy_quantity = 0
    # Sell orders product count
    for order in all_sellorders:
        print("###### ORDER")
        for item in order.items.all():

            if item.stockproduct.product.id == product.id:
                print("####### ITEM FOUND")
                print(item.stockproduct.product)
                print(product)
                chosen_orders |= Order.objects.all().filter(id=order.id)
                pieces |= order.items.all().filter(id=item.id)
                sell_quantity += item.quantity
                quantities.append(item.quantity)
                # print(order.items.all().filter(id=item.id))
    final_list = zip(chosen_orders, pieces, quantities)

    # Buy orders product count
    for order in all_buyorders:
        for item in order.items.all():
            if item.product == product:
                chosen_buyorders |= BuyOrder.objects.all().filter(id=order.id)
                buy_pieces |= order.items.all().filter(id=item.id)
                buy_quantity += item.quantity
                buy_quantities.append(item.quantity)
    final_buylist = zip(chosen_buyorders, buy_pieces, buy_quantities)
    context = {
        'product': product,
        'pieces': pieces,
        'final_list': final_list,
        'final_buylist': final_buylist,
        'chosen_orders': chosen_orders,
        'sell_quantity': sell_quantity,
        'buy_quantity': buy_quantity,
    }
    return render(request, 'product/details.html', context)


def delete_product(request, pk):
    product = Product.objects.get(id=pk)
    context = {'product': product}
    if request.method == 'POST':
        product.delete()
        return redirect('/')
    return render(request, 'product/delete.html', context)
