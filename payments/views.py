from django.shortcuts import render, redirect

# Create your views here.
from buyorder.models import BuyOrder
from caisse.models import Caisse
from customer.models import Customer
from payments.forms import CustomerChequeForm, SupplierPaymentForm, SupplierChequeForm, CustomerPaymentForm
from payments.models import SellOrderPayment, BuyOrderPayment
from sellorder.models import Order
from supplier.models import Supplier


# Sell Order Payment is Customer Payment
def create_customer_payment(request, pk):
    # customer = Customer.objects.get(id=pk)
    order = Order.objects.get(id=pk)
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
                order.debt = order.get_total_cost()
            print(order.debt)
            order.debt -= customerpayment.amount
            # print(order.debt)
            if order.debt == 0:
                order.paid = True
            order.save()
            order.customer.debt -= customerpayment.amount
            caisse = Caisse.objects.all().filter()[:1].get()
            caisse.caisse_value += customerpayment.amount
            caisse.save()
            order.customer.save()
            # TODO: Uncomment this one
            # customerpayment.user = request.user.id
            if customerpayment.pay_status == "Cheque":
                return redirect(f'../create_customer_cheque/{customerpayment.pk}')
            return redirect('customer:customer_list')
    context = {
        'customerpaymentform': customerpaymentform,
    }
    return render(request, 'payments/customer/create_payment.html', context)


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
