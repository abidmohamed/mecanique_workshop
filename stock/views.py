from datetime import date

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from accounts.models import CurrentYear
from buyorder.models import BuyOrderItem, BuyOrder
from caisse.forms import DateForm
from category.models import Category
from customer.models import Customer
from product.models import Product
from rdv.models import Panne
from sellorder.models import Order, OrderItem, PanneItem, ServiceItem
from services.models import Service, ServiceProvider
from stock.forms import StockForm, StockProductForm
from stock.models import Stock, StockProduct
from vehicule.models import Vehicle


def putit_in_stock(request):
    stockproducts = StockProduct.objects.all()
    for stockproduct in stockproducts:
        if stockproduct.stock is None:
            stockproduct.stock = Stock.objects.get(id=2)
            stockproduct.save()
        elif stockproduct.quantity <= -13:
            stockproduct.quantity = 0
    return HttpResponse("All stocked")


def delete_duplicated_stockproduct(request):
    # assuming which duplicate is removed doesn't matter...
    stocks = Stock.objects.all()
    for stock in stocks:
        for current_prod in StockProduct.objects.all().reverse():
            if StockProduct.objects.filter(product=current_prod.product, stock=stock).count() > 1:
                current_prod.delete()

    return HttpResponse("Duplicate Deleted")


def add_stock(request):
    if request.method == 'GET':
        stockform = StockForm()
    elif request.method == 'POST':
        stockform = StockForm(request.POST)
        if stockform.is_valid():
            stockform.save()
            return redirect('stock:stock_list')
    context = {'stockform': stockform}
    return render(request, 'stock/add_stock.html', context)


def stock_list(request):
    stocks = Stock.objects.all()
    context = {
        'stocks': stocks,
    }
    return render(request, 'stock/list_stock.html', context)


def all_stock_list(request):
    stocks = Stock.objects.all()
    context = {
        'stocks': stocks,
    }
    return render(request, 'stock/list_stock.html', context)


def update_stock(request, pk):
    stock = Stock.objects.get(id=pk)
    stockform = StockForm(instance=stock)
    if request.method == 'POST':
        stockform = StockForm(request.POST, instance=stock)
        if stockform.is_valid():
            stockform.save()
            return redirect('stock:stock_list')
    context = {'stockform': stockform}
    return render(request, 'stock/add_stock.html', context)


def delete_stock(request, pk):
    stock = Stock.objects.get(id=pk)
    context = {'stock': stock}
    if request.method == 'POST':
        stock.delete()
        return redirect('stock:stock_list')
    return render(request, 'stock/delete.html', context)


def reset_stock(request, pk):
    stock = Stock.objects.get(id=pk)
    stockproducts = StockProduct.objects.all().filter(stock=stock)
    if request.method == 'POST':
        for stockproduct in stockproducts:
            stockproduct.quantity = 0
            stockproduct.save()
        return redirect('stock:stock_list')
    context = {
        'stock': stock
    }
    return render(request, 'stock/reset.html', context)


def add_stockproduct(request):
    # check if product exist in stock already
    if request.method == 'GET':
        stockproductform = StockProductForm()
    elif request.method == 'POST':
        stockproductform = StockProductForm(request.POST)
        if stockproductform.is_valid():
            stockproduct = stockproductform.save(commit=False)
            items = StockProduct.objects.all().filter(stock=request.POST['stock'])

            itemexist = 1
            if len(items) > 0:
                for item in items:
                    if item.product.id == stockproduct.product.id:
                        item.quantity += stockproduct.quantity
                        item.save()
                        itemexist = 2
                        print("ALL FINE HERE 1")
                if itemexist == 1:
                    stockproduct.save()
                    itemexist = 0
                    print("ALL FINE HERE 2")
            else:
                itemexist = 0
                if itemexist == 0:
                    stockproduct.save()
                    print("ALL FINE HERE 3")

            return redirect('stock:stock_list')
    context = {'stockproductform': stockproductform}
    return render(request, 'stockproduct/add_stockproduct.html', context)


