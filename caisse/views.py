from django.shortcuts import render, redirect

# Create your views here.
from caisse.forms import TransactionForm, DateForm
from caisse.models import Caisse, CaisseHistory, Transaction


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
    transactions = Transaction.objects.all()
    # Search request by date===>
    if request.method == 'POST':
        # dateform = request.POST
        print('POST applied')
        alldata = request.POST
        print(alldata)
        chosen_date = alldata.get("date")
        month = chosen_date.split("-", 2)
        year = chosen_date.split("-", 1)
        print(chosen_date.split("-", 1))
        print(chosen_date.split("-", 2))
        print(year[0])
        print(month[1])
        transactions = Transaction.objects.all().filter(date_created__year=year[0],
                                                        date_created__month=month[1])
    context = {
        "transactions": transactions,
        "dateform": dateform,
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
            caisse.caisse_value = caisse.caisse_value + transaction.amount

        elif transaction.Transaction_type == 'Expense':
            caisse.caisse_value = caisse.caisse_value - transaction.amount

        caisse.save()
        transaction.delete()
        return redirect('caisse:transaction_list')
    return render(request, 'caisse/transaction_delete.html', context)
