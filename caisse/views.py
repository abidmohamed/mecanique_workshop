import datetime
import decimal
from datetime import date, datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q, Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import cache_page

# Create your views here.
from accounts.models import CurrentYear
from caisse.filters import TransactionFilter
from caisse.forms import TransactionForm, DateForm, PeriodForm, CategoryTransactionForm
from caisse.models import Caisse, CaisseHistory, Transaction, TransactionCategory
from customer.models import Enterprise
from payments.models import SellOrderPayment, BuyOrderPayment, ServicePayment
from sellorder.models import Order


def create_transaction_category(request):
    transaction_form = CategoryTransactionForm()
    if request.method == 'POST':
        transaction_form = CategoryTransactionForm(request.POST)
        if transaction_form.is_valid():
            transaction_form.save()

            return redirect('caisse:transaction_category_list')

    context = {'transaction_form': transaction_form}
    return render(request, 'caisse/add_transaction.html', context)


def transaction_category_list(request):
    categories = TransactionCategory.objects.all()

    context = {
        'categories': categories
    }
    return render(request, 'category/list.html', context)


def transaction_category_details(request, pk):
    category = get_object_or_404(TransactionCategory, id=pk)
    # current year
    if CurrentYear.objects.all().filter(user=request.user):
        current_year = CurrentYear.objects.all().filter(user=request.user)[:1].get()
    else:
        current_year = CurrentYear.objects.create(year=2022, user=request.user)
    transactions = category.items.filter(trans_date__year=current_year.year)
    # date forms
    dateform = DateForm()
    periodform = PeriodForm()
    # now time
    now = datetime.now()
    chosen_date = datetime.now()
    # values
    total_per_period = 0
    income_per_period = 0
    expense_per_period = 0
    total_transaction_payments = 0
    # Search request by date===>
    if request.method == 'POST':
        alldata = request.POST
        # extract date
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

        # Date Submit ----------trans_date
        transactions = category.items.filter(
            Q(
                trans_date__gt=date(int(start_year), int(start_month), int(start_day)),
                trans_date__lt=date(int(end_year), int(end_month), int(end_day))
            )
            |
            Q(
                trans_date=date(int(end_year), int(end_month), int(end_day))
            )
        )

    for transaction in transactions:
        if transaction.Transaction_type == "Income":
            total_per_period += transaction.amount
            income_per_period += transaction.amount
            total_transaction_payments += transaction.amount
        else:
            total_per_period -= transaction.amount
            expense_per_period += transaction.amount
            total_transaction_payments -= transaction.amount

    context = {
        'transactions': transactions,
        'total_per_period': total_per_period,
        'income_per_period': income_per_period,
        'expense_per_period': expense_per_period,
        'total_transaction_payments': total_transaction_payments,
        'current_year': current_year,
        "dateform": dateform,
        "periodform": periodform,
        "chosen_date": chosen_date,
    }

    return render(request, 'category/details.html', context)


def create_transaction(request):
    transaction_form = TransactionForm()
    if request.method == 'POST':
        transaction_form = TransactionForm(request.POST)
        if transaction_form.is_valid():
            transaction = transaction_form.save(commit=False)
            caisse = Caisse.objects.all().filter()[:1].get()
            caisse_history = CaisseHistory()
            caisse_history.caisse_value = caisse.caisse_value

            caisse_history.save()

            if transaction.Transaction_type == 'Income':
                caisse.caisse_value = caisse.caisse_value + transaction.amount

            elif transaction.Transaction_type == 'Expense':
                caisse.caisse_value = caisse.caisse_value - transaction.amount

            caisse.save()
            transaction.save()
            return redirect('caisse:transaction_list')

    context = {'transaction_form': transaction_form}
    return render(request, 'caisse/add_transaction.html', context)


def update_transaction(request, pk):
    transaction = get_object_or_404(Transaction, id=pk)
    transaction_form = TransactionForm(instance=transaction)
    transaction_date = transaction.trans_date
    if request.method == 'POST':
        transaction_form = TransactionForm(request.POST, instance=transaction)
        if transaction_form.is_valid():
            transaction_form.save()

            return redirect('caisse:transaction_list')

    context = {
        'transaction_form': transaction_form,
        'transaction_date': transaction_date,
    }
    return render(request, 'caisse/add_transaction.html', context)