def stockproduct_list(request, pk):
    stock = Stock.objects.get(id=pk)
    stockproducts = StockProduct.objects.all().filter(stock=stock)

    context = {
        'stockproducts': stockproducts,
    }
    return render(request, 'stockproduct/all_list_stockproduct.html', context)


def all_stockproduct_list(request):
    stockproducts = StockProduct.objects.only("product", "quantity", "stock")
    categories = Category.objects.all()
    print("======>", stockproducts[1].product)

    context = {
        'categories': categories,
        'stockproducts': stockproducts,
    }
    return render(request, 'stockproduct/all_list_stockproduct.html', context)


# Modal Add Stock Product To Buy Order
def modal_buyorder_stockproduct_list(request, pk):
    order = BuyOrder.objects.get(id=pk)
    stockproducts = Product.objects.all()
    if request.method == 'POST':
        # get submitted orders
        chosenproducts = request.POST.getlist("products")
        if len(chosenproducts) != 0:
            for product in chosenproducts:
                product = ''.join(product.split())
                currentproduct = Product.objects.get(id=product)
                # print(currentproduct)
                BuyOrderItem.objects.create(
                    order=order,
                    product=currentproduct,
                    price=currentproduct.buyprice,
                    # weight=currentproduct.product.weight,
                    quantity=1,
                )
        if order.confirmed:
            return redirect('buyorder:update_order', order.pk)
        else:
            return redirect('buyorder:buyorder_confirmation', order.pk)
    context = {
        'stockproducts': stockproducts,
    }
    return render(request, 'stockproduct/modal_buyorder_list_stockproduct.html', context)


# Modal Add Stock Product To Sell Order
def modal_order_stockproduct_list(request, pk):
    sellorder = Order.objects.get(id=pk)
    stockproducts = StockProduct.objects.all()
    if request.method == 'POST':
        # get submitted orders
        chosenproducts = request.POST.getlist("products")
        if len(chosenproducts) != 0:
            for product in chosenproducts:
                product = ''.join(product.split())
                currentproduct = StockProduct.objects.get(id=product)
                # print(currentproduct)
                OrderItem.objects.create(
                    order=sellorder,
                    stockproduct=currentproduct,
                    price=currentproduct.product.sellprice,
                    # weight=currentproduct.product.weight,
                    quantity=1,
                )
        if sellorder.confirmed:
            return redirect(f'../../sellorder/confirm_order/{sellorder.pk}')
        else:
            return redirect('sellorder:update_order_performa', sellorder.id)

    context = {
        'stockproducts': stockproducts,
    }
    return render(request, 'stockproduct/modal_order_list_stockproduct.html', context)


# Modal Add Stock Product To Sell Order update
def modal_update_order_stockproduct_list(request, pk):
    sellorder = Order.objects.get(id=pk)
    stockproducts = StockProduct.objects.all()
    if request.method == 'POST':
        # get submitted orders
        chosenproducts = request.POST.getlist("products")
        if len(chosenproducts) != 0:
            for product in chosenproducts:
                product = ''.join(product.split())
                currentproduct = StockProduct.objects.get(id=product)
                # print(currentproduct)
                OrderItem.objects.create(
                    order=sellorder,
                    stockproduct=currentproduct,
                    price=currentproduct.product.sellprice,
                    # weight=currentproduct.product.weight,
                    quantity=0,
                )
        if sellorder.confirmed:
            return redirect('sellorder:update_order', sellorder.id)
        else:
            return redirect('sellorder:update_order_performa', sellorder.id)
    context = {
        'stockproducts': stockproducts,
    }
    return render(request, 'stockproduct/modal_order_list_stockproduct.html', context)


