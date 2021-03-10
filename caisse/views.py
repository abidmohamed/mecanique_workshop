from datetime import date

from django.shortcuts import render, redirect

# Create your views here.
from caisse.forms import TransactionForm, DateForm, PeriodForm
from caisse.models import Caisse, CaisseHistory, Transaction
from payments.models import SellOrderPayment, BuyOrderPayment


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


def transaction_list(request):
    dateform = DateForm()
    periodform = PeriodForm()
    transactions = Transaction.objects.all()

    customerpayments = SellOrderPayment.objects.all()
    supplierpayments = BuyOrderPayment.objects.all()
    total_per_period = 0
    # Search request by date===>
    if request.method == 'POST':
        # dateform = request.POST
        print('POST applied')
        alldata = request.POST
        print(alldata)
        chosen_start_date = alldata.get("start_date")
        chosen_end_date = alldata.get("end_date")
        start_month = chosen_start_date.split("-", 2)
        start_year = chosen_start_date.split("-", 1)
        start_day = chosen_start_date.split("-", 2)

        end_month = chosen_end_date.split("-", 2)
        end_year = chosen_end_date.split("-", 1)
        end_day = chosen_end_date.split("-", 2)
        # print(chosen_date.split("-", 1))
        # print(chosen_date.split("-", 3))
        # print(year[0])
        # print(day[2])
        # Date Submit ----------date_created
        transactions = Transaction.objects.all().filter(
            trans_date__gte=date(int(start_year[0]), int(start_month[1]), int(start_day[2])),
            trans_date__lte=date(int(end_year[0]), int(end_month[1]), int(end_day[2]))
        )
        customerpayments = SellOrderPayment.objects.all().filter(
            pay_date__gte=date(int(start_year[0]), int(start_month[1]), int(start_day[2])),
            pay_date__lte=date(int(end_year[0]), int(end_month[1]), int(end_day[2]))
        )
        supplierpayments = BuyOrderPayment.objects.all().filter(
            pay_date__gte=date(int(start_year[0]), int(start_month[1]), int(start_day[2])),
            pay_date__lte=date(int(end_year[0]), int(end_month[1]), int(end_day[2]))
        )

        for transaction in transactions:
            if transaction.Transaction_type == "Income":
                total_per_period += transaction.amount
            else:
                total_per_period -= transaction.amount

        for customerpayment in customerpayments:
            total_per_period += customerpayment.amount

        for supplierpayment in supplierpayments:
            total_per_period -= supplierpayment.amount

    context = {
        "transactions": transactions,
        "dateform": dateform,
        "periodform": periodform,
        "customerpayments": customerpayments,
        "supplierpayments": supplierpayments,
        "total_per_period": total_per_period,
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
