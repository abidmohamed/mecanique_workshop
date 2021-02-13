from django.shortcuts import render, redirect

# Create your views here.
from caisse.forms import TransactionForm
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
    transactions = Transaction.objects.all()
    context = {"transactions": transactions}

    return render(request, "caisse/transaction_list.html", context)
