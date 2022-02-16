from django.shortcuts import render, get_object_or_404
from django.db.models import Q
# Create your views here.
from django.shortcuts import render, redirect

from accounts.models import CurrentYear
from buyorder.models import BuyOrder
from payments.models import BuyOrderPayment
from supplier.forms import SupplierForm
from supplier.models import Supplier


def add_supplier(request):
    supplier_form = SupplierForm()

    if request.method == 'POST':
        supplier_form = SupplierForm(request.POST)

        if supplier_form.is_valid():
            supplier_form.save()

            return redirect('supplier:supplier_list')

    context = {
            'supplier_form': supplier_form
    }

    return render(request, 'supplier/add_supplier.html', context)


def supplier_list(request):
    current_year = CurrentYear.objects.all().filter()[:1].get()
    suppliers = Supplier.objects.all()
    context = {
        'suppliers': suppliers,
        'current_year': current_year,
    }
    return render(request, 'supplier/list_supplier.html', context)


def buyorder_supplier_list(request):
    suppliers = Supplier.objects.all()
    context = {
        'suppliers': suppliers
    }
    return render(request, 'supplier/buyorder_list_supplier.html', context)


def update_supplier(request, pk):
    supplier = Supplier.objects.get(id=pk)
    supplier_form = SupplierForm(instance=supplier)

    if request.method == 'POST':
        supplier_form = SupplierForm(request.POST, instance=supplier)
        if supplier_form.is_valid():
            supplier_form.save()

            return redirect('supplier:supplier_list')

    context = {
        'supplier_form': supplier_form
    }
    return render(request, 'supplier/add_supplier.html', context)


def delete_supplier(request, pk):
    supplier = Supplier.objects.get(id=pk)
    context = {
        'supplier': supplier
    }
    if request.method == 'POST':
        supplier.delete()
        return redirect('supplier:supplier_list')
    return render(request, 'supplier/delete_supplier.html', context)


def supplier_detail(request, pk):
    supplier = get_object_or_404(Supplier, id=pk)
    current_year = CurrentYear.objects.all().filter()[:1].get()
    orders = BuyOrder.objects.all().filter(
        Q(
            order_date__year=current_year.year
        ) |
        Q(
            order_date__year=None
        ),
        supplier=supplier, confirmed=True,
    )
    unconfirmed_orders = BuyOrder.objects.all().filter(
        Q(
            order_date__year=current_year.year
        ) |
        Q(
            order_date__year=None
        ),
        supplier=supplier, confirmed=False,
        )
    payments = BuyOrderPayment.objects.all().filter(supplier=supplier, pay_date__year=current_year.year)
    context = {
        'supplier': supplier,
        'orders': orders,
        'unconfirmed_orders': unconfirmed_orders,
        'current_year': current_year,
        'payments': payments,
    }
    return render(request, 'supplier/detail.html', context)