# Normal sell order
def order_stockproduct_list(request):
    stockproducts = StockProduct.objects.all().filter(quantity__gt=0)
    customers = Customer.objects.all()
    pannes = Panne.objects.all()
    services = Service.objects.all()
    # providers = ServiceProvider.objects.all()
    if request.method == 'POST':
        # get submitted orders
        chosenproducts = request.POST.getlist("products")
        chosencustomer = request.POST.getlist("customers")
        # chosenvehicule = request.POST.getlist("vehicle")
        chosenpannes = request.POST.getlist("pannes")
        chosenservices = request.POST.getlist("services")
        # print(chosencustomer)
        # print(chosenvehicule)
        if len(chosencustomer) != 0:
            sellorder = Order()
            chosencustomer[0] = ''.join(chosencustomer[0].split())
            customer = Customer.objects.get(id=chosencustomer[0])

            sellorder.customer = customer
            sellorder.save()
            print(chosenproducts)
            # add products
            if len(chosenproducts) != 0:
                for product in chosenproducts:
                    product = ''.join(product.split())
                    print("Product ID ###########>", product)
                    product = ''.join(product.split())
                    currentproduct = StockProduct.objects.get(id=product)
                    # print(currentproduct)
                    OrderItem.objects.create(
                        order=sellorder,
                        stockproduct=currentproduct,
                        price=currentproduct.product.sellprice,
                        # weight=currentproduct.product.weight,
                        quantity=1,
                    )
            # add pannes
            if len(chosenpannes) != 0:
                for panne in chosenpannes:
                    panne = ''.join(panne.split())
                    currentpanne = Panne.objects.get(id=panne)
                    # print(currentpanne)
                    PanneItem.objects.create(
                        order=sellorder,
                        panne=currentpanne,
                        price=currentpanne.price
                    )
            # add services
            if len(chosenservices) != 0:
                for service in chosenservices:
                    service = ''.join(service.split())
                    currentservice = Service.objects.get(id=service)
                    ServiceItem.objects.create(
                        order=sellorder,
                        service=currentservice,
                        price=currentservice.price,
                        charge=currentservice.charge,
                    )

            return redirect('stock:order_vehicle', sellorder.pk)

    context = {
        'customers': customers,
        'stockproducts': stockproducts,
        'pannes': pannes,
        "services": services,
    }
    return render(request, 'stockproduct/order_list_stockproduct.html', context)


# Performa order
def performa_order_stockproduct_list(request):
    stockproducts = StockProduct.objects.all()
    customers = Customer.objects.all()
    pannes = Panne.objects.all()
    services = Service.objects.all()

    if request.method == 'POST':
        # get submitted orders
        chosenproducts = request.POST.getlist("products")
        chosencustomer = request.POST.getlist("customers")
        # chosenvehicule = request.POST.getlist("vehicle")
        chosenpannes = request.POST.getlist("pannes")
        chosenservices = request.POST.getlist("services")

        # print(chosencustomer)
        # print(chosenvehicule)
        if len(chosencustomer) != 0:
            sellorder = Order()
            chosen_customer = chosencustomer[0]
            chosen_customer = ''.join(chosen_customer.split())
            customer = Customer.objects.get(id=chosen_customer)
            # print(customer)
            # vehicles = Vehicle.objects.all().filter(customer=customer)
            # print(vehicles)
            #
            # vehicle = Vehicle.objects.get(id=chosenvehicule[int(chosencustomer[0]) - 1])
            # print(vehicle)

            sellorder.customer = customer
            # sellorder.vehicle = vehicle
            sellorder.save()
            print(chosenproducts)
            # add products
            if len(chosenproducts) != 0:
                for product in chosenproducts:
                    product = ''.join(product.split())
                    currentproduct = StockProduct.objects.get(id=product)
                    # print(currentproduct)
                    OrderItem.objects.create(
                        order=sellorder,
                        stockproduct=currentproduct,
                        price=currentproduct.product.sellprice,
                        # weight=currentproduct.product.weight,
                        quantity=1,
                    )
            # add Pannes
            if len(chosenpannes) != 0:
                for panne in chosenpannes:
                    currentpanne = Panne.objects.get(id=panne)
                    # print(currentpanne)
                    PanneItem.objects.create(
                        order=sellorder,
                        panne=currentpanne,
                        price=currentpanne.price
                    )
            # add services
            if len(chosenservices) != 0:
                for service in chosenservices:
                    currentservice = Service.objects.get(id=service)
                    ServiceItem.objects.create(
                        order=sellorder,
                        service=currentservice,
                        price=currentservice.price + currentservice.charge
                    )
            return redirect('stock:performa_order_vehicle', sellorder.pk)

    context = {
        'customers': customers,
        'stockproducts': stockproducts,
        'pannes': pannes,
        'services': services,
    }
    return render(request, 'stockproduct/order_list_stockproduct.html', context)


