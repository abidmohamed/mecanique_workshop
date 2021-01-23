from django.shortcuts import render, redirect

# Create your views here.
from customer.models import Customer
from payments.forms import CustomerChequeForm, SupplierPaymentForm, SupplierChequeForm, CustomerPaymentForm
from payments.models import CustomerPayment, SupplierPayment
from supplier.models import Supplier


def create_customer_payment(request, pk):
    customer = Customer.objects.get(id=pk)
    customerpaymentform = CustomerPaymentForm()
    if request.method == "POST":
        customerpaymentform = CustomerPaymentForm(request.POST)
        if customerpaymentform.is_valid():
            customerpayment = customerpaymentform.save(commit=False)
            print(customerpayment.amount)
            customerpayment.customer = customer
            customerpayment.save()
            customer.debt -= customerpayment.amount
            customer.save()
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
    customerpayment = CustomerPayment.objects.get(id=pk)
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
    customerpayments = CustomerPayment.objects.all()
    context = {
        "customerpayments": customerpayments
    }
    return render(request, 'payments/customer/payment_list.html', context)


def create_supplier_payment(request, pk):
    supplier = Supplier.objects.get(id=pk)
    supplierpaymentform = SupplierPaymentForm()
    if request.method == "POST":
        supplierpaymentform = SupplierPaymentForm(request.POST)
        if supplierpaymentform.is_valid():
            supplierpayment = supplierpaymentform.save(commit=False)
            print(supplierpayment.amount)
            supplierpayment.supplier = supplier
            supplierpayment.save()
            supplier.credit -= supplierpayment.amount
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
    supplierpayment = SupplierPayment.objects.get(id=pk)
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
    supplierpayments = SupplierPayment.objects.all()
    context = {
        "supplierpayments": supplierpayments
    }
    return render(request, 'payments/supplier/payment_list.html', context)