def transaction_list(request):
    dateform = DateForm()
    periodform = PeriodForm()
    # now time
    now = datetime.now()
    chosen_date = datetime.now()
    # current year
    if CurrentYear.objects.all().filter(user=request.user):
        current_year = CurrentYear.objects.all().filter(user=request.user)[:1].get()
    else:
        current_year = CurrentYear.objects.create(year=2022, user=request.user)
    # Orders
    yearly_sellorders = Order.objects.all().filter(order_date__year=current_year.year, confirmed=True)
    paid_daily_sellorders = Order.objects.all().filter(order_date__year=current_year.year, order_date__day=now.day, confirmed=True, paid=True)
    # transaction
    in_transaction = Transaction.objects.filter(Transaction_type='Income',
                                                trans_date__year=current_year.year).aggregate(Sum('amount'))
    out_transaction = Transaction.objects.filter(Transaction_type='Expense',
                                                 trans_date__year=current_year.year).aggregate(Sum('amount'))
    # print(in_transaction['amount__sum'])
    transactions = 0
    if in_transaction['amount__sum']:
        transactions += in_transaction['amount__sum']
    if out_transaction['amount__sum']:
        transactions -= out_transaction['amount__sum']
    # transactions = Transaction.objects.filter(trans_date__year=current_year.year)

    # Payments
    customerpayments = SellOrderPayment.objects.all().filter(pay_status='Cash',
                                                             pay_date__year=current_year.year).aggregate(Sum('amount'))
    supplierpayments = BuyOrderPayment.objects.all().filter(pay_status='Cash',
                                                            pay_date__year=current_year.year).aggregate(Sum('amount'))
    servicepayments = ServicePayment.objects.filter(pay_date__year=current_year.year).aggregate(Sum('amount'))

    total_customer_payments = 0
    total_supplier_payments = 0
    total_service_payments = 0
    total_transaction_payments = 0

    total_per_period = 0
    income_per_period = 0
    expense_per_period = 0
    # Search request by date===>
    if request.method == 'POST':
        # dateform = request.POST
        print('POST applied')
        alldata = request.POST
        print(alldata)
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

        # Date Submit ----------trans_date
        # Transactions

        # transaction
        in_transaction = Transaction.objects.filter(
            Q(
                trans_date__gt=date(int(start_year), int(start_month), int(start_day)),
                trans_date__lt=date(int(end_year), int(end_month), int(end_day))
            )
            |
            Q(
                trans_date=date(int(end_year), int(end_month), int(end_day))
            ),
            Transaction_type='Income'
        ).aggregate(Sum('amount'))

        out_transaction = Transaction.objects.filter(
            Q(
                trans_date__gt=date(int(start_year), int(start_month), int(start_day)),
                trans_date__lt=date(int(end_year), int(end_month), int(end_day))
            )
            |
            Q(
                trans_date=date(int(end_year), int(end_month), int(end_day))
            ),
            Transaction_type='Expense'
        ).aggregate(Sum('amount'))
        # print(in_transaction['amount__sum'])
        transactions = 0
        if in_transaction['amount__sum']:
            transactions += in_transaction['amount__sum']
        if out_transaction['amount__sum']:
            transactions -= out_transaction['amount__sum']

        # Customer Payments
        customerpayments = SellOrderPayment.objects.all().filter(
            Q(
                pay_date__gt=date(int(start_year), int(start_month), int(start_day)),
                pay_date__lt=date(int(end_year), int(end_month), int(end_day))
            )
            |
            Q(
                pay_date=date(int(end_year), int(end_month), int(end_day))
            )
            ,
            pay_status='Cash',

        ).aggregate(Sum('amount'))
        supplierpayments = BuyOrderPayment.objects.all().filter(
            Q(
                pay_date__gt=date(int(start_year), int(start_month), int(start_day)),
                pay_date__lt=date(int(end_year), int(end_month), int(end_day))
            )
            |
            Q(
                pay_date=date(int(end_year), int(end_month), int(end_day))
            )
            ,
            pay_status='Cash',
        ).aggregate(Sum('amount'))

        servicepayments = ServicePayment.objects.all().filter(
            Q(
                pay_date__gt=date(int(start_year), int(start_month), int(start_day)),
                pay_date__lt=date(int(end_year), int(end_month), int(end_day))
            )
            |
            Q(
                pay_date=date(int(end_year), int(end_month), int(end_day))
            )
        ).aggregate(Sum('amount'))

        yearly_sellorders = Order.objects.all().filter(
            Q(
                order_date__gt=date(int(start_year), int(start_month), int(start_day)),
                order_date__lt=date(int(end_year), int(end_month), int(end_day))
            )
            |
            Q(
                order_date=date(int(end_year), int(end_month), int(end_day))
            ),
            confirmed=True
        )

        paid_daily_sellorders = Order.objects.all().filter(
            Q(
                order_date__gt=date(int(start_year), int(start_month), int(start_day)),
                order_date__lt=date(int(end_year), int(end_month), int(end_day))
            )
            |
            Q(
                order_date=date(int(end_year), int(end_month), int(end_day))
            ),
            confirmed=True, paid=True
        )


    # checking variables
    if customerpayments is None:
        customerpayments = 0
    if supplierpayments is None:
        supplierpayments = 0
    if transactions is None:
        transactions = 0
    if servicepayments is None:
        servicepayments = 0

    # Transactions
    # # ADD
    total_per_period += in_transaction['amount__sum']
    income_per_period += in_transaction['amount__sum']
    total_transaction_payments += in_transaction['amount__sum']
    # # SUB
    total_per_period -= out_transaction['amount__sum']
    expense_per_period += out_transaction['amount__sum']
    total_transaction_payments -= out_transaction['amount__sum']

    # Customer Payments
    customerpayments = customerpayments['amount__sum']
    total_per_period += customerpayments
    income_per_period += customerpayments
    total_customer_payments += customerpayments
    # Supplier Payments
    supplierpayments = supplierpayments['amount__sum']
    total_per_period -= supplierpayments
    expense_per_period += supplierpayments
    total_supplier_payments += supplierpayments
    # Service Payments
    servicepayments = servicepayments['amount__sum']
    total_per_period -= servicepayments
    expense_per_period += servicepayments
    total_service_payments += servicepayments

    # Sell Orders Pannes & Pieces
    totaltodaypanne = 0
    totaltodaypiece = 0
    chief_percentage = 0
    for order in yearly_sellorders:
        totaltodaypanne += order.get_total_panne()
        totaltodaypiece += order.get_total_cost()
        # calculate workshop chief 10%
        # get customer
        order_customer = order.customer
        # check if the customer enterprise 5% else 10%
        if Enterprise.objects.filter(customer=order_customer):
            chief_percentage += decimal.Decimal(order.get_total_panne() * 5) / decimal.Decimal(100)
        else:
            chief_percentage += decimal.Decimal(order.get_total_panne() * 10) / decimal.Decimal(100)

    paid_totaltodaypanne = 0
    paid_totaltodaypiece = 0
    paid_chief_percentage = 0
    for order in paid_daily_sellorders:
        paid_totaltodaypanne += order.get_total_panne()
        paid_totaltodaypiece += order.get_total_cost()
        # calculate workshop chief 10%
        # get customer
        order_customer = order.customer
        # check if the customer enterprise 5% else 10%
        if Enterprise.objects.filter(customer=order_customer):
            paid_chief_percentage += decimal.Decimal(order.get_total_panne() * 5) / decimal.Decimal(100)
        else:
            paid_chief_percentage += decimal.Decimal(order.get_total_panne() * 10) / decimal.Decimal(100)

    context = {
        "transactions": transactions,

        "dateform": dateform,
        "periodform": periodform,
        "chosen_date": chosen_date,

        "customerpayments": customerpayments,
        "supplierpayments": supplierpayments,
        'servicepayments': servicepayments,

        "total_per_period": total_per_period,
        "income_per_period": income_per_period,
        "expense_per_period": expense_per_period,

        'total_customer_payments': total_customer_payments,
        'total_supplier_payments': total_supplier_payments,
        'total_service_payments': total_service_payments,
        'total_transaction_payments': total_transaction_payments,

        'totaltodaypanne': totaltodaypanne,
        'totaltodaypiece': totaltodaypiece,
        'chief_percentage': chief_percentage,

        'paid_totaltodaypanne': paid_totaltodaypanne,
        'paid_totaltodaypiece': paid_totaltodaypiece,
        'paid_chief_percentage': paid_chief_percentage,

        'current_year': current_year,
    }

    return render(request, "caisse/transaction_list.html", context)


