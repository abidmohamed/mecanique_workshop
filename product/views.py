from datetime import datetime, date

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from accounts.models import CurrentYear
from buyorder.models import BuyOrder
from caisse.forms import DateForm
from category.models import Category
from product.forms import ProductForm
from product.models import Product
from sellorder.models import Order, OrderItem
from stock.models import StockProduct


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

            StockProduct.objects.create(
                product=product,
                quantity=0,
                stock=product.stock
            )

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
    current_year = CurrentYear.objects.all().filter()[:1].get()
    products = Product.objects.all()
    context = {
        'products': products,
        'current_year': current_year,
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
    dateform = DateForm()
    # now time
    now = datetime.now()

    all_sellorders = Order.objects.all().filter(confirmed=True, created__year=now.year, created__day=now.day,
                                                created__month=now.month)
    all_buyorders = BuyOrder.objects.filter(created__year=now.year, created__day=now.day,
                                            created__month=now.month)

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
            if StockProduct.objects.filter(product=product):
                if item.stockproduct is not None:
                    if item.stockproduct.product == product:
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

    if request.method == 'POST':
        alldata = request.POST

        # Search by date
        chosen_date = alldata.get("date")
        chosen_date = chosen_date.split("-", 1)
        chosen_start_date = chosen_date[0]
        chosen_end_date = chosen_date[1]

        chosen_start_date = chosen_start_date.split("/", 2)
        start_month = chosen_start_date[0]
        start_year = chosen_start_date[2]
        start_day = chosen_start_date[1]
        # Remove white spaces
        start_year = ''.join(start_year.split())
        start_month = ''.join(start_month.split())
        start_day = ''.join(start_day.split())

        chosen_end_date = chosen_end_date.split("/", 2)
        end_month = chosen_end_date[0]
        end_year = chosen_end_date[2]
        end_day = chosen_end_date[1]
        # Remove white spaces
        end_year = ''.join(end_year.split())
        end_month = ''.join(end_month.split())
        end_day = ''.join(end_day.split())

        # filtering orders
        all_sellorders = Order.objects.all().filter(
            Q(
                order_date__gt=date(int(start_year), int(start_month),
                                    int(start_day)),
                order_date__lt=date(int(end_year), int(end_month), int(end_day))
            )
            |
            Q(
                order_date=date(int(end_year), int(end_month), int(end_day))
            )
            , confirmed=True, factured=False,
        )
        all_buyorders = BuyOrder.objects.filter(
            Q(
                order_date__gt=date(int(start_year), int(start_month),
                                    int(start_day)),
                order_date__lt=date(int(end_year), int(end_month), int(end_day))
            )
            |
            Q(
                order_date=date(int(end_year), int(end_month), int(end_day))
            )
        )

        # boucle orders
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
                if StockProduct.objects.filter(product=product):
                    if item.stockproduct is not None:
                        if item.stockproduct.product == product:
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
        'dateform': dateform,
    }
    return render(request, 'product/details.html', context)


def delete_product(request, pk):
    product = Product.objects.get(id=pk)
    context = {'product': product}
    if request.method == 'POST':
        product.delete()
        return redirect('/')
    return render(request, 'product/delete.html', context)
