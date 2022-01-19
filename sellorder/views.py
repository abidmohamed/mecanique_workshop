import decimal
from datetime import date, datetime

from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from xhtml2pdf import pisa
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.views.decorators.cache import cache_page

# Create your views here.
from billing.models import OrderBilling, BillOrderItem
from caisse.forms import DateForm, PeriodForm
from caisse.models import Caisse
from customer.models import Customer, Enterprise
from discount.forms import DiscountForm
from discount.models import Discount
from payments.forms import CustomerPaymentForm
from payments.models import SellOrderPayment
from rdv.models import Panne
from sellorder.apps import SellorderConfig
from sellorder.models import Order, SellOrderFacture, OrderItem, PanneItem
from services.models import ServiceProvider, Service
from stock.models import StockProduct
from num2words import num2words


# confirmation get order object from the stock view Of a Real Order
def confirm_order(request, pk):
    stockproducts = StockProduct.objects.all()
    sellorder = Order.objects.get(id=pk)
    discount = Discount()
    # get customer to add debt
    customer = Customer.objects.get(id=sellorder.customer.pk)
    # Get Discount
    discountform = DiscountForm()
    # print(sellorder.vehicle)
    if request.method == 'POST':

        # product prices
        prices = request.POST.getlist('prices')
        quantities = request.POST.getlist('quantities')
        # Panne prices
        panne_prices = request.POST.getlist('panne-prices')

        # Service price & charge
        service_prices = request.POST.getlist('service-prices')
        service_charges = request.POST.getlist('service-charge')

        tva = request.POST.get('tva')
        timbre = request.POST.get('timbre')
        chosen_date = request.POST.get('order_date')

        # get year month day
        chosen_year = chosen_date.split("-", 1)
        chosen_month = chosen_date.split("-", 2)
        chosen_day = chosen_date.split("-", 2)

        if sellorder.items.all():
            for index, item in enumerate(sellorder.items.all()):
                # get the price and value of each element
                # Saving the orderitem
                str_price = prices[index]
                str_price = str_price.replace(",", ".")
                # str_price = str_price.replace(' ', '')
                # Remove white spaces
                str_price = ''.join(str_price.split())
                item.price = str_price

                str_quantity = quantities[index]
                str_quantity = str_quantity.replace(",", ".")
                item.quantity = str_quantity
                print("=========>", str_quantity)

                item.save()
                # Reducing the sold products from stock
                stockitems = StockProduct.objects.all().filter(stock=item.stockproduct.stock)
                # check if stock doesn't have the product
                if len(stockitems) > 0:
                    # stock has products check if product exist
                    for stockitem in stockitems:
                        # the same product exist
                        if stockitem.id == item.stockproduct.id:
                            # if stockitem.quantity > 0 and stockitem.quantity - decimal.Decimal(item.quantity) >= 0:
                            stockitem.quantity -= decimal.Decimal(item.quantity)
                            print("=========>", stockitem.quantity)
                            stockitem.save()
                            itemexist = 2
                            #                 # operation done same product plus the new quantity
        if sellorder.pannes.all():
            for index, item in enumerate(sellorder.pannes.all()):
                # pannes
                print(panne_prices[index])
                str_panne_price = panne_prices[index]
                str_panne_price = str_panne_price.replace(",", ".")
                # Remove white spaces
                str_panne_price = ''.join(str_panne_price.split())
                item.price = str_panne_price

                item.save()

        if sellorder.services.all():
            for index, item in enumerate(sellorder.services.all()):
                # Services
                print(service_prices[index])
                print(service_charges[index])
                str_service_price = service_prices[index]
                str_service_price = str_service_price.replace(",", ".")
                # Remove white spaces
                str_service_price = ''.join(str_service_price.split())
                item.price = str_service_price
                # Add credit to provider
                service = Service.objects.get(id=item.service.id)
                service_provider = ServiceProvider.objects.get(id=service.provider.id)
                service_provider.credit += decimal.Decimal(item.price)
                # Charge
                str_service_charge = service_charges[index]
                str_service_charge = str_service_charge.replace(",", ".")
                # Remove white spaces
                str_service_charge = ''.join(str_service_charge.split())
                item.charge = str_service_charge
                # saving values
                item.save()
                service_provider.save()

        print(request.POST)
        discount.order = sellorder
        discount.value = request.POST.get('discount-value')
        discount.discount_status = request.POST.get('discount-status')
        discount.save()
        print(discount.discount_status)
        if discount.discount_status == '1':
            sellorder.discount_amount = (sellorder.get_ttc() * decimal.Decimal(decimal.Decimal(discount.value) / 100))
        else:
            sellorder.discount_amount = decimal.Decimal(discount.value)

        sellorder.total_price = sellorder.get_total_item_panne()
        sellorder.order_tva = int(tva)
        timbre = timbre.replace(",", ".")
        timbre = ''.join(timbre.split())
        sellorder.timbre = decimal.Decimal(timbre)
        sellorder.debt = sellorder.get_ttc()
        sellorder.order_date = date(int(chosen_year[0]), int(chosen_month[1]), int(chosen_day[2]))
        sellorder.confirmed = True
        sellorder.save()
        print(sellorder.confirmed)
        # customer debt
        customer.debt += sellorder.get_ttc()
        customer.save()
        return redirect('payments:create_customer_payment', sellorder.id)
    context = {
        'customer': customer,
        'sellorder': sellorder,
        'discountform': discountform,
        'stockproducts': stockproducts,
    }
    return render(request, 'sellorder/sellorder_confirmation.html', context)