def today_transaction_list(request):
    dateform = DateForm()
    periodform = PeriodForm()
    # now time
    now = datetime.now()
    transactions = Transaction.objects.all()

    customerpayments = SellOrderPayment.objects.all().filter(pay_status='Cash')
    supplierpayments = BuyOrderPayment.objects.all().filter(pay_status='Cash')
    total_per_period = 0
    income_per_period = 0
    expense_per_period = 0

    # Date Submit ----------date_created
    transactions = Transaction.objects.all().filter(
        trans_date=now
    )
    customerpayments = SellOrderPayment.objects.all().filter(
        pay_date=now
        ,
        pay_status='Cash',

    )
    supplierpayments = BuyOrderPayment.objects.all().filter(
        pay_date=now
        ,
        pay_status='Cash',
    )

    for transaction in transactions:
        if transaction.Transaction_type == "Income":
            total_per_period += transaction.amount
            income_per_period += transaction.amount
        else:
            total_per_period -= transaction.amount
            expense_per_period += transaction.amount

    for customerpayment in customerpayments:
        total_per_period += customerpayment.amount
        income_per_period += customerpayment.amount

    for supplierpayment in supplierpayments:
        total_per_period -= supplierpayment.amount
        expense_per_period += supplierpayment.amount

    context = {
        "transactions": transactions,
        "dateform": dateform,
        "periodform": periodform,
        "customerpayments": customerpayments,
        "supplierpayments": supplierpayments,
        "total_per_period": total_per_period,
        "income_per_period": income_per_period,
        "expense_per_period": expense_per_period,
    }

    return render(request, "caisse/transaction_list.html", context)


