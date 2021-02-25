from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from category.models import Category
from customer.models import Customer
from product.models import Product
from rdv.models import Panne
from sellorder.models import Order, OrderItem, PanneItem
from stock.forms import StockForm, StockProductForm
from stock.models import Stock, StockProduct
from vehicule.models import Vehicle


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
    return render(request, 'stockproduct/list_stockproduct.html', context)


def all_stockproduct_list(request):
    stockproducts = StockProduct.objects.all().filter(quantity__gt=0)
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'stockproducts': stockproducts,
    }
    return render(request, 'stockproduct/all_list_stockproduct.html', context)


# Modal Add Stock Product To Sell Order
def modal_order_stockproduct_list(request, pk):
    sellorder = Order.objects.get(id=pk)
    stockproducts = StockProduct.objects.all()
    if request.method == 'POST':
        # get submitted orders
        chosenproducts = request.POST.getlist("products")
        if len(chosenproducts) != 0:
            for product in chosenproducts:
                currentproduct = StockProduct.objects.get(id=product)
                # print(currentproduct)
                OrderItem.objects.create(
                    order=sellorder,
                    stockproduct=currentproduct,
                    price=currentproduct.product.sellprice,
                    # weight=currentproduct.product.weight,
                    quantity=1,
                )
        return redirect(f'../../sellorder/confirm_order/{sellorder.pk}')
    context = {
        'stockproducts': stockproducts,
    }
    return render(request, 'stockproduct/modal_order_list_stockproduct.html', context)


# Normal
def order_stockproduct_list(request):
    stockproducts = StockProduct.objects.all().filter(quantity__gt=0)
    customers = Customer.objects.all()
    pannes = Panne.objects.all()

    if request.method == 'POST':
        # get submitted orders
        chosenproducts = request.POST.getlist("products")
        chosencustomer = request.POST.getlist("customers")
        # chosenvehicule = request.POST.getlist("vehicle")
        chosenpannes = request.POST.getlist("pannes")
        # print(chosencustomer)
        # print(chosenvehicule)
        if len(chosencustomer) != 0:
            sellorder = Order()
            customer = Customer.objects.get(id=chosencustomer[0])
            # print(customer)
            # vehicles = Vehicle.objects.all().filter(customer=customer)
            # print(vehicles)
            #
            # vehicle = Vehicle.objects.get(id=chosenvehicule[int(chosencustomer[0]) - 1])
            # print(vehicle)

            sellorder.customer = customer
            # sellorder.vehicle = vehicle
            sellorder.save()
            if len(chosenproducts) != 0:
                for product in chosenproducts:
                    currentproduct = StockProduct.objects.get(id=product)
                    # print(currentproduct)
                    OrderItem.objects.create(
                        order=sellorder,
                        stockproduct=currentproduct,
                        price=currentproduct.product.sellprice,
                        # weight=currentproduct.product.weight,
                        quantity=1,
                    )
            if len(chosenpannes) != 0:
                for panne in chosenpannes:
                    currentpanne = Panne.objects.get(id=panne)
                    # print(currentpanne)
                    PanneItem.objects.create(
                        order=sellorder,
                        panne=currentpanne,
                        price=currentpanne.price
                    )
            return redirect('stock:order_vehicle', sellorder.pk)

    context = {
        'customers': customers,
        'stockproducts': stockproducts,
        'pannes': pannes,
    }
    return render(request, 'stockproduct/order_list_stockproduct.html', context)


def order_vehicle(request, pk):
    sellorder = Order.objects.get(id=pk)
    customer = Customer.objects.get(id=sellorder.customer.pk)
    vehicles = Vehicle.objects.all().filter(customer=customer)
    if request.method == 'POST':
        chosenvehicule = request.POST.get("vehicle")
        if chosenvehicule:
            print(chosenvehicule)
            vehicle = Vehicle.objects.get(id=chosenvehicule)
            print(vehicle)
            sellorder.vehicle = vehicle
            sellorder.save()
            return redirect(f'../../sellorder/confirm_order/{sellorder.pk}')

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
