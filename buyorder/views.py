import decimal
from datetime import date, datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.views.decorators.cache import cache_page
from django.core.cache import cache

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
# Create your views here.
from billing.models import BuyOrderBilling, BillBuyOrderItem
from buyorder.forms import BuyOrderForm, BuyOrderItemFormset
from buyorder.models import BuyOrderItem, BuyOrder
from caisse.models import Caisse
from payments.models import BuyOrderPayment
from product.forms import ProductForm
from product.models import Product
from supplier.models import Supplier
from stock.models import StockProduct, Stock

Buyorder_KEY = "buyorder.all"


def create_buyorder(request):
    buyorderform = BuyOrderForm()
    buyorderitemformset = BuyOrderItemFormset(queryset=BuyOrderItem.objects.none())
    productform = ProductForm()
    products = Product.objects.all()

    if request.method == 'POST':
        print(request.POST)
        # fix the form to be validated
        # get the list of the chosen products
        products_list = request.POST.getlist('products')
        # print(products_list)
        buyorderform = BuyOrderForm(request.POST)
        # if the list has elements

        if buyorderform.is_valid():
            if len(products_list):
                print(products_list)
                buyorder = buyorderform.save()
                # to add credit
                # supplier = Supplier.objects.get(id=request.POST['supplier'])
                buyorder.user = request.user.id
                for prod_list_item in products_list:
                    # saving the order items
                    orderitem = BuyOrderItem()
                    orderitem.order = buyorder
                    print("PRODUCT ID ====================>", prod_list_item)
                    prod_list_item = ''.join(prod_list_item.split())
                    orderitem.product = Product.objects.get(id=prod_list_item)
                    orderitem.price = Product.objects.get(id=prod_list_item).buyprice
                    orderitem.save()
                    # print(Product.objects.get(id=prod_list_item))
            cache.delete(Buyorder_KEY)
            return redirect(f'../buyorder/buyorder_confirmation/{buyorder.pk}')
    context = {
        'products': products,
        'buyorderform': buyorderform,
        'buyorderitemformset': buyorderitemformset,
        'productform': productform,
    }
    return render(request, 'buyorder/add_buyorder.html', context)


def confirm_all(request):
    buyorders = BuyOrder.objects.all()
    for order in buyorders:
        order.total_price = order.get_total_cost()
        order.confirmed = True
        order.save()
        cache.delete(Buyorder_KEY)
    context = {
        'buyorders': buyorders,
    }
    return render(request, 'buyorder/list_buyorder.html', context)