# Real Order
def order_vehicle(request, pk):
    sellorder = Order.objects.get(id=pk)
    customer = Customer.objects.get(id=sellorder.customer.pk)
    vehicles = Vehicle.objects.all().filter(customer=customer)
    if request.method == 'POST':
        chosenvehicule = request.POST.get("vehicle")
        # Remove white spaces
        chosenvehicule = ''.join(chosenvehicule.split())
        if chosenvehicule:
            # print(chosenvehicule)
            vehicle = Vehicle.objects.get(id=chosenvehicule)
            # print(vehicle)
            sellorder.vehicle = vehicle
            sellorder.save()
            return redirect(f'../../sellorder/confirm_order/{sellorder.pk}')

    context = {
        'vehicles': vehicles,
    }
    return render(request, 'stockproduct/order_vehicle.html', context)


# PerformaS Order
def performa_order_vehicle(request, pk):
    sellorder = Order.objects.get(id=pk)
    customer = Customer.objects.get(id=sellorder.customer.pk)
    vehicles = Vehicle.objects.all().filter(customer=customer)
    if request.method == 'POST':
        chosenvehicule = request.POST.get("vehicle")
        if chosenvehicule:
            # print(chosenvehicule)
            # Remove white spaces
            chosenvehicule = ''.join(chosenvehicule.split())
            vehicle = Vehicle.objects.get(id=chosenvehicule)
            # print(vehicle)
            sellorder.vehicle = vehicle
            sellorder.save()
            return redirect('sellorder:confirm_order_performa', sellorder.pk)

    context = {
        'vehicles': vehicles,
    }
    return render(request, 'stockproduct/order_vehicle.html', context)


def stockproduct_detail(request, id):
    stockproduct = get_object_or_404(StockProduct, id=id)

    context = {
        'stockproduct': stockproduct,

    }
    return render(request, 'stockproduct/detail.html', context)


def stockproductcategory_list(request, pk):
    categories = Category.objects.all()
    category = Category.objects.get(id=pk)
    stockproducts = StockProduct.objects.all().filter(category=category)
    customer = Customer.objects.get(user=request.user)
    customertype = customer.customer_type
    context = {
        'category': category,
        'categories': categories,
        'stockproducts': stockproducts,
        'customertype': customertype,
        'customer': customer,
    }
    return render(request, 'stockproduct/list_stockproduct.html', context)


def stockproduct_quantityalert(request):
    products = Product.objects.all()
    for product in products:
        stockproductsalert = StockProduct.objects.all().filter(quantity__lte=product.alert_quantity)
    context = {
        'stockproductsalert': stockproductsalert,
    }

    return render(request, 'stockproduct/stock_alert_list.html', context)


def update_stockproduct(request, pk):
    stockproduct = StockProduct.objects.get(id=pk)
    stockproductform = StockProductForm(instance=stockproduct)
    if request.method == 'POST':
        stockproductform = StockProductForm(request.POST, instance=stockproduct)
        if stockproductform.is_valid():
            stockproductform.save()
            return redirect('stock:stock_list')
    context = {'stockproductform': stockproductform}
    return render(request, 'stockproduct/add_stockproduct.html', context)


def delete_stockproduct(request, pk):
    stockproduct = StockProduct.objects.get(id=pk)
    context = {'stockproduct': stockproduct}
    if request.method == 'POST':
        stockproduct.delete()
        return redirect('stock:stock_list')
    return render(request, 'stockproduct/delete.html', context)


def calculate_general_stock(request):
    in_products = StockProduct.objects.all().filter(quantity__gt=0)
    in_price = 0
    out_price = 0
    benefits = 0
    for product in in_products:
        in_price += product.product.buyprice
        out_price += product.product.sellprice
    benefits = out_price - in_price

    context = {
        'in_price': in_price,
        'out_price': out_price,
        'benefits': benefits,
    }

    return render(request, 'stock/state.html', context)