# confirmation get order object from the stock view Of Perfoma Order
def confirm_order_performa(request, pk):
    stockproducts = StockProduct.objects.all()
    sellorder = Order.objects.get(id=pk)
    discount = Discount()
    # get customer to add debt
    customer = Customer.objects.get(id=sellorder.customer.pk)
    # Get Discount
    discountform = DiscountForm()
    # print(sellorder.vehicle)
    if request.method == 'POST':
        prices = request.POST.getlist('prices')
        quantities = request.POST.getlist('quantities')
        tva = request.POST.get('tva')
        timbre = request.POST.get('timbre')
        chosen_date = request.POST.get('order_date')
        # get year month day
        chosen_year = chosen_date.split("-", 1)
        chosen_month = chosen_date.split("-", 2)
        chosen_day = chosen_date.split("-", 2)
        if sellorder.items.all():
            for index, item in enumerate(sellorder.items.all()):
                # get the price and value of each element
                # Saving the orderitem
                str_price = prices[index]
                str_price = str_price.replace(",", ".")
                # str_price = str_price.replace(' ', '')
                # Remove white spaces
                str_price = ''.join(str_price.split())
                item.price = str_price
                item.quantity = quantities[index]
                item.save()

        print(request.POST)
        discount.order = sellorder
        discount.value = request.POST.get('discount-value')
        discount.discount_status = request.POST.get('discount-status')
        discount.save()
        print(discount.discount_status)
        if discount.discount_status == '1':
            sellorder.discount_amount = (sellorder.get_ttc() * decimal.Decimal(decimal.Decimal(discount.value) / 100))
        else:
            sellorder.discount_amount = decimal.Decimal(discount.value)

        sellorder.total_price = sellorder.get_total_item_panne()
        sellorder.order_tva = int(tva)
        timbre = timbre.replace(",", ".")
        timbre = ''.join(timbre.split())
        sellorder.timbre = decimal.Decimal(timbre)
        sellorder.debt = sellorder.get_ttc()
        sellorder.order_date = date(int(chosen_year[0]), int(chosen_month[1]), int(chosen_day[2]))
        sellorder.confirmed = False
        sellorder.save()
        print(sellorder.confirmed)
        # customer debt
        # customer.debt += sellorder.get_ttc()
        # customer.save()
        return redirect('sellorder:performa_sellorder_list')
    context = {
        'customer': customer,
        'sellorder': sellorder,
        'discountform': discountform,
        'stockproducts': stockproducts,
    }
    return render(request, 'sellorder/sellorder_confirmation.html', context)


# Update Performa
def update_order_performa(request, pk):
    # get Stock Products
    stockproducts = StockProduct.objects.all()
    # Get Sell order
    sellorder = Order.objects.get(id=pk)
    # Verify discount
    if Discount.objects.all().filter(order=sellorder):
        print("################## Exist")
        discount = Discount.objects.all().filter(order=sellorder)[:1].get()
    else:
        print("################# Don't Exist")
        discount = Discount()
    # Get Customer
    customer = Customer.objects.get(id=sellorder.customer.pk)
    # Get Discount
    discountform = DiscountForm(instance=discount)

    if request.method == 'POST':

        # Product Price & Quantity
        prices = request.POST.getlist('prices')
        quantities = request.POST.getlist('quantities')

        # Panne prices
        panne_prices = request.POST.getlist('panne-prices')

        # Service price & charge
        service_prices = request.POST.getlist('service-prices')
        service_charges = request.POST.getlist('service-charge')

        tva = request.POST.get('tva')
        timbre = request.POST.get('timbre')
        chosen_date = request.POST.get('order_date')
        # get year month day
        chosen_year = chosen_date.split("-", 1)
        chosen_month = chosen_date.split("-", 2)
        chosen_day = chosen_date.split("-", 2)

        if sellorder.items.all():
            for index, item in enumerate(sellorder.items.all()):
                # get the price and value of each element
                # Saving the orderitem
                str_price = prices[index]
                str_price = str_price.replace(",", ".")
                # str_price = str_price.replace(' ', '')
                # Remove white spaces
                str_price = ''.join(str_price.split())
                item.price = str_price
                item.quantity = quantities[index]
                item.save()

        # Pannes
        if sellorder.pannes.all():
            for index, item in enumerate(sellorder.pannes.all()):
                # pannes
                print(panne_prices[index])
                str_panne_price = panne_prices[index]
                str_panne_price = str_panne_price.replace(",", ".")
                # Remove white spaces
                str_panne_price = ''.join(str_panne_price.split())
                item.price = str_panne_price

                item.save()

        # Services
        if sellorder.services.all():
            for index, item in enumerate(sellorder.services.all()):
                # Services
                print(service_prices[index])
                print(service_charges[index])
                str_service_price = service_prices[index]
                str_service_price = str_service_price.replace(",", ".")
                # Remove white spaces
                str_service_price = ''.join(str_service_price.split())
                item.price = str_service_price
                # Add credit to provider
                service = Service.objects.get(id=item.service.id)
                service_provider = ServiceProvider.objects.get(id=service.provider.id)
                service_provider.credit += decimal.Decimal(item.price)
                # Charge
                str_service_charge = service_charges[index]
                str_service_charge = str_service_charge.replace(",", ".")
                # Remove white spaces
                str_service_charge = ''.join(str_service_charge.split())
                item.charge = str_service_charge

                item.save()

        print(request.POST)
        discount.order = sellorder
        discount.value = request.POST.get('discount-value')
        discount.discount_status = request.POST.get('discount-status')
        discount.save()
        print(discount.discount_status)
        if discount.discount_status == '1':
            sellorder.discount_amount = (sellorder.get_ttc() * decimal.Decimal(decimal.Decimal(discount.value) / 100))
        else:
            sellorder.discount_amount = decimal.Decimal(discount.value)

        sellorder.total_price = sellorder.get_total_item_panne()
        sellorder.order_tva = int(tva)
        timbre = timbre.replace(",", ".")
        timbre = ''.join(timbre.split())
        sellorder.timbre = decimal.Decimal(timbre)
        sellorder.debt = sellorder.get_ttc()
        sellorder.order_date = date(int(chosen_year[0]), int(chosen_month[1]), int(chosen_day[2]))
        sellorder.save()
        print(sellorder.confirmed)
        # customer debt
        # customer.debt += sellorder.get_ttc()
        # customer.save()
        return redirect('sellorder:performa_sellorder_list')
    context = {
        'customer': customer,
        'sellorder': sellorder,
        'discountform': discountform,
        'stockproducts': stockproducts,
    }
    return render(request, 'sellorder/sellorder_confirmation.html', context)