@login_required
def in_out_transaction_list(request):
    context = {}
    transactions_list = Transaction.objects.all().order_by('trans_date')

    myFilter = TransactionFilter(request.GET, queryset=transactions_list)

    # paginate after filtering
    transactions_list = myFilter.qs
    # Page
    page = request.GET.get('page', 1)
    # Number of customers in the page
    paginator = Paginator(transactions_list, 5)
    try:
        transactions = paginator.page(page)
    except PageNotAnInteger:
        transactions = paginator.page(1)
    except EmptyPage:
        transactions = paginator.page(paginator.num_pages)

    context['myFilter'] = myFilter

    context['transactions'] = transactions

    total = 0
    incomes = 0
    expenses = 0
    for transaction in transactions_list:
        if transaction.Transaction_type == "Income":
            total += transaction.amount
            incomes += transaction.amount
        else:
            total -= transaction.amount
            expenses += transaction.amount

    context['incomes'] = incomes
    context['total'] = total
    context['expenses'] = expenses

    # company = Settings.objects.all().filter()[:1].get()
    # context['company'] = company
    if request.method == 'GET':
        form = TransactionForm()
        context['form'] = form
        return render(request, 'transaction/list.html', context)

    if request.method == 'POST':
        form = TransactionForm(request.POST)

        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            messages.success(request, "New Value Added")

            return redirect('caisse:in_out_transaction_list')
        else:
            messages.error(request, 'Problem processing your request')
            return redirect('caisse:in_out_transaction_list')

    return render(request, 'transaction/list.html', context)


@login_required
def transaction_details(request, pk):
    context = {}
    try:
        transaction = Transaction.objects.get(id=pk)
    except:
        messages.error(request, 'Something went wrong')
        return redirect('caisse:in_out_transaction_list')

    context['transaction'] = transaction
    return render(request, 'transaction/details.html', context)


def transaction_update(request, pk):
    context = {}
    try:
        transaction = Transaction.objects.get(id=pk)
    except:
        messages.error(request, 'Something went wrong')
        return redirect('caisse:in_out_transaction_list')

    form = TransactionForm(instance=transaction)
    context['form'] = form
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            transaction_form = form.save(commit=False)
            transaction_form.save()

            return redirect('caisse:transaction_details', pk)

    return render(request, 'transaction/update.html', context)


def transaction_delete(request, pk):
    try:
        transaction = Transaction.objects.get(id=pk)
    except:
        messages.error(request, 'Something went wrong')
        return redirect('caisse:in_out_transaction_list')

    transaction.delete()

    return redirect('caisse:in_out_transaction_list')
