from django.shortcuts import render, redirect, get_object_or_404
from xhtml2pdf import pisa
from django.template.loader import render_to_string
from django.http import HttpResponse

# Create your views here.
from billing.models import OrderBilling, BillOrderItem
from caisse.models import Caisse
from customer.models import Customer
from discount.forms import DiscountForm
from payments.forms import CustomerPaymentForm
from payments.models import SellOrderPayment
from sellorder.apps import SellorderConfig
from sellorder.models import Order
from stock.models import StockProduct


# confirmation get order object from the stock view
def confirm_order(request, pk):
    stockproducts = StockProduct.objects.all()
    sellorder = Order.objects.get(id=pk)
    # get customer to add debt
    customer = Customer.objects.get(id=sellorder.customer.pk)
    # Get Discount
    discountform = DiscountForm()
    # print(sellorder.vehicle)
    if request.method == 'POST':
        prices = request.POST.getlist('prices')
        quantities = request.POST.getlist('quantities')

        for index, item in enumerate(sellorder.items.all()):
            # get the price and value of each element
            # Saving the orderitem
            item.price = prices[index]
            item.quantity = quantities[index]
            item.save()
            # Reducing the sold products from stock
            stockitems = StockProduct.objects.all().filter(stock=item.stockproduct.product.stock)
            itemexist = 1
            #     # check if stock doesn't have the product
            if len(stockitems) > 0:
                # stock has products check if product exist
                for stockitem in stockitems:
                    # the same product exist
                    if stockitem.product.id == item.stockproduct.product.id:
                        stockitem.quantity -= int(item.quantity)
                        stockitem.save()
                        itemexist = 2
                        #                 # operation done same product plus the new quantity

                if itemexist == 1:
                    #             # stock not empty product doesn't exist in it
                    #             # create new stockproduct
                    StockProduct.objects.create(
                        product=item.stockproduct.product,
                        quantity=int(item.quantity),
                        # type=item.type,
                        # color=item.color,
                        # category=item.stockproduct.product.category,
                        stock=item.stockproduct.product.stock
                    )
            else:
                #         # stock is empty
                itemexist = 0
                if itemexist == 0:
                    # create new stockproduct
                    StockProduct.objects.create(
                        product=item.stockproduct.product,
                        quantity=int(item.quantity),
                        # type=item.type,
                        # color=item.color,
                        # category=item.stockproduct.product.category,
                        stock=item.stockproduct.product.stock
                    )
        sellorder.debt = sellorder.get_total_item_panne()
        sellorder.total_price = sellorder.get_total_item_panne()
        sellorder.confirmed = True
        sellorder.save()
        # customer debt
        customer.debt += sellorder.get_total_item_panne()
        customer.save()
        # batch (installement) page
        return redirect('sellorder:sellorder_list')
    context = {
        'customer': customer,
        'sellorder': sellorder,
        'discountform': discountform,
        'stockproducts': stockproducts,
    }
    return render(request, 'sellorder/sellorder_confirmation.html', context)


def sellorder_details(request, pk):
    order = Order.objects.get(id=pk)
    context = {
        'order': order
    }
    return render(request, 'sellorder/sellorder_details.html', context)


def sellorder_list(request):
    sellorders = Order.objects.all()
    context = {
        'sellorders': sellorders
    }
    return render(request, 'sellorder/list_sellorder.html', context)


def sellorder_delete(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        if order.confirmed:
            if order.items.all():
                for item in order.items.all():
                    stockitem = StockProduct.objects.get(id=item.stockproduct.id)
                    stockitem.quantity += int(item.quantity)
                    stockitem.save()
        customer = Customer.objects.get(id=order.customer.id)
        customer.debt -= order.debt
        customer.save()
        if SellOrderPayment.objects.all().filter(order=order):
            customerpayment = SellOrderPayment.objects.get(order=order)
            caisse = Caisse.objects.all().filter()[:1].get()
            caisse.caisse_value -= customerpayment.amount
            caisse.save()
            customerpayment.delete()
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


def sellorder_pdf(request, pk):
    sellorder = get_object_or_404(Order, id=pk)
    html = render_to_string('sellorder/pdf.html', {'order': sellorder})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{sellorder.id}.pdf'

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