# Copy an Order to Performa
def order_to_performa(request, pk):
    performa_order = Order()
    sellorder = Order.objects.get(id=pk)

    # Copy Order
    performa_order.customer = sellorder.customer
    performa_order.vehicle = sellorder.vehicle
    performa_order.debt = sellorder.debt
    performa_order.timbre = sellorder.timbre
    performa_order.total_price = sellorder.total_price
    performa_order.discount_amount = sellorder.discount_amount
    performa_order.paid = sellorder.paid
    performa_order.order_tva = sellorder.order_tva
    performa_order.confirmed = False
    performa_order.factured = False
    performa_order.order_date = sellorder.order_date
    performa_order.save()
    # copy order items
    for item in sellorder.items.all():
        OrderItem.objects.create(
            order=performa_order,
            stockproduct=item.stockproduct,
            price=item.price,
            quantity=item.quantity,
        )
    # copy panne items
    for panne in sellorder.pannes.all():
        PanneItem.objects.create(
            order=performa_order,
            panne=panne.panne,
            price=panne.price,
        )

    return redirect('sellorder:performa_sellorder_list')


def update_order(request, pk):
    stockproducts = StockProduct.objects.all()
    sellorder = Order.objects.get(id=pk)

    if Discount.objects.all().filter(order=sellorder):
        print("################## Exist")
        discount = Discount.objects.all().filter(order=sellorder)[:1].get()
    else:
        print("################# Don't Exist")
        discount = Discount()

    # get customer to add debt
    customer = Customer.objects.get(id=sellorder.customer.pk)
    # Get Discount
    discountform = DiscountForm(instance=discount)
    # Get Old TTC
    old_ttc = round(sellorder.total_price + (
            sellorder.total_price * decimal.Decimal(
        sellorder.order_tva / 100)) - sellorder.discount_amount + sellorder.timbre, 2)
    # TTC after Update
    new_ttc = 0
    # Diference between TTC old & new
    ttc_difference = 0

    # Get Old Date
    old_date = sellorder.order_date

    if request.method == 'POST':
        # delete customer debt until modification over
        # customer.debt -= sellorder.get_ttc()
        # Delete all order elements to be modified
        if sellorder.items.all():
            for item in sellorder.items.all():
                stockitem = StockProduct.objects.get(id=item.stockproduct.id)
                stockitem.quantity += decimal.Decimal(item.quantity)
                stockitem.save()
        # Get the new data to confirm it
        # Product Price & Quantity
        prices = request.POST.getlist('prices')
        quantities = request.POST.getlist('quantities')

        # Panne prices
        panne_prices = request.POST.getlist('panne-prices')

        # Service price & charge
        service_prices = request.POST.getlist('service-prices')
        service_charges = request.POST.getlist('service-charge')

        tva = request.POST.get('tva')
        timbre = request.POST.get('timbre')
        chosen_date = request.POST.get('order_date')
        # get year month day
        chosen_year = chosen_date.split("-", 1)
        chosen_month = chosen_date.split("-", 2)
        chosen_day = chosen_date.split("-", 2)
        # Confirm Items (Products)
        if sellorder.items.all():
            for index, item in enumerate(sellorder.items.all()):
                # get the price and value of each element
                # Saving the orderitem
                # print(index)
                # print(item.stockproduct)
                str_price = prices[index]
                str_price = str_price.replace(",", ".")
                # str_price = str_price.replace(' ', '')
                # Remove white spaces
                str_price = ''.join(str_price.split())
                item.price = str_price

                # treating the quantity
                str_quantity = quantities[index]
                str_quantity = str_quantity.replace(",", ".")
                # Remove white spaces
                str_quantity = ''.join(str_quantity.split())
                # assign quantity
                item.quantity = str_quantity

                print(item.quantity)
                print(item.stockproduct)
                item.save()
                # Reducing the sold products from stock
                stockitems = StockProduct.objects.all().filter(stock=item.stockproduct.stock)
                # check if stock doesn't have the product
                if len(stockitems) > 0:
                    # stock has products check if product exist
                    for stockitem in stockitems:
                        # the same product exist
                        if stockitem.id == item.stockproduct.id:
                            # if stockitem.quantity > 0 and stockitem.quantity - int(item.quantity) >= 0:
                            print("----------------------------------")
                            print(stockitem.quantity - decimal.Decimal(item.quantity))
                            stockitem.quantity -= decimal.Decimal(item.quantity)
                            print(item.stockproduct)
                            print(item.quantity)
                            stockitem.save()

        if sellorder.pannes.all():
            for index, item in enumerate(sellorder.pannes.all()):
                # pannes
                print(panne_prices[index])
                str_panne_price = panne_prices[index]
                str_panne_price = str_panne_price.replace(",", ".")
                # Remove white spaces
                str_panne_price = ''.join(str_panne_price.split())
                item.price = str_panne_price

                item.save()

        if sellorder.services.all():
            for index, item in enumerate(sellorder.services.all()):
                # Services
                print(service_prices[index])
                print(service_charges[index])
                str_service_price = service_prices[index]
                str_service_price = str_service_price.replace(",", ".")
                # Remove white spaces
                str_service_price = ''.join(str_service_price.split())
                item.price = str_service_price
                # Add credit to provider
                service = Service.objects.get(id=item.service.id)
                service_provider = ServiceProvider.objects.get(id=service.provider.id)
                service_provider.credit += decimal.Decimal(item.price)
                # Charge
                str_service_charge = service_charges[index]
                str_service_charge = str_service_charge.replace(",", ".")
                # Remove white spaces
                str_service_charge = ''.join(str_service_charge.split())
                item.charge = str_service_charge
                # saving Values
                item.save()
                service_provider.save()

        discount.order = sellorder
        discount.value = request.POST.get('discount-value')
        discount.discount_status = request.POST.get('discount-status')
        discount.save()
        if discount.discount_status == '1':
            sellorder.discount_amount = (sellorder.get_ttc() * decimal.Decimal(decimal.Decimal(discount.value) / 100))
        else:
            sellorder.discount_amount = decimal.Decimal(discount.value)

        sellorder.total_price = sellorder.get_total_item_panne()
        sellorder.order_date = date(int(chosen_year[0]), int(chosen_month[1]), int(chosen_day[2]))
        sellorder.confirmed = True
        sellorder.order_tva = int(tva)
        timbre = timbre.replace(",", ".")
        timbre = ''.join(timbre.split())
        sellorder.timbre = decimal.Decimal(timbre)
        # get money additiion
        print(old_ttc)
        new_ttc = sellorder.get_ttc()
        print(new_ttc)
        ttc_difference = new_ttc - old_ttc
        print(ttc_difference)
        # sellorder.debt = sellorder.get_ttc()
        sellorder.debt += ttc_difference

        sellorder.save()
        # customer debt
        # customer.debt += sellorder.get_ttc()
        customer.debt -= old_ttc
        customer.debt += new_ttc

        customer.save()
        return redirect('sellorder:sellorder_list')
    context = {
        'customer': customer,
        'sellorder': sellorder,
        'discountform': discountform,
        'stockproducts': stockproducts,
        'tva': sellorder.order_tva,
        'timbre': sellorder.timbre,
        'old_date': old_date,
    }
    return render(request, 'sellorder/sellorder_update.html', context)