def buyorder_confirmation(request, pk):
    buyorder = BuyOrder.objects.get(id=pk)
    stocks = Stock.objects.all()
    buyorderform = BuyOrderForm(instance=buyorder)

    if request.method == 'POST':
        buyorderform = BuyOrderForm(request.POST, instance=buyorder)
        if buyorderform.is_valid():
            print(request.POST)
            buyorder = buyorderform.save()
            # to add credit
            supplier = Supplier.objects.get(id=request.POST['supplier'])
            # get modified items
            prices = request.POST.getlist('prices')
            quantities = request.POST.getlist('quantities')
            # Stock list
            stocklist = request.POST.getlist('stock')
            tva = request.POST.get('tva')
            chosen_date = request.POST.get('order_date')
            # get year month day
            chosen_year = chosen_date.split("-", 1)
            chosen_month = chosen_date.split("-", 2)
            chosen_day = chosen_date.split("-", 2)
            for index, item in enumerate(buyorder.items.all()):
                # print(index, item)
                print(prices[index], quantities[index])
                # get the price and value of each element
                # Saving the orderitem
                # print("----------------------------------------------")
                # print(prices[index])
                str_price = prices[index]
                str_price = str_price.replace(",", ".")
                # str_price = str_price.replace(' ', '')
                # Remove white spaces
                str_price = ''.join(str_price.split())
                # assign price
                item.price = str_price
                # print("----------------------------------------------")
                # treating the quantity
                str_quantity = quantities[index]
                str_quantity = str_quantity.replace(",", ".")
                # Remove white spaces
                str_quantity = ''.join(str_quantity.split())
                # assign quantity
                item.quantity = str_quantity

                # get stock
                item.stock = Stock.objects.get(id=stocklist[index])

                item.save()
                # adding the bought products to stock
                stockitems = StockProduct.objects.all().filter(stock=item.stock)
                itemexist = 1
                # check if stock doesn't have the product
                if len(stockitems) > 0:
                    # stock has products check if product exist
                    for stockitem in stockitems:
                        # the same product exist
                        if stockitem.product.id == item.product.id:
                            stockitem.quantity += decimal.Decimal(item.quantity)
                            stockitem.save()
                            itemexist = 2
                            # operation done same product plus the new quantity

                    if itemexist == 1:
                        #             # stock not empty product doesn't exist in it
                        #             # create new stockproduct
                        StockProduct.objects.create(
                            product=item.product,
                            quantity=decimal.Decimal(item.quantity),
                            # category=item.product.category,
                            stock=item.stock
                        )
                else:
                    #         # stock is empty
                    itemexist = 0
                    if itemexist == 0:
                        # create new stockproduct
                        StockProduct.objects.create(
                            product=item.product,
                            quantity=decimal.Decimal(item.quantity),
                            # type=item.type,
                            # color=item.color,
                            # category=item.product.category,
                            stock=item.stock
                        )
            # print(buyorder.get_total_cost())
            # print(supplier)
            buyorder.order_tva = int(tva)
            buyorder.debt = buyorder.get_ttc()
            supplier.credit += buyorder.get_ttc()
            supplier.save()
            buyorder.total_price = buyorder.get_total_cost()
            buyorder.order_date = date(int(chosen_year[0]), int(chosen_month[1]), int(chosen_day[2]))
            buyorder.confirmed = True
            buyorder.save()
            cache.delete(Buyorder_KEY)
            return redirect('buyorder:buyorder_list')

    context = {
        'buyorderform': buyorderform,
        'buyorder': buyorder,
        'stocks': stocks,
    }
    return render(request, 'buyorder/buyorder_confirmation.html', context)


