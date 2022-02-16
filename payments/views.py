from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from buyorder.models import BuyOrder
from caisse.models import Caisse
from customer.models import Customer
from payments.forms import CustomerChequeForm, SupplierPaymentForm, SupplierChequeForm, CustomerPaymentForm, \
    ServicePaymentForm, CustomerVermentForm
from payments.models import SellOrderPayment, BuyOrderPayment, CustomerCheque, ServicePayment, SupplierCheque
from sellorder.models import Order
from services.models import ServiceProvider
from supplier.models import Supplier


# Sell Order Payment is Customer Payment
def create_customer_payment(request, pk):
    order = Order.objects.get(id=pk)
    customer = Customer.objects.get(id=order.customer.id)
    customerpaymentform = CustomerPaymentForm()
    if request.method == "POST":
        customerpaymentform = CustomerPaymentForm(request.POST)
        if customerpaymentform.is_valid():
            customerpayment = customerpaymentform.save(commit=False)
            print(customerpayment.amount)
            customerpayment.order = order
            customerpayment.customer = order.customer
            customerpayment.save()
            if order.debt == 0 or order.debt is None:
                order.debt = order.get_ttc()
            print(order.debt)
            order.debt -= customerpayment.amount
            # print(order.debt)
            if order.debt == 0:
                order.paid = True
            order.save()
            customer.debt -= customerpayment.amount
            customer.save()

            caisse = Caisse.objects.all().filter()[:1].get()
            caisse.caisse_value += customerpayment.amount
            caisse.save()

            # TODO: Uncomment this one
            # customerpayment.user = request.user.id
            if customerpayment.pay_status == "Cheque":
                return redirect(f'../create_customer_cheque/{customerpayment.pk}')
            if customerpayment.pay_status == "Verement":
                return redirect("payments:create_customer_verment", customerpayment.pk)
            return redirect('customer:customer_list')
    context = {
        'customerpaymentform': customerpaymentform,
        'customer': customer,
    }
    return render(request, 'payments/customer/create_payment.html', context)


def delete_customer_payment(request, pk):
    sellorder_payment = SellOrderPayment.objects.get(id=pk)
    order = Order.objects.get(id=sellorder_payment.order.id)
    if request.method == "POST":
        # fix order values before deleting
        order.debt += sellorder_payment.amount
        order.customer.debt += sellorder_payment.amount
        order.save()
        order.customer.save()
        # fix caisse value before deleting
        caisse = Caisse.objects.all().filter()[:1].get()
        caisse.caisse_value -= sellorder_payment.amount
        caisse.save()
        # delete payment cheque is automatic
        # delete payment
        sellorder_payment.delete()

        return redirect("payments:customer_payment_list")

    context = {
        'sellorder_payment': sellorder_payment,
        'order': order,
    }
    return render(request, 'payments/customer/delete_payment.html', context)


def create_customer_cheque(request, pk):
    customerpayment = SellOrderPayment.objects.get(id=pk)
    customerchequeform = CustomerChequeForm()
    if request.method == "POST":
        customerchequeform = CustomerChequeForm(request.POST)
        if customerchequeform.is_valid():
            customercheque = customerchequeform.save(commit=False)
            customercheque.customer = customerpayment.customer
            customercheque.customerpayment = customerpayment
            customercheque.save()
            return redirect("payments:customer_payment_list")

    context = {
        "customerchequeform": customerchequeform
    }
    return render(request, 'payments/customer/create_cheque.html', context)


def create_customer_verment(request, pk):
    customerpayment = SellOrderPayment.objects.get(id=pk)
    customervermentform = CustomerVermentForm()
    if request.method == "POST":
        customervermentform = CustomerVermentForm(request.POST)
        if customervermentform.is_valid():
            customerverment = customervermentform.save(commit=False)
            customerverment.customer = customerpayment.customer
            customerverment.customerpayment = customerpayment
            customerverment.save()
            return redirect("payments:customer_payment_list")

    context = {
        "customerchequeform": customervermentform,
    }
    return render(request, 'payments/customer/create_cheque.html', context)


def customer_payment_list(request):
    customerpayments = SellOrderPayment.objects.all()
    context = {
        "customerpayments": customerpayments
    }
    return render(request, 'payments/customer/payment_list.html', context)