def calculate_one_stock(request, pk):
    stock = Stock.objects.get(id=pk)
    in_products = StockProduct.objects.all().filter(quantity__gt=0, stock=stock)
    in_price = 0
    out_price = 0
    benefits = 0
    for product in in_products:
        in_price += product.product.buyprice
        out_price += product.product.sellprice
    benefits = out_price - in_price

    context = {
        'in_price': in_price,
        'out_price': out_price,
        'benefits': benefits,
    }

    return render(request, 'stock/state.html', context)


# sell & buy details
def stock_product_details(request, pk):
    # current year
    current_year = CurrentYear.objects.all().filter()[:1].get()
    # date
    dateform = DateForm()

    stockproduct = get_object_or_404(StockProduct, id=pk)
    # chosen orders
    chosen_orders = Order.objects.none()
    chosen_buyorders = BuyOrder.objects.none()
    # quantities
    sell_quantities = []
    buy_quantities = []

    sell_quantity = 0
    buy_quantity = 0
    # product
    sell_pieces = OrderItem.objects.none()
    buy_pieces = OrderItem.objects.none()
    # order items
    # print(stockproduct.order_item.all())
    order_items = stockproduct.order_item.all(order__order_date__year=current_year.year,
                                              order__confirmed=True)
    for item in order_items:
        chosen_orders |= Order.objects.all().filter(id=item.order.id, created__year=current_year.year)
        sell_quantity += item.quantity
        sell_quantities.append(item.quantity)
        sell_pieces |= order_items.filter(id=item.id)

    # buy product
    product = get_object_or_404(Product, id=stockproduct.product.id)

    # print(product.buyorder_item.all())
    order_items = product.buyorder_item.all()
    for item in order_items:
        chosen_buyorders |= BuyOrder.objects.all().filter(id=item.order.id, created__year=current_year.year)
        buy_pieces |= order_items.filter(id=item.id)
        buy_quantity += item.quantity
        buy_quantities.append(item.quantity)

    # Time search
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

        for item in order_items:
            chosen_orders |= Order.objects.all().filter(
                Q(
                    order_date__gt=date(int(start_year), int(start_month),
                                        int(start_day)),
                    order_date__lt=date(int(end_year), int(end_month), int(end_day))
                )
                |
                Q(
                    order_date=date(int(end_year), int(end_month), int(end_day))
                )
                |
                Q(
                    order_date__year=None
                )
                ,
                id=item.order.id,
                confirmed=True,
            )
            sell_quantity += item.quantity
            sell_quantities.append(item.quantity)
            sell_pieces |= OrderItem.objects.filter(id=item.id)

        # buy product
        product = get_object_or_404(Product, id=stockproduct.product.id)

        # print(product.buyorder_item.all())
        order_items = product.buyorder_item.all()
        for item in order_items:
            chosen_buyorders |= BuyOrder.objects.all().filter(
                Q(
                    order_date__gt=date(int(start_year), int(start_month),
                                        int(start_day)),
                    order_date__lt=date(int(end_year), int(end_month), int(end_day))
                )
                |
                Q(
                    order_date=date(int(end_year), int(end_month), int(end_day))
                )
                |
                Q(
                    order_date__year=None
                )
                ,
                id=item.order.id,

            )
            buy_pieces |= order_items.filter(id=item.id)
            buy_quantity += item.quantity
            buy_quantities.append(item.quantity)

    sell_list = zip(chosen_orders, sell_pieces, sell_quantities)
    final_buylist = zip(chosen_buyorders, buy_pieces, buy_quantities)

    context = {

        'current_year': current_year,
        # sell vars
        'stockproduct': stockproduct,
        'sell_list': sell_list,
        'sell_pieces': sell_pieces,
        'chosen_orders': chosen_orders,
        'sell_quantity': sell_quantity,
        # buy vars
        'product': product,
        'final_buylist': final_buylist,
        'buy_pieces': buy_pieces,
        'buy_quantity': buy_quantity,
        # time
        'dateform': dateform,
    }

    return render(request, 'stockproduct/product_details.html', context)