def update_order(request, pk):
    buyorder = BuyOrder.objects.get(id=pk)

    stocks = Stock.objects.all()

    buyorderform = BuyOrderForm(instance=buyorder)
    old_ttc = round(buyorder.total_price + (buyorder.total_price * decimal.Decimal(buyorder.order_tva / 100)), 2)
    new_ttc = 0
    ttc_difference = 0
    if request.method == 'POST':
        buyorderform = BuyOrderForm(request.POST, instance=buyorder)
        if buyorderform.is_valid():
            # Reset Stock Quantity to update the quantities
            if buyorder.items.all():
                for item in buyorder.items.all():
                    if StockProduct.objects.all().filter(product=item.product):
                        print("############# OKAY Update minus")
                        stockitem = StockProduct.objects.get(product=item.product)
                        # if stockitem.quantity - int(item.quantity) >= 0:
                        stockitem.quantity -= decimal.Decimal(item.quantity)
                        stockitem.save()
            print(request.POST)
            buyorder = buyorderform.save()

            # to add credit
            supplier = Supplier.objects.get(id=request.POST['supplier'])
            # get modified items
            prices = request.POST.getlist('prices')
            quantities = request.POST.getlist('quantities')
            # Stock list
            stocklist = request.POST.getlist('stock')
            tva = request.POST.get('tva')
            chosen_date = request.POST.get('order_date')
            # get year month day
            chosen_year = chosen_date.split("-", 1)
            chosen_month = chosen_date.split("-", 2)
            chosen_day = chosen_date.split("-", 2)
            for index, item in enumerate(buyorder.items.all()):
                # print(index, item)
                print(prices[index], quantities[index])
                # get the price and value of each element
                # Saving the orderitem
                str_price = prices[index]
                str_price = str_price.replace(",", ".")
                # str_price = str_price.replace(' ', '')
                # Remove white spaces
                str_price = ''.join(str_price.split())
                # print("----------------------------------------------")
                item.price = str_price
                item.quantity = quantities[index]

                # get stock
                item.stock = Stock.objects.get(id=stocklist[index])

                item.save()
                # adding the bought products to stock
                stockitems = StockProduct.objects.all().filter(stock=item.stock)
                itemexist = 1
                # check if stock doesn't have the product
                if len(stockitems) > 0:
                    # stock has products check if product exist
                    for stockitem in stockitems:
                        # the same product exist
                        if stockitem.product.id == item.product.id:
                            stockitem.quantity += decimal.Decimal(item.quantity)
                            stockitem.save()
                            itemexist = 2
                            # operation done same product plus the new quantity

                    if itemexist == 1:
                        #             # stock not empty product doesn't exist in it
                        #             # create new stockproduct
                        StockProduct.objects.create(
                            product=item.product,
                            quantity=decimal.Decimal(item.quantity),
                            # category=item.product.category,
                            stock=item.stock
                        )
                else:
                    #         # stock is empty
                    itemexist = 0
                    if itemexist == 0:
                        # create new stockproduct
                        StockProduct.objects.create(
                            product=item.product,
                            quantity=decimal.Decimal(item.quantity),
                            # type=item.type,
                            # color=item.color,
                            # category=item.product.category,
                            stock=item.stock
                        )
            # print(buyorder.get_total_cost())
            # print(supplier)
            buyorder.order_tva = int(tva)
            # get money additiion
            print(old_ttc)
            new_ttc = buyorder.get_ttc()
            print(new_ttc)
            ttc_difference = new_ttc - old_ttc
            print(ttc_difference)
            buyorder.debt += ttc_difference
            supplier.credit += ttc_difference
            supplier.save()
            buyorder.order_date = date(int(chosen_year[0]), int(chosen_month[1]), int(chosen_day[2]))
            buyorder.confirmed = True
            buyorder.total_price = buyorder.get_total_cost()
            buyorder.save()
            cache.delete(Buyorder_KEY)
            return redirect('buyorder:buyorder_list')
    context = {
        'buyorderform': buyorderform,
        'buyorder': buyorder,
    }
    return render(request, 'buyorder/buyorder_confirmation.html', context)


def buyorder_details(request, pk):
    order = BuyOrder.objects.get(id=pk)
    context = {
        'order': order
    }
    return render(request, 'buyorder/buyorder_details.html', context)


def buyorder_list(request):
    # now time
    now = datetime.now()
    suppliers = Supplier.objects.all()
    buyorders = BuyOrder.objects.filter(created__day=now.day, created__month=now.month)

    if request.method == 'POST':
        alldata = request.POST
        chosensupplier = request.POST.getlist("suppliers")
        if len(chosensupplier) != 0:
            supplier = Supplier.objects.get(id=chosensupplier[0])
            buyorders = BuyOrder.objects.filter(supplier=supplier)

    context = {
        'buyorders': buyorders,
        'suppliers': suppliers
    }
    return render(request, 'buyorder/list_buyorder.html', context)