# Supplier Payment is BuyOrderPayment
def create_supplier_payment(request, pk):
    # supplier = Supplier.objects.get(id=pk)
    order = BuyOrder.objects.get(id=pk)
    supplierpaymentform = SupplierPaymentForm()
    if request.method == "POST":
        supplierpaymentform = SupplierPaymentForm(request.POST)
        if supplierpaymentform.is_valid():
            supplierpayment = supplierpaymentform.save(commit=False)
            print(supplierpayment.amount)
            supplierpayment.order = order
            supplierpayment.supplier = order.supplier
            supplierpayment.save()
            if order.debt == 0 or order.debt is None:
                order.debt = order.get_total_cost()
            order.debt -= supplierpayment.amount
            order.supplier.credit -= supplierpayment.amount
            caisse = Caisse.objects.all().filter()[:1].get()
            caisse.caisse_value -= supplierpayment.amount
            caisse.save()
            if order.debt == 0:
                order.paid = True
            order.supplier.save()
            order.save()
            # TODO: Uncomment this one
            # supplierpayment.user = request.user.id
            if supplierpayment.pay_status == "Cheque":
                return redirect(f'../create_supplier_cheque/{supplierpayment.pk}')
            return redirect('supplier:supplier_list')
    context = {
        'supplierpaymentform': supplierpaymentform,
    }
    return render(request, 'payments/supplier/create_payment.html', context)


# Supplier Payment is BuyOrderPayment
def create_supplier_payment_by_supplier(request, pk):
    supplier = Supplier.objects.get(id=pk)
    orders = BuyOrder.objects.all().filter(supplier=supplier, debt__gt=0).order_by('order_date')
    print(orders)
    supplierpaymentform = SupplierPaymentForm()
    if request.method == "POST":
        supplierpaymentform = SupplierPaymentForm(request.POST)
        if supplierpaymentform.is_valid():
            supplierpayment = supplierpaymentform.save(commit=False)
            # print(supplierpayment.amount)
            # supplierpayment.order = order
            supplierpayment.supplier = supplier
            supplierpayment.save()
            payed_amount = supplierpayment.amount
            rest_amount = payed_amount
            for order in orders:
                # if order.debt == 0 or order.debt is None:
                # order.debt = order.get_ttc()
                if rest_amount > 0 and order.debt > 0:
                    # print("#### First Step")
                    # print(order)
                    # print(order.debt)
                    # print(payed_amount)
                    # print(rest_amount)
                    # print("#### Second Step")
                    # how to reach zero for debt
                    if payed_amount > order.debt:
                        # if payment amount is bigger than reduce only the debt
                        to_reach_zero = order.debt
                    else:
                        # if the debt is bigger than reduce the amount
                        to_reach_zero = payed_amount
                    # the rest after the operation
                    rest_amount = payed_amount - order.debt
                    # print(to_reach_zero)
                    order.debt -= to_reach_zero
                    # supplierpayment.order = order
                    # supplierpayment.save()
                    payed_amount = rest_amount
                    # print("#### Last Step")
                    # print(order.debt)
                    # print(payed_amount)
                    # print(rest_amount)
                    if order.debt == 0:
                        order.paid = True
                    order.save()

            supplier.credit -= supplierpayment.amount
            # caisse = Caisse.objects.all().filter()[:1].get()
            # caisse.caisse_value -= supplierpayment.amount
            # caisse.save()
            supplier.save()

            # TODO: Uncomment this one
            # supplierpayment.user = request.user.id
            if supplierpayment.pay_status == "Cheque":
                return redirect(f'../create_supplier_cheque/{supplierpayment.pk}')
            return redirect('supplier:supplier_list')
    context = {
        'supplierpaymentform': supplierpaymentform,
    }
    return render(request, 'payments/supplier/create_payment.html', context)


def create_supplier_cheque(request, pk):
    supplierpayment = BuyOrderPayment.objects.get(id=pk)
    supplierchequeform = SupplierChequeForm()
    if request.method == "POST":
        supplierchequeform = SupplierChequeForm(request.POST)
        if supplierchequeform.is_valid():
            suppliercheque = supplierchequeform.save(commit=False)
            suppliercheque.supplier = supplierpayment.supplier
            suppliercheque.supplierpayment = supplierpayment
            suppliercheque.save()
            return redirect("supplier:supplier_list")

    context = {
        "supplierchequeform": supplierchequeform
    }
    return render(request, 'payments/supplier/create_cheque.html', context)


