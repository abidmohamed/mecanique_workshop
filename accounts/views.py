from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User, Group, Permission

from django.shortcuts import render, redirect
import calendar
from datetime import date, datetime
from datetime import timedelta
# Create your views here.
from django.utils.safestring import mark_safe

from accounts.decorators import unauthneticated_user
from bank.models import BankTransaction
from buyorder.models import BuyOrder
from caisse.models import Caisse, Transaction
from customer.models import Customer
from payments.models import SellOrderPayment, BuyOrderPayment, ServicePayment
from product.models import Product
from rdv.models import Rdv

# Calendar Views & functions
from rdv.utils import Calendar
from sellorder.models import Order
from stock.models import StockProduct
from supplier.models import Supplier


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month


# Login & Log Out
@unauthneticated_user
def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        print('USER LOGED ------->', user)
        if user is not None:
            login(request, user)
            return redirect('accounts:home')
        else:
            messages.info(request, 'Username Or Password Is not correct')
    context = {}
    return render(request, 'login/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('accounts:login')


# Dashboard
def home(request):
    # now time
    now = datetime.now()
    # Calendar
    calendar_date = get_date(request.GET.get('month', None))
    none_html_calendar = Calendar(calendar_date.year, calendar_date.month)
    html_calendar = none_html_calendar.formatmonth(withyear=True)

    # sellorders = Order.objects.all().filter(confirmed=True)  # .filter(created__year=now.year, created__month=now.month)
    # buyorders = BuyOrder.objects.all()  # can be filtred by year & month
    # Today order
    today_sellorders = Order.objects.all().filter(created__year=now.year, created__month=now.month,
                                                  created__day=now.day, confirmed=True)
    payed_today_sellorders = Order.objects.all().filter(created__year=now.year, created__month=now.month,
                                                        created__day=now.day, confirmed=True, paid=True)

    # customers + suppliers all objects
    allcustomers = Customer.objects.all()
    allsuppliers = Supplier.objects.all()
    # Caisse
    transactions = Transaction.objects.all()
    customerpayments = SellOrderPayment.objects.all()
    supplierpayments = BuyOrderPayment.objects.all()
    servicepayments = ServicePayment.objects.all()
    # today Caisse
    today_transactions = Transaction.objects.all().filter(trans_date__year=now.year, trans_date__month=now.month,
                                                          trans_date__day=now.day)
    today_customerpayments = SellOrderPayment.objects.all().filter(pay_date__year=now.year, pay_date__month=now.month,
                                                                   pay_date__day=now.day)
    today_supplierpayments = BuyOrderPayment.objects.all().filter(pay_date__year=now.year, pay_date__month=now.month,
                                                                  pay_date__day=now.day)

    today_servicepayments = ServicePayment.objects.all().filter(pay_date__year=now.year, pay_date__month=now.month,
                                                                pay_date__day=now.day)

    # caisse = Caisse.objects.all().filter()[:1].get().caisse_value
    today_caisse = 0
    caisse = 0
    # Bank
    bank = 0
    bank_transactions = BankTransaction.objects.all()
    # Customer
    customers = Customer.objects.all().count()
    # Supplier
    suppliers = Supplier.objects.all().count()
    # Total customers Debt
    totaldebt = 0
    for customer in allcustomers:
        totaldebt += customer.debt

    # Total suppliers Credit
    totalcredit = 0
    for supplier in allsuppliers:
        totalcredit += supplier.credit

    # BuyOrder
    buyorder_number = BuyOrder.objects.all().count()
    # SellOrder
    sellorder_number = Order.objects.all().filter(confirmed=True).count()
    # sell orders total
    totalsellorders = 0
    totalbuyorders = 0
    # for order in Order.objects.all().filter(confirmed=True):
    #     totalsellorders += order.get_ttc()
    # Buy orders total
    # for order in buyorders:
    #    totalbuyorders += order.get_total_cost()

    # Sell Orders today total
    totaltodaypanne = 0
    totaltodaypiece = 0
    for order in today_sellorders:
        totaltodaypanne += order.get_total_panne()
        totaltodaypiece += order.get_total_cost()

    # Sell Orders today total
    payed_totaltodaypanne = 0
    payed_totaltodaypiece = 0
    today_caisse = 0
    for order in payed_today_sellorders:
        payed_totaltodaypanne += order.get_total_panne()
        payed_totaltodaypiece += order.get_total_cost()

    # Stock Qt Alert
    stockproductsalertcount = 0
    products = Product.objects.all()
    for product in products:
        stockproductsalertcount = StockProduct.objects.all().filter(quantity__lte=product.alert_quantity).count()

    if not stockproductsalertcount:
        stockproductsalertcount = 0

    # Total Caisse Value
    for transaction in transactions:
        if transaction.Transaction_type == "Income":
            caisse += transaction.amount
        else:
            caisse -= transaction.amount

    for customerpayment in customerpayments:
        if customerpayment.pay_status == "Cash":
            caisse += customerpayment.amount

    for supplierpayment in supplierpayments:
        if supplierpayment.pay_status == "Cash":
            caisse -= supplierpayment.amount

    for servicepayment in servicepayments:
        caisse -= servicepayment.amount

    # Today Caisse
    for transaction in today_transactions:
        if transaction.Transaction_type == "Income":
            today_caisse += transaction.amount
        else:
            today_caisse -= transaction.amount

    for customerpayment in today_customerpayments:
        if customerpayment.pay_status == "Cash":
            today_caisse += customerpayment.amount

    for supplierpayment in today_supplierpayments:
        if supplierpayment.pay_status == "Cash":
            today_caisse -= supplierpayment.amount

    for servicepayment in today_servicepayments:
        today_caisse -= servicepayment.amount

    # Total Bank Value
    for transaction in bank_transactions:
        if transaction.Transaction_type == "Income":
            bank += transaction.amount
        else:
            bank -= transaction.amount

    # Cheque Payment
    for customerpayment in customerpayments:
        if customerpayment.pay_status == "Cheque":
            bank += customerpayment.amount

    for supplierpayment in supplierpayments:
        if supplierpayment.pay_status == "Cheque":
            bank -= supplierpayment.amount

    # Verement Payment
    for customerpayment in customerpayments:
        if customerpayment.pay_status == "Verement":
            bank += customerpayment.amount

    for supplierpayment in supplierpayments:
        if supplierpayment.pay_status == "Verement":
            bank -= supplierpayment.amount

    context = {
        'calendar': mark_safe(html_calendar),
        'prev_month': prev_month(calendar_date),
        'next_month': next_month(calendar_date),
        'caisse': caisse, 'customers': customers,
        'buyorder_number': buyorder_number, 'sellorder_number': sellorder_number,
        'totalsellorders': totalsellorders, 'totalbuyorders': totalbuyorders,
        'stockproductsalertcount': stockproductsalertcount, 'suppliers': suppliers,
        'totaldebt': totaldebt, 'totalcredit': totalcredit,
        'totaltodaypanne': totaltodaypanne, 'totaltodaypiece': totaltodaypiece,
        'bank': bank, 'payed_totaltodaypanne': payed_totaltodaypanne,
        'payed_totaltodaypiece': payed_totaltodaypiece,
        'today_caisse': today_caisse,
    }
    return render(request, 'dashboard.html', context)
