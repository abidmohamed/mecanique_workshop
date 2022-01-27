import datetime
from datetime import date, datetime

from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import cache_page

# Create your views here.
from accounts.models import CurrentYear
from caisse.forms import TransactionForm, DateForm, PeriodForm, CategoryTransactionForm
from caisse.models import Caisse, CaisseHistory, Transaction, TransactionCategory
from payments.models import SellOrderPayment, BuyOrderPayment, ServicePayment


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
    current_year = CurrentYear.objects.all().filter()[:1].get().year
    transactions = category.items.filter(trans_date__year=current_year)
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
    if request.method == 'POST':
        transaction_form = TransactionForm(request.POST)
        if transaction_form.is_valid():
            transaction_form.save()

            return redirect('caisse:transaction_list')

    context = {'transaction_form': transaction_form}
    return render(request, 'caisse/add_transaction.html', context)


def transaction_list(request):
    dateform = DateForm()
    periodform = PeriodForm()
    # current year
    current_year = CurrentYear.objects.all().filter()[:1].get()

    transactions = Transaction.objects.filter(trans_date__year=current_year.year)

    # now time
    now = datetime.now()
    chosen_date = datetime.now()

    customerpayments = SellOrderPayment.objects.all().filter(pay_status='Cash', pay_date__year=current_year.year)
    supplierpayments = BuyOrderPayment.objects.all().filter(pay_status='Cash', pay_date__year=current_year.year)
    servicepayments = ServicePayment.objects.filter(pay_date__year=current_year.year)

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
        transactions = Transaction.objects.all().filter(
            Q(
                trans_date__gt=date(int(start_year), int(start_month), int(start_day)),
                trans_date__lt=date(int(end_year), int(end_month), int(end_day))
            )
            |
            Q(
                trans_date=date(int(end_year), int(end_month), int(end_day))
            )
        )
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

        )
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
        )

        servicepayments = ServicePayment.objects.all().filter(
            Q(
                pay_date__gt=date(int(start_year), int(start_month), int(start_day)),
                pay_date__lt=date(int(end_year), int(end_month), int(end_day))
            )
            |
            Q(
                pay_date=date(int(end_year), int(end_month), int(end_day))
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

    for customerpayment in customerpayments:
        total_per_period += customerpayment.amount
        income_per_period += customerpayment.amount
        total_customer_payments += customerpayment.amount

    for supplierpayment in supplierpayments:
        total_per_period -= supplierpayment.amount
        expense_per_period += supplierpayment.amount
        total_supplier_payments += supplierpayment.amount

    for servicepayment in servicepayments:
        total_per_period -= servicepayment.amount
        expense_per_period += servicepayment.amount
        total_service_payments += servicepayment.amount

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
    # Search request by date===>
    # if request.method == 'POST':
    #     # dateform = request.POST
    #     print('POST applied')
    #     alldata = request.POST
    #     print(alldata)
    #     chosen_date = alldata.get("date")
    #     chosen_date = chosen_date.split("-", 1)
    #     chosen_start_date = chosen_date[0]
    #     chosen_end_date = chosen_date[1]
    #
    #     chosen_start_date = chosen_start_date.split("/", 2)
    #     start_month = chosen_start_date[0]
    #     start_year = chosen_start_date[2]
    #     start_day = chosen_start_date[1]
    #     # Remove white spaces
    #     start_year = ''.join(start_year.split())
    #     start_month = ''.join(start_month.split())
    #     start_day = ''.join(start_day.split())
    #
    #     chosen_end_date = chosen_end_date.split("/", 2)
    #     end_month = chosen_end_date[0]
    #     end_year = chosen_end_date[2]
    #     end_day = chosen_end_date[1]
    #     # Remove white spaces
    #     end_year = ''.join(end_year.split())
    #     end_month = ''.join(end_month.split())
    #     end_day = ''.join(end_day.split())

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


def delete_transaction(request, pk):
    transaction = Transaction.objects.get(id=pk)
    context = {'transaction': transaction}
    if request.method == 'POST':
        caisse = Caisse.objects.all().filter()[:1].get()
        caisse_history = CaisseHistory()
        caisse_history.caisse_value = caisse.caisse_value

        caisse_history.save()

        if transaction.Transaction_type == 'Income':
            caisse.caisse_value = caisse.caisse_value - transaction.amount

        elif transaction.Transaction_type == 'Expense':
            caisse.caisse_value = caisse.caisse_value + transaction.amount

        caisse.save()
        transaction.delete()
        return redirect('caisse:transaction_list')
    return render(request, 'caisse/transaction_delete.html', context)