# Update order delete item
def order_item_delete(request, orderpk, itempk):
    sellorder = Order.objects.get(id=orderpk)
    if sellorder.items.filter(id=itempk):
        item = sellorder.items.get(id=itempk)
    else:
        return redirect('sellorder:update_order', sellorder.id)
    print(item)
    if request.method == 'POST':
        if sellorder.items.filter(id=itempk):
            item = sellorder.items.get(id=itempk)
            stockproduct = StockProduct.objects.get(id=item.stockproduct.id)
            stockproduct.quantity += item.quantity
            stockproduct.save()
            item.delete()
            return redirect('sellorder:update_order', sellorder.id)
        else:
            return redirect('sellorder:update_order', sellorder.id)

    context = {
        'sellorder': sellorder,
        'item': item
    }
    return render(request, 'sellorder/delete_item.html', context)


# Update order delete item
def order_item_delete(request, orderpk, itempk):
    sellorder = Order.objects.get(id=orderpk)
    if sellorder.items.filter(id=itempk):
        item = sellorder.items.get(id=itempk)
    else:
        return redirect('sellorder:update_order', sellorder.id)
    print(item)
    if request.method == 'POST':
        item = sellorder.items.get(id=itempk)
        stockproduct = StockProduct.objects.get(id=item.stockproduct.id)
        stockproduct.quantity += item.quantity
        stockproduct.save()
        item.delete()
        return redirect('sellorder:update_order', sellorder.id)

    context = {
        'sellorder': sellorder,
        'item': item
    }
    return render(request, 'sellorder/update_order_delete_item.html', context)


# Confirm order delete item
def confirm_order_item_delete(request, orderpk, itempk):
    sellorder = Order.objects.get(id=orderpk)
    if sellorder.items.filter(id=itempk):
        item = sellorder.items.get(id=itempk)
    else:
        return redirect('sellorder:confirm_order', sellorder.id)
    print(item)
    if request.method == 'POST':
        item = sellorder.items.get(id=itempk)
        stockproduct = StockProduct.objects.get(id=item.stockproduct.id)
        stockproduct.quantity += item.quantity
        stockproduct.save()
        item.delete()
        return redirect('sellorder:confirm_order', sellorder.id)

    context = {
        'sellorder': sellorder,
        'item': item
    }
    return render(request, 'sellorder/delete_item.html', context)


# delete panne from order update
def order_panne_delete(request, orderpk, itempk):
    sellorder = Order.objects.get(id=orderpk)
    if sellorder.pannes.filter(id=itempk):
        item = sellorder.pannes.get(id=itempk)
    else:
        return redirect('sellorder:update_order', sellorder.id)
    print(item)
    if request.method == 'POST':
        item = sellorder.pannes.get(id=itempk)
        item.delete()
        return redirect('sellorder:update_order', sellorder.id)

    context = {
        'sellorder': sellorder,
        'item': item
    }
    return render(request, 'sellorder/update_order_delete_panne.html', context)


# delete panne from order confirm
def confirm_order_panne_delete(request, orderpk, itempk):
    sellorder = Order.objects.get(id=orderpk)
    if sellorder.pannes.filter(id=itempk):
        item = sellorder.pannes.get(id=itempk)
    else:
        return redirect('sellorder:confirm_order', sellorder.id)
    print(item)
    if request.method == 'POST':
        item = sellorder.pannes.get(id=itempk)
        item.delete()
        return redirect('sellorder:confirm_order', sellorder.id)

    context = {
        'sellorder': sellorder,
        'item': item
    }
    return render(request, 'sellorder/delete_panne.html', context)


# delete service in confirm order
def confirm_order_service_delete(request, orderpk, itempk):
    sellorder = Order.objects.get(id=orderpk)
    if sellorder.services.filter(id=itempk):
        item = sellorder.services.get(id=itempk)
    else:
        return redirect('sellorder:confirm_order', sellorder.id)
    if request.method == 'POST':
        item = sellorder.services.get(id=itempk)
        item.delete()
        return redirect('sellorder:confirm_order', sellorder.id)

    context = {
        'sellorder': sellorder,
        'item': item
    }
    return render(request, 'sellorder/delete_service.html', context)


# delete service in update order
def order_service_delete(request, orderpk, itempk):
    sellorder = Order.objects.get(id=orderpk)
    if sellorder.services.filter(id=itempk):
        item = sellorder.services.get(id=itempk)
    else:
        return redirect('sellorder:update_order', sellorder.id)
    if request.method == 'POST':
        item = sellorder.services.get(id=itempk)
        item.delete()
        return redirect('sellorder:update_order', sellorder.id)

    context = {
        'sellorder': sellorder,
        'item': item
    }
    return render(request, 'sellorder/update_order_delete_service.html', context)