def buyorderorder_list_by_supplier(request, pk):
    supplier = Supplier.objects.get(id=pk)
    buyorders = BuyOrder.objects.all().filter(supplier=supplier, factured=False)

    if request.method == 'POST':
        # get submitted orders
        chosenorders = request.POST.getlist("orders")
        # create billing object if there is selected orders
        if len(chosenorders) != 0:
            # print(chosenorders)
            # buyorderbill object
            buyorderbilling = BuyOrderBilling()
            buyorderbilling.supplier = supplier
            # TODO : Uncomment this line
            # buyorderbilling.user = request.user.id
            buyorderbilling.save()
            for orderid in chosenorders:
                # each order is a billing item
                currentorder = BuyOrder.objects.get(id=orderid)
                currentorder.factured = True
                currentorder.save()
                orderprice = currentorder.get_total_cost()
                # adding supplier credit
                supplier.credit += orderprice
                supplier.save()
                #                orderweight = currentorder.get_total_weight()
                BillBuyOrderItem.objects.create(
                    bill=buyorderbilling,
                    order=currentorder,
                    price=orderprice,
                    #                   weight=orderweight,
                )
                # reduce quantity from the stock
                currentorderitems = currentorder.items.all()
                for item in currentorderitems:
                    stockitems = StockProduct.objects.all().filter(stock=item.product.stock)
                    itemexist = 1
                    # check if stock doesn't have the product
                    if len(stockitems) > 0:
                        # stock has products check if product exist
                        for stockitem in stockitems:
                            # the same product exist
                            if stockitem.product.id == item.product.id:
                                stockitem.quantity += decimal.Decimal(item.quantity)
                                stockitem.save()
                                itemexist = 2
                                #                 # operation done same product plus the new quantity

                        if itemexist == 1:
                            #             # stock not empty product doesn't exist in it
                            #             # create new stockproduct
                            StockProduct.objects.create(
                                product=item.product,
                                quantity=decimal.Decimal(item.quantity),
                                # category=item.product.category,
                                stock=item.product.stock
                            )
                    else:
                        #         # stock is empty
                        itemexist = 0
                        if itemexist == 0:
                            # create new stockproduct
                            StockProduct.objects.create(
                                product=item.product,
                                quantity=decimal.Decimal(item.quantity),
                                # category=item.product.category,
                                stock=item.product.stock
                            )
            # send bill to be printed
            pk = buyorderbilling.pk
            return redirect(f'../../buyor/buyorder_pdf/{pk}')

    context = {
        'buyorders': buyorders
    }
    return render(request, 'buyorder/billing_list_buyorder.html', context)


def buyorder_pdf(request, pk):
    buyorder = get_object_or_404(BuyOrder, id=pk)
    html = render_to_string('buyorder/pdf.html', {'order': buyorder})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{buyorder.id}.pdf'

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def buyorder_delete(request, pk):
    order = get_object_or_404(BuyOrder, id=pk)
    if request.method == 'POST':
        if order.confirmed:
            if order.items.all():
                for item in order.items.all():
                    stockitem = StockProduct.objects.get(product__id=item.product.id)
                    print(stockitem)
                    print(stockitem.quantity)
                    print(item.quantity)
                    # if stockitem.quantity > 0:
                    stockitem.quantity -= decimal.Decimal(item.quantity)
                    stockitem.save()
                    print("After subtraction")
                    print(stockitem.quantity)
        supplier = Supplier.objects.get(id=order.supplier.id)
        supplier.credit -= order.debt
        supplier.save()
        if BuyOrderPayment.objects.all().filter(order=order):
            supplierpayment = BuyOrderPayment.objects.get(order=order)
            caisse = Caisse.objects.all().filter()[:1].get()
            caisse.caisse_value += supplierpayment.amount
            caisse.save()
            supplierpayment.delete()
        order.delete()
        cache.delete(Buyorder_KEY)
        return redirect('buyorder:buyorder_list')
    context = {
        'order': order
    }
    return render(request, 'buyorder/buyorder_delete.html', context)


# Confirm Order Delete item or Update
def confirm_order_item_delete(request, orderpk, itempk):
    buyorder = BuyOrder.objects.get(id=orderpk)
    item = buyorder.items.get(id=itempk)
    if request.method == 'POST':
        if buyorder.confirmed:
            item = buyorder.items.get(id=itempk)
            stockproduct = StockProduct.objects.get(product=item.product)
            # print("StockProduct =====> ", stockproduct)
            stockproduct.quantity -= item.quantity
            stockproduct.save()
            item.delete()
        else:
            item = buyorder.items.get(id=itempk)
            item.delete()
        buyorder.save()
        return redirect('buyorder:buyorder_confirmation', buyorder.id)

    context = {
        'buyorder': buyorder,
        'item': item,
    }
    return render(request, 'buyorder/delete_item.html', context)
