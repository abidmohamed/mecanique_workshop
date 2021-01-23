from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
# Create your views here.
from billing.models import BuyOrderBilling, BillBuyOrderItem
from buyorder.forms import BuyOrderForm, BuyOrderItemFormset
from buyorder.models import BuyOrderItem, BuyOrder
from product.models import Product
from supplier.models import Supplier
from stock.models import StockProduct


def create_buyorder(request):
    buyorderform = BuyOrderForm()
    buyorderitemformset = BuyOrderItemFormset(queryset=BuyOrderItem.objects.none())

    products = Product.objects.all()

    if request.method == 'POST':
        # print(request.POST)
        # fix the form to be validated
        # get the list of the chosen products
        products_list = request.POST.getlist('products')
        # print(products_list)
        buyorderform = BuyOrderForm(request.POST)
        # if the list has elements

        if buyorderform.is_valid():
            if len(products_list):
                buyorder = buyorderform.save()
                # to add credit
                # supplier = Supplier.objects.get(id=request.POST['supplier'])
                buyorder.user = request.user.id
                for prod_list_item in products_list:
                    # saving the order items
                    orderitem = BuyOrderItem()
                    orderitem.order = buyorder
                    orderitem.product = Product.objects.get(id=prod_list_item)
                    orderitem.price = Product.objects.get(id=prod_list_item).buyprice
                    orderitem.save()
                    # print(Product.objects.get(id=prod_list_item))

            return redirect(f'../buyorder/buyorder_confirmation/{buyorder.pk}')
    context = {
        'products': products,
        'buyorderform': buyorderform,
        'buyorderitemformset': buyorderitemformset
    }
    return render(request, 'buyorder/add_buyorder.html', context)


def buyorder_confirmation(request, pk):
    buyorder = BuyOrder.objects.get(id=pk)

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

            for index, item in enumerate(buyorder.items.all()):
                # print(index, item)
                print(prices[index], quantities[index])
                # get the price and value of each element
                # Saving the orderitem
                item.price = prices[index]
                item.quantity = quantities[index]
                item.save()
                # adding the bought products to stock
                stockitems = StockProduct.objects.all().filter(stock=item.product.stock)
                itemexist = 1
                #     # check if stock doesn't have the product
                # if len(stockitems) > 0:
                #     # stock has products check if product exist
                #     for stockitem in stockitems:
                #         # the same product exist
                #         if stockitem.product.id == item.product.id:
                #             stockitem.quantity += int(item.quantity)
                #             stockitem.save()
                #             itemexist = 2
                #             #                 # operation done same product plus the new quantity
                #
                #     if itemexist == 1:
                #         #             # stock not empty product doesn't exist in it
                #         #             # create new stockproduct
                #         StockProduct.objects.create(
                #             product=item.product,
                #             quantity=int(item.quantity),
                #             category=item.product.category,
                #             stock=item.product.stock
                #         )
                # else:
                #     #         # stock is empty
                #     itemexist = 0
                #     if itemexist == 0:
                #         # create new stockproduct
                #         StockProduct.objects.create(
                #             product=item.product,
                #             quantity=int(item.quantity),
                #             type=item.type,
                #             color=item.color,
                #             category=item.product.category,
                #             stock=item.product.stock
                #         )
            print(buyorder.get_total_cost())
            print(supplier)
            # supplier.credit += buyorder.get_total_cost()
            # supplier.save()
            return redirect('buyorder:buyorder_list')
    context = {
        'buyorderform': buyorderform,
        'buyorder': buyorder,
    }
    return render(request, 'buyorder/buyorder_confirmation.html', context)


def buyorder_list(request):
    buyorders = BuyOrder.objects.all()
    context = {
        'buyorders': buyorders
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
                                stockitem.quantity += int(item.quantity)
                                stockitem.save()
                                itemexist = 2
                                #                 # operation done same product plus the new quantity

                        if itemexist == 1:
                            #             # stock not empty product doesn't exist in it
                            #             # create new stockproduct
                            StockProduct.objects.create(
                                product=item.product,
                                quantity=int(item.quantity),
                                category=item.product.category,
                                stock=item.product.stock
                            )
                    else:
                        #         # stock is empty
                        itemexist = 0
                        if itemexist == 0:
                            # create new stockproduct
                            StockProduct.objects.create(
                                product=item.product,
                                quantity=int(item.quantity),
                                category=item.product.category,
                                stock=item.product.stock
                            )
            # send bill to be printed
            pk = buyorderbilling.pk
            return redirect(f'../../billing/buybill_pdf/{pk}')

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