# order details
def sellorder_details(request, pk):
    order = Order.objects.get(id=pk)
    sellorder_payments = SellOrderPayment.objects.all().filter(order=order)
    context = {
        'order': order,
        'sellorder_payments': sellorder_payments,
    }
    return render(request, 'sellorder/sellorder_details.html', context)


def facture_all(request):
    sellorders = Order.objects.all().filter(factured=True)
    for order in sellorders:
        sellorderfacture = SellOrderFacture()
        sellorderfacture.order = order
        sellorderfacture.save()
        return redirect('sellorder:factured_sellorder_list')

    return render(request, 'sellorder/list_sellorder.html', context={"sellorders": sellorders})


def sellorder_facture(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.factured = True
        order.save()
        sellorderfacture = SellOrderFacture()
        sellorderfacture.order = order
        sellorderfacture.save()
        return redirect('sellorder:factured_sellorder_list')
    return render(request, 'sellorder/sellorder_facture.html', context={'order': order})


def sellorder_list(request):
    list_type = 1  # Sellorder
    dateform = DateForm()
    # now time
    now = datetime.now()
    sellorders = Order.objects.all().filter(confirmed=True, factured=False, created__day=now.day,
                                            created__month=now.month)
    sellorders_customers = Customer.objects.all()
    # sellorders_customers = Order.customer.all()
    # print(sellorders_customers)
    customers = Customer.objects.all()
    # Search request by date===>
    if request.method == 'POST':
        alldata = request.POST
        print(alldata)
        # customer
        chosencustomer = request.POST.getlist("customers")

        if len(chosencustomer) != 0:
            # Remove white spaces
            chosencustomer = ''.join(chosencustomer[0].split())
            customer = Customer.objects.get(id=chosencustomer)
            sellorders = Order.objects.all().filter(customer=customer, confirmed=True, factured=False)

        # Search by date removed
        # chosen_date = alldata.get("date")
        # chosen_date = chosen_date.split("-", 1)
        # chosen_start_date = chosen_date[0]
        # chosen_end_date = chosen_date[1]
        #
        # chosen_start_date = chosen_start_date.split("/", 2)
        # start_month = chosen_start_date[0]
        # start_year = chosen_start_date[2]
        # start_day = chosen_start_date[1]
        # # Remove white spaces
        # start_year = ''.join(start_year.split())
        # start_month = ''.join(start_month.split())
        # start_day = ''.join(start_day.split())
        #
        # chosen_end_date = chosen_end_date.split("/", 2)
        # end_month = chosen_end_date[0]
        # end_year = chosen_end_date[2]
        # end_day = chosen_end_date[1]
        # # Remove white spaces
        # end_year = ''.join(end_year.split())
        # end_month = ''.join(end_month.split())
        # end_day = ''.join(end_day.split())
        #
        # sellorders = Order.objects.all().filter(
        #     Q(
        #         created__gt=date(int(start_year), int(start_month),
        #                          int(start_day)),
        #         created__lt=date(int(end_year), int(end_month), int(end_day))
        #     )
        #     |
        #     Q(
        #         created=date(int(end_year), int(end_month), int(end_day))
        #     )
        #     , confirmed=True, factured=False,
        #
        # )
    # print(customers)
    context = {
        'sellorders': sellorders,
        "dateform": dateform,
        'customers': customers,
        'list_type': list_type,
    }
    return render(request, 'sellorder/list_sellorder.html', context)


def sellorder_list_by_date(request):
    list_type = 1  # Sellorder
    dateform = DateForm()
    # now time
    now = datetime.now()
    chosen_date = datetime.now()
    sellorders = Order.objects.all().filter(confirmed=True, factured=False, created__year=now.year,
                                            created__day=now.day,
                                            created__month=now.month)

    if request.method == 'POST':
        alldata = request.POST
        print(alldata)
        # customer

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

        sellorders = Order.objects.all().filter(
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

    context = {
        'sellorders': sellorders,
        "dateform": dateform,
        'list_type': list_type,
        'chosen_date': chosen_date,
    }
    return render(request, 'sellorder/list_sellorder_by_date.html', context)


def factured_sellorder_list(request):
    list_type = 2  # Sellorder Bill
    sellorders = SellOrderFacture.objects.all()
    context = {
        'sellorders': sellorders,
        'list_type': list_type,
    }
    return render(request, 'sellorder/list_sellorder_facture.html', context)


def performa_sellorder_list(request):
    list_type = 3  # Sellorder Proforma Bill
    # now time
    now = datetime.now()

    sellorders = Order.objects.all().filter(confirmed=False, factured=False, created__day=now.day,
                                            created__month=now.month)

    customers = Customer.objects.all()
    if request.method == 'POST':
        alldata = request.POST
        print(alldata)
        # customer
        chosencustomer = request.POST.getlist("customers")
        if len(chosencustomer) != 0:
            # Remove white spaces
            chosen_customer = ''.join(chosencustomer[0].split())
            customer = Customer.objects.get(id=chosen_customer)
            sellorders = Order.objects.all().filter(customer=customer, confirmed=False, factured=False)

    context = {
        'sellorders': sellorders,
        'list_type': list_type,
        'customers': customers,
    }
    return render(request, 'sellorder/list_sellorder.html', context)


def sellorder_delete(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        if order.confirmed:
            if order.items.all():
                for item in order.items.all():
                    stockitem = StockProduct.objects.get(id=item.stockproduct.id)
                    stockitem.quantity += decimal.Decimal(item.quantity)
                    stockitem.save()
        customer = Customer.objects.get(id=order.customer.id)
        customer.debt -= order.debt

        if SellOrderPayment.objects.all().filter(order=order):
            customerpayments = SellOrderPayment.objects.all().filter(order=order)
            for customerpayment in customerpayments:
                caisse = Caisse.objects.all().filter()[:1].get()
                caisse.caisse_value -= customerpayment.amount
                # customer.debt += customerpayment.amount
                caisse.save()
                customerpayment.delete()
        customer.save()
        order.delete()
        return redirect('sellorder:sellorder_list')
    context = {
        'order': order
    }
    return render(request, 'sellorder/sellorder_delete.html', context)


def sellorder_list_by_customer(request, pk):
    customer = Customer.objects.get(id=pk)
    sellorders = Order.objects.all().filter(customer=customer, factured=False)

    if request.method == 'POST':
        # get submitted orders
        chosenorders = request.POST.getlist("orders")
        # create billing object if there is selected orders
        if len(chosenorders) != 0:
            # print(chosenorders)
            # buyorderbill object
            sellorderbilling = OrderBilling()
            sellorderbilling.customer = customer
            # TODO : Uncomment this line
            # buyorderbilling.user = request.user.id
            sellorderbilling.save()
            for orderid in chosenorders:
                # each order is a billing item
                currentorder = Order.objects.get(id=orderid)
                currentorder.factured = True
                currentorder.save()
                orderprice = currentorder.get_total_cost()
                # adding customer debt
                customer.debt += orderprice
                customer.save()
                BillOrderItem.objects.create(
                    bill=sellorderbilling,
                    order=currentorder,
                    price=orderprice,
                    # weight=orderweight,
                )
            pk = sellorderbilling.pk
            return redirect(f'../../billing/sellbill_pdf/{pk}')

    context = {
        'sellorders': sellorders
    }
    return render(request, 'sellorder/billing_list_sellorder.html', context)


def sellorder_pdf(request, pk, credit, tva):
    sellorder = get_object_or_404(Order, id=pk)
    customer = get_object_or_404(Customer, id=sellorder.customer.id)
    if customer.debt - sellorder.get_ttc() == 0 or customer.debt - sellorder.get_ttc() < 0:
        old_debt = 0
    else:
        old_debt = customer.debt - sellorder.get_ttc()
    new_debt = old_debt + sellorder.get_ttc()

    # print("Customer Debt", customer.debt)
    # print("Order Debt", sellorder.debt)
    # print("Old Debt", old_debt)
    # print("New Debt", new_debt)
    # print("TTC", sellorder.get_ttc())

    html = render_to_string('sellorder/pdf.html',
                            {'order': sellorder,
                             'customer': customer,
                             'old_debt': old_debt,
                             'new_debt': new_debt,
                             'credit': credit,
                             'tva': tva,
                             })
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{sellorder.id}.pdf'

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


# Bon Pour
def sellorder_pour_pdf(request, pk, credit, tva):
    sellorder = get_object_or_404(Order, id=pk)
    customer = get_object_or_404(Customer, id=sellorder.customer.id)
    if customer.debt - sellorder.get_ttc() == 0 or customer.debt - sellorder.get_ttc() < 0:
        old_debt = 0
    else:
        old_debt = customer.debt - sellorder.get_ttc()
    new_debt = old_debt + sellorder.get_ttc()

    # print("Customer Debt", customer.debt)
    # print("Order Debt", sellorder.debt)
    # print("Old Debt", old_debt)
    # print("New Debt", new_debt)
    # print("TTC", sellorder.get_ttc())

    html = render_to_string('sellorder/bon_pour_pdf.html',
                            {'order': sellorder,
                             'customer': customer,
                             'old_debt': old_debt,
                             'new_debt': new_debt,
                             'credit': credit,
                             'tva': tva,
                             })
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{sellorder.id}.pdf'

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


# Bon livraison
def sellorder_livraison_pdf(request, pk, credit, tva):
    sellorder = get_object_or_404(Order, id=pk)
    customer = get_object_or_404(Customer, id=sellorder.customer.id)
    if customer.debt - sellorder.get_ttc() == 0 or customer.debt - sellorder.get_ttc() < 0:
        old_debt = 0
    else:
        old_debt = customer.debt - sellorder.get_ttc()
    new_debt = old_debt + sellorder.get_ttc()

    # print("Customer Debt", customer.debt)
    # print("Order Debt", sellorder.debt)
    # print("Old Debt", old_debt)
    # print("New Debt", new_debt)
    # print("TTC", sellorder.get_ttc())

    html = render_to_string('sellorder/bon_livraison_pdf.html',
                            {'order': sellorder,
                             'customer': customer,
                             'old_debt': old_debt,
                             'new_debt': new_debt,
                             'credit': credit,
                             'tva': tva,
                             })
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{sellorder.id}.pdf'

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def sellorder_facture_pdf(request, pk):
    order = get_object_or_404(Order, id=pk)
    sellorder = get_object_or_404(SellOrderFacture, order=order)
    customer = Customer.objects.get(id=sellorder.order.customer.id)
    if customer.enterprise:
        enterprise = Enterprise.objects.get(customer=customer)
    else:
        enterprise = Enterprise.objects.none()
    # tva for products only
    tva = round(order.get_total_cost() * decimal.Decimal(0.19), 2)
    # get total price for products only
    total_price = order.get_total_cost() + tva + order.timbre
    total_in_letters = num2words(total_price, lang='fr_DZ', to='currency')
    context = {
        'order': sellorder,
        'total_in_letters': total_in_letters.capitalize(),
        'enterprise': enterprise,
        'tva': tva,
        'total_price': total_price,
    }
    html = render_to_string('sellorder/facture_pdf.html', context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{sellorder.id}_{sellorder.order.customer}.pdf'

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response, encoding='UTF-8')

    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def sellorder_facture_no_date_pdf(request, pk):
    order = get_object_or_404(Order, id=pk)
    sellorder = get_object_or_404(SellOrderFacture, order=order)
    customer = Customer.objects.get(id=sellorder.order.customer.id)
    if customer.enterprise:
        enterprise = Enterprise.objects.get(customer=customer)
    else:
        enterprise = Enterprise.objects.none()
    # tva for products only
    tva = round(order.get_total_cost() * decimal.Decimal(0.19), 2)
    # get total price for products only
    total_price = order.get_total_cost() + tva + order.timbre
    total_in_letters = num2words(total_price, lang='fr_DZ', to='currency')
    context = {
        'order': sellorder,
        'total_in_letters': total_in_letters.capitalize(),
        'enterprise': enterprise,
        'tva': tva,
        'total_price': total_price,
    }
    html = render_to_string('sellorder/facture_no_date_pdf.html', context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{sellorder.id}_{sellorder.order.customer}.pdf'

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response, encoding='UTF-8')
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def sellorder_facture_mo_pdf(request, pk):
    order = get_object_or_404(Order, id=pk)
    sellorder = get_object_or_404(SellOrderFacture, order=order)
    customer = Customer.objects.get(id=sellorder.order.customer.id)
    if customer.enterprise:
        enterprise = Enterprise.objects.get(customer=customer)
    else:
        enterprise = Enterprise.objects.none()
    # total panne + service
    total_ht = order.get_total_panne() + order.get_total_service()
    # tva panne + service only
    tva = round(total_ht * decimal.Decimal(0.19), 2)
    # TTC
    total_price = total_ht + tva + order.timbre

    total_in_letters = num2words(total_price, lang='fr_DZ', to='currency')
    context = {
        'order': sellorder,
        'total_in_letters': total_in_letters.capitalize(),
        'enterprise': enterprise,
        'total_ht': total_ht,
        'tva': tva,
        'total_price': total_price,
    }
    html = render_to_string('sellorder/facture_mo_pdf.html', context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{sellorder.id}_{sellorder.order.customer}.pdf'

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def sellorder_facture_mo_no_date_pdf(request, pk):
    order = get_object_or_404(Order, id=pk)
    sellorder = get_object_or_404(SellOrderFacture, order=order)
    customer = Customer.objects.get(id=sellorder.order.customer.id)
    if customer.enterprise:
        enterprise = Enterprise.objects.get(customer=customer)
    else:
        enterprise = Enterprise.objects.none()
    # total panne + service
    total_ht = order.get_total_panne() + order.get_total_service()
    # tva panne + service only
    tva = round(total_ht * decimal.Decimal(0.19), 2)
    # TTC
    total_price = total_ht + tva + order.timbre

    total_in_letters = num2words(total_price, lang='fr_DZ', to='currency')
    context = {
        'order': sellorder,
        'total_in_letters': total_in_letters.capitalize(),
        'enterprise': enterprise,
        'total_ht': total_ht,
        'tva': tva,
        'total_price': total_price,
    }
    html = render_to_string('sellorder/facture_mo_no_date_pdf.html', context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{sellorder.id}_{sellorder.order.customer}.pdf'

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def sellorder_facture_proforma_pdf(request, pk):
    order = get_object_or_404(Order, id=pk)
    customer = Customer.objects.get(id=order.customer.id)
    if customer.enterprise:
        enterprise = Enterprise.objects.get(customer=customer)
    else:
        enterprise = Enterprise.objects.none()
    total_in_letters = num2words(order.get_ttc(), lang='fr_DZ', to='currency')
    context = {
        'order': order,
        'total_in_letters': total_in_letters.capitalize(),
        'enterprise': enterprise
    }
    html = render_to_string('sellorder/facture_proforma_pdf.html', context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}_{order.customer}.pdf'

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


# proforma MO
def sellorder_facture_proforma_mo_pdf(request, pk):
    order = get_object_or_404(Order, id=pk)
    customer = Customer.objects.get(id=order.customer.id)
    if customer.enterprise:
        enterprise = Enterprise.objects.get(customer=customer)
    else:
        enterprise = Enterprise.objects.none()

    # total panne + service
    total_ht = order.get_total_panne() + order.get_total_service()
    # tva panne + service only
    tva = round(total_ht * decimal.Decimal(0.19), 2)
    # TTC
    total_price = total_ht + tva + order.timbre
    total_in_letters = num2words(total_price, lang='fr_DZ', to='currency')
    context = {
        'order': order,
        'total_in_letters': total_in_letters.capitalize(),
        'enterprise': enterprise,
        'total_ht': total_ht,
        'tva': tva,
        'total_price': total_price,
    }
    html = render_to_string('sellorder/facture_proforma_mo_pdf.html', context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}_{order.customer}.pdf'

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


# proforma Piece
def sellorder_facture_proforma_piece_pdf(request, pk):
    order = get_object_or_404(Order, id=pk)
    customer = Customer.objects.get(id=order.customer.id)
    if customer.enterprise:
        enterprise = Enterprise.objects.get(customer=customer)
    else:
        enterprise = Enterprise.objects.none()

    # tva for products only
    tva = round(order.get_total_cost() * decimal.Decimal(0.19), 2)
    # get total price for products only
    total_price = order.get_total_cost() + tva + order.timbre
    total_in_letters = num2words(total_price, lang='fr_DZ', to='currency')
    context = {
        'order': order,
        'total_in_letters': total_in_letters.capitalize(),
        'enterprise': enterprise,
        'tva': tva,
        'total_price': total_price,
    }
    html = render_to_string('sellorder/facture_proforma_piece_pdf.html', context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}_{order.customer}.pdf'

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def bsb_sellorder_facture_proforma_pdf(request, pk):
    order = get_object_or_404(Order, id=pk)
    customer = Customer.objects.get(id=order.customer.id)
    if customer.enterprise:
        enterprise = Enterprise.objects.get(customer=customer)
    else:
        enterprise = Enterprise.objects.none()
    total_in_letters = num2words(order.get_ttc() * 3, lang='fr_DZ', to='currency')
    context = {
        'order': order,
        'total_in_letters': total_in_letters.capitalize(),
        'enterprise': enterprise
    }
    html = render_to_string('sellorder/bsb_facture_proforma_pdf.html', context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}_{order.customer}.pdf'

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def nacer_sellorder_facture_proforma_pdf(request, pk):
    order = get_object_or_404(Order, id=pk)
    customer = Customer.objects.get(id=order.customer.id)
    if customer.enterprise:
        enterprise = Enterprise.objects.get(customer=customer)
    else:
        enterprise = Enterprise.objects.none()
    total_in_letters = num2words(order.get_ttc() * 2, lang='fr_DZ', to='currency')
    context = {
        'order': order,
        'total_in_letters': total_in_letters.capitalize(),
        'enterprise': enterprise
    }
    html = render_to_string('sellorder/nacer_facture_proforma_pdf.html', context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}_{order.customer}.pdf'

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def ghezal_sellorder_facture_proforma_pdf(request, pk):
    order = get_object_or_404(Order, id=pk)
    customer = Customer.objects.get(id=order.customer.id)
    if customer.enterprise:
        enterprise = Enterprise.objects.get(customer=customer)
    else:
        enterprise = Enterprise.objects.none()
    total_in_letters = num2words(order.get_ttc() * 2, lang='fr_DZ', to='currency')
    context = {
        'order': order,
        'total_in_letters': total_in_letters.capitalize(),
        'enterprise': enterprise
    }
    html = render_to_string('sellorder/ghezal_facture_proforma_pdf.html', context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}_{order.customer}.pdf'

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def sellorder_facture_proforma_pdf_no_date(request, pk):
    order = get_object_or_404(Order, id=pk)
    customer = Customer.objects.get(id=order.customer.id)
    if customer.enterprise:
        enterprise = Enterprise.objects.get(customer=customer)
    else:
        enterprise = Enterprise.objects.none()
    total_in_letters = num2words(order.get_ttc(), lang='fr_DZ', to='currency')
    context = {
        'order': order,
        'total_in_letters': total_in_letters.capitalize(),
        'enterprise': enterprise
    }
    html = render_to_string('sellorder/facture_proforma_pdf_no_date.html', context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}_{order.customer}.pdf'

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


# pannes per period date
def get_orders_pannes(request):
    # now time
    now = datetime.now()
    dateform = DateForm()
    periodform = PeriodForm()
    orders = Order.objects.all().filter(confirmed=True, created__year=now.year, created__month=now.month, created__day=now.day)
    pannes = Panne.objects.none()
    totalpanne = 0
    chief_percentage = 0
    if request.method == 'POST':
        # Get Date from request.POST
        alldata = request.POST
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

        # Date Submit ----------date_created
        orders = Order.objects.all().filter(order_date__gte=date(int(start_year), int(start_month), int(start_day)),
                                            order_date__lte=date(int(end_year), int(end_month), int(end_day)))

    for order in orders:
        pannes |= order.pannes.all()
        totalpanne += order.get_total_panne()
        # calculate workshop chief 10%
        # get customer
        order_customer = order.customer
        # check if the customer enterprise 5% else 10%
        if Enterprise.objects.filter(customer=order_customer):
            chief_percentage += (order.get_total_panne() * 5) / 100
        else:
            chief_percentage += (order.get_total_panne() * 10) / 100
    # print(pannes)

    context = {
        'pannes': pannes,
        'periodform': periodform,
        'totalpanne': totalpanne,
        "dateform": dateform,
        'chief_percentage': chief_percentage,

    }
    return render(request, 'sellorder/sellorders_pannes.html', context)


# piece per period date
def get_orders_pieces(request):
    # now time
    now = datetime.now()
    dateform = DateForm()
    periodform = PeriodForm()
    orders = Order.objects.all().filter(confirmed=True, created__year=now.year, created__month=now.month, created__day=now.day)
    pieces = OrderItem.objects.none()
    totalpiece = 0
    if request.method == 'POST':
        # Get Date from request.POST
        alldata = request.POST
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

        # Date Submit ----------date_created
        orders = Order.objects.all().filter(order_date__gte=date(int(start_year), int(start_month), int(start_day)),
                                            order_date__lte=date(int(end_year), int(end_month), int(end_day)))
    for order in orders:
        pieces |= order.items.all()
        totalpiece += order.get_total_cost()

    context = {
        'pieces': pieces,
        'periodform': periodform,
        'totalpiece': totalpiece,
        "dateform": dateform,
    }
    return render(request, 'sellorder/sellorders_pieces.html', context)


# payed pannes per period date
def get_orders_pannes_payed(request):
    # now time
    now = datetime.now()
    dateform = DateForm()
    periodform = PeriodForm()
    orders = Order.objects.all().filter(created__year=now.year, created__month=now.month, created__day=now.day,
                                        paid=True)
    pannes = Panne.objects.none()
    totalpanne = 0
    if request.method == 'POST':
        # Get Date from request.POST
        alldata = request.POST
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

        # Date Submit ----------date_created
        orders = Order.objects.all().filter(created__year__gte=int(start_year), created__month__gte=int(start_month),
                                            created__day__gte=int(start_day),
                                            created__year__lte=int(end_year), created__month__lte=int(end_month),
                                            created__day__lte=int(end_day)
                                            )
    for order in orders:
        pannes |= order.pannes.all()
        totalpanne += order.get_total_panne()
    print(pannes)

    context = {
        'pannes': pannes,
        'periodform': periodform,
        'totalpanne': totalpanne,
        "dateform": dateform,

    }
    return render(request, 'sellorder/sellorders_pannes.html', context)


# piece per period date
def get_orders_pieces_payed(request):
    # now time
    now = datetime.now()
    dateform = DateForm()
    periodform = PeriodForm()
    orders = Order.objects.all().filter(created__year=now.year, created__month=now.month, created__day=now.day,
                                        paid=True)
    pieces = OrderItem.objects.none()
    totalpiece = 0
    if request.method == 'POST':
        # Get Date from request.POST
        alldata = request.POST
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

        # Date Submit ----------date_created
        orders = Order.objects.all().filter(created__gte=date(int(start_year), int(start_month), int(start_day)),
                                            created__lte=date(int(end_year), int(end_month), int(end_day)))
    for order in orders:
        pieces |= order.items.all()
        totalpiece += order.get_total_cost()

    context = {
        'pieces': pieces,
        'periodform': periodform,
        'totalpiece': totalpiece,
        "dateform": dateform,
    }
    return render(request, 'sellorder/sellorders_pieces.html', context)
