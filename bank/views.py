from datetime import date

from django.db.models import Q
from django.shortcuts import render, redirect
# Create your views here.
from accounts.models import CurrentYear
from bank.forms import BankTransactionForm
from bank.models import BankTransaction
from caisse.forms import DateForm, PeriodForm
from payments.models import SellOrderPayment, BuyOrderPayment


def create_transaction(request):
    transaction_form = BankTransactionForm()
    if request.method == 'POST':
        transaction_form = BankTransactionForm(request.POST)
        if transaction_form.is_valid():
            transaction_form.save()
            return redirect('bank:transaction_list')

    context = {
        'transaction_form': transaction_form
    }
    return render(request, 'bank/add_transaction.html', context)


def transaction_list(request):
    dateform = DateForm()
    periodform = PeriodForm()
    # current year
    current_year = CurrentYear.objects.all().filter()[:1].get()

    transactions = BankTransaction.objects.filter(trans_date__year=current_year.year).order_by('trans_date')

    customerpayments = SellOrderPayment.objects.all().filter(Q(pay_status='Cheque') | Q(pay_status='Verement'),
                                                             pay_date__year=current_year.year).order_by('pay_date')
    supplierpayments = BuyOrderPayment.objects.all().filter(Q(pay_status='Cheque') | Q(pay_status='Verement'),
                                                            pay_date__year=current_year.year).order_by('pay_date')
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

        # Date Submit ----------date_created
        transactions = BankTransaction.objects.all().filter(
            trans_date__gte=date(int(start_year), int(start_month), int(start_day)),
            trans_date__lte=date(int(end_year), int(end_month), int(end_day)),
        ).order_by('trans_date')

        customerpayments = SellOrderPayment.objects.all().filter(
            Q(pay_status='Cheque') | Q(pay_status='Verement'),
            pay_date__gte=date(int(start_year), int(start_month), int(start_day)),
            pay_date__lte=date(int(end_year), int(end_month), int(end_day)),
        ).order_by('pay_date')

        supplierpayments = BuyOrderPayment.objects.all().filter(
            Q(pay_status='Cheque') | Q(pay_status='Verement'),
            pay_date__gte=date(int(start_year), int(start_month), int(start_day)),
            pay_date__lte=date(int(end_year), int(end_month), int(end_day)),
        ).order_by('pay_date')

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

    return render(request, "bank/transaction_list.html", context)


def delete_transaction(request, pk):
    transaction = BankTransaction.objects.get(id=pk)
    context = {'transaction': transaction}
    if request.method == 'POST':
        transaction.delete()
        return redirect('bank:transaction_list')
    return render(request, 'bank/transaction_delete.html', context)
