from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.shortcuts import render, redirect

from buyorder.models import BuyOrder
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
    suppliers = Supplier.objects.all()
    context = {
        'suppliers': suppliers
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
    orders = BuyOrder.objects.all().filter(supplier=supplier, confirmed=True)
    context = {
        'supplier': supplier,
        'orders': orders,
    }
    return render(request, 'supplier/detail.html', context)