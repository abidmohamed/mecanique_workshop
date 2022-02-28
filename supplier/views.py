from datetime import date, datetime

from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Sum
# Create your views here.
from django.shortcuts import render, redirect

from accounts.models import CurrentYear
from buyorder.models import BuyOrder
from caisse.forms import DateForm
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

    # TimeField related
    # current year
    current_year = CurrentYear.objects.all().filter()[:1].get()
    dateform = DateForm()
    # now time
    chosen_date = datetime.now()
    # total order
    total_order = 0
    orders = BuyOrder.objects.all().filter(
        Q(
            order_date__year=current_year.year
        ) |
        Q(
            order_date=None
        ),
        supplier=supplier, confirmed=True,
    )
    # total order credit
    total_credit = orders.aggregate(Sum('debt'))['debt__sum']
    # Total
    for order in orders:
        total_order += order.get_ttc()

    unconfirmed_orders = BuyOrder.objects.all().filter(
        Q(
            order_date__year=current_year.year
        ) |
        Q(
            order_date__year=None
        ),
        supplier=supplier, confirmed=False,
        )
    # Payments
    payments = BuyOrderPayment.objects.all().filter(supplier=supplier, pay_date__year=current_year.year)
    # searching by date
    if request.method == 'POST':
        alldata = request.POST

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

        # total order
        total_order = 0
        orders = BuyOrder.objects.all().filter(
            Q(
                order_date__gt=date(int(start_year), int(start_month),
                                    int(start_day)),
                order_date__lt=date(int(end_year), int(end_month), int(end_day))
            )
            |
            Q(
                order_date=date(int(end_year), int(end_month), int(end_day))
            )
            |
            Q(
                order_date__year=None
            ),
            supplier=supplier, confirmed=True,
        )
        # total order credit
        total_credit = orders.aggregate(Sum('debt'))['debt__sum']
        # Total
        for order in orders:
            total_order += order.get_ttc()

        unconfirmed_orders = BuyOrder.objects.all().filter(
            Q(
                order_date__gt=date(int(start_year), int(start_month),
                                    int(start_day)),
                order_date__lt=date(int(end_year), int(end_month), int(end_day))

            )
            |
            Q(
                order_date=date(int(end_year), int(end_month), int(end_day))
            )
            |
            Q(
                order_date__year=None
            ),
            supplier=supplier, confirmed=False,
        )
        # Payments
        payments = BuyOrderPayment.objects.all().filter(
            Q(
                pay_date__gt=date(int(start_year), int(start_month),
                                  int(start_day)),
                pay_date__lt=date(int(end_year), int(end_month), int(end_day))
            )
            |
            Q(
                pay_date=date(int(end_year), int(end_month), int(end_day))
            ),
            supplier=supplier
        )

    context = {
        'supplier': supplier,
        'orders': orders,
        'unconfirmed_orders': unconfirmed_orders,
        'current_year': current_year,
        'payments': payments,
        'total_order': total_order,
        'total_credit': total_credit,
        "dateform": dateform,
        'chosen_date': chosen_date,
    }
    return render(request, 'supplier/detail.html', context)