def supplier_payment_list(request):
    supplierpayments = BuyOrderPayment.objects.all()
    context = {
        "supplierpayments": supplierpayments
    }
    return render(request, 'payments/supplier/payment_list.html', context)


def delete_supplier_payment(request, pk):
    buyorder_payment = get_object_or_404(BuyOrderPayment, id=pk)
    order = get_object_or_404(BuyOrder, id=buyorder_payment.order.id)
    if request.method == "POST":
        payment_amount = buyorder_payment.amount
        buyorder_payment.delete()
        # fix order values after deleting
        order.debt += payment_amount
        order.supplier.credit += payment_amount
        order.save()
        order.supplier.save()

        return redirect("payments:supplier_payment_list")

    context = {
        'buyorder_payment': buyorder_payment,
        'order': order,
    }
    return render(request, 'payments/supplier/delete_payment.html', context)


def delete_supplier_by_supplier_payment(request, pk):
    payment = get_object_or_404(BuyOrderPayment, id=pk)
    supplier = Supplier.objects.get(id=payment.supplier.id)
    orders = BuyOrder.objects.all().filter(supplier=supplier, confirmed=True).order_by('order_date')
    if request.method == "POST":
        total_payment_amount = payment.amount
        rest_amount = total_payment_amount
        for order in orders:

            if rest_amount > 0 and order.get_ttc() != order.debt:
                print("TTC =====>", order.get_ttc())
                print("DEBT =====>", order.debt)
                order_diff_amount = order.get_ttc() - order.debt
                # to reach zero difference between ttc and debt
                if total_payment_amount > order_diff_amount:
                    to_reach_zero = order_diff_amount
                else:
                    to_reach_zero = total_payment_amount

                # what rest after the operation
                rest_amount = total_payment_amount - order_diff_amount
                order.debt += to_reach_zero
                total_payment_amount = rest_amount
                # check order debt
                if order.debt > 0:
                    order.paid = False
                print("ORDER ::::>", order.id)
                print("TTC =====>", order.get_ttc())
                print("DEBT =====>", order.debt)
                order.save()

        # fix supplier credit
        supplier.credit += payment.amount
        supplier.save()
        # if payment is cheque
        if payment.pay_status == "Cheque":
            cheque = SupplierCheque.objects.get(buyorderpayment=payment)
            # delete cheque
            cheque.delete()
        # delete payment
        payment.delete()

        return redirect("supplier:supplier_detail", supplier.id)

    context = {
        'payment': payment,
        'supplier': supplier,
        'orders': orders,
    }
    return render(request, 'payments/supplier/delete_supplier_payment.html', context)


def create_service_payment(request, pk):
    provider = get_object_or_404(ServiceProvider, id=pk)
    servicepaymentform = ServicePaymentForm()
    if request.method == "POST":
        servicepaymentform = ServicePaymentForm(request.POST)
        if servicepaymentform.is_valid():
            # saving service payment
            servicepayment = servicepaymentform.save(commit=False)
            servicepayment.provider = provider
            servicepayment.save()
            # handling provider credit
            provider.credit -= servicepayment.amount
            provider.save()

            return redirect('payments:service_payment_list')

    context = {
        'servicepaymentform': servicepaymentform,
    }
    return render(request, "payments/service/create_payment.html", context)


def service_payment_list(request):
    serivcepayments = ServicePayment.objects.all()

    context = {
        'serivcepayments': serivcepayments,
    }
    return render(request, 'payments/service/payment_list.html', context)


def delete_service_payment(request, pk):
    payment = get_object_or_404(ServicePayment, id=pk)
    provider = get_object_or_404(ServiceProvider, id=payment.provider.id)
    if request.method == "POST":

        provider.credit += payment.amount
        provider.save()

        payment.delete()

        return redirect("services:provider_details", provider.id)

    context = {
        "payment": payment,
        "provider": provider,
    }
    return render(request, "payments/service/delete_payment.html", context)