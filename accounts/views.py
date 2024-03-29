import decimal

from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group, Permission
from django.db.models import Sum, Q

from django.shortcuts import render, redirect, get_object_or_404
import calendar
from datetime import date, datetime
from datetime import timedelta
# Create your views here.
from django.utils.safestring import mark_safe

from accounts.decorators import unauthneticated_user
from accounts.forms import UserForm, CurrentYearForm
from accounts.models import CurrentYear
from bank.models import BankTransaction
from buyorder.models import BuyOrder
from caisse.models import Caisse, Transaction
from customer.models import Customer, Enterprise
from employee.models import Employee
from payments.models import SellOrderPayment, BuyOrderPayment, ServicePayment
from product.models import Product
from rdv.models import Rdv

# Calendar Views & functions
from rdv.utils import Calendar
from sellorder.models import Order
from services.models import ServiceProvider
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


# Add user
def add_user(request):
    user_form = UserForm()
    if request.method == 'POST':
        user_form = UserForm(request.POST)

        if user_form.is_valid():
            user = user_form.save()

            if Group.objects.all().filter(name='desk_helper'):
                group = Group.objects.get(name='desk_helper')
            else:
                group = Group.objects.create(name='desk_helper')

            user.groups.add(group)

            user.save()

            return redirect('accounts:users_list')

    context = {
        'user_form': user_form,
    }

    return render(request, 'user/add_user.html', context)


def update_user(request, pk):
    user = get_object_or_404(User, id=pk)
    user_form = UserForm(instance=user)
    groups = Group.objects.all()

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)

        if user_form.is_valid():
            user_form.save()

            return redirect("accounts:users_list")

    context = {
        'user_form': user_form,
        'groups': groups,
    }

    return render(request, 'user/update_user.html', context)


def users_list(request):
    users = User.objects.filter(is_superuser=False)
    context = {
        "users": users,
    }
    return render(request, "user/list_user.html", context)


# Dashboard
@login_required
def home(request):
    # now time
    now = datetime.now()
    # Calendar
    calendar_date = get_date(request.GET.get('month', None))
    none_html_calendar = Calendar(calendar_date.year, calendar_date.month)
    html_calendar = none_html_calendar.formatmonth(withyear=True)

    # Choosed Year
    if CurrentYear.objects.all().filter(user=request.user):
        current_year = CurrentYear.objects.all().filter(user=request.user)[:1].get()
    else:
        current_year = CurrentYear.objects.create(year=2022, user=request.user)

    # sellorders = Order.objects.all().filter(confirmed=True)  # .filter(created__year=now.year,
    # created__month=now.month) buyorders = BuyOrder.objects.all()  # can be filtred by year & month Today order
    today_sellorders = Order.objects.all().filter(order_date__year=current_year.year,
                                                  order_date__month=now.month,
                                                  order_date__day=now.day, confirmed=True)
    payed_today_sellorders = Order.objects.all().filter(order_date__year=current_year.year,
                                                        order_date__month=now.month,
                                                        order_date__day=now.day, confirmed=True, paid=True)

    total_salary = 0
    daily_salary = 0
    if Employee.objects.all():
        # Employees weekly salary
        total_salary_dict = Employee.objects.only("weekly_salary").aggregate(Sum("weekly_salary"))
        # get only the value
        total_salary = total_salary_dict['weekly_salary__sum']
        # daily total salary
        daily_salary = round(total_salary / 7, 2)

    # Service Providers
    providers = ServiceProvider.objects.filter(credit__gt=0)
    # customers + suppliers all objects
    allcustomers = Customer.objects.filter(debt__gt=0)
    allsuppliers = Supplier.objects.filter(credit__gt=0)

    # Top 5
    top_five_suppliers = Supplier.objects.filter(credit__gt=0).order_by('-credit')[:5]
    # print(top_five_suppliers)
    top_five_customer = Customer.objects.filter(debt__gt=0).order_by('-debt')[:5]
    # print(top_five_customer) # excluding my garage provider
    top_five_providers = ServiceProvider.objects.filter(credit__gt=0).order_by('-credit')[:5]
    # Caisse
    transactions = Transaction.objects.filter(trans_date__year=current_year.year)
    customerpayments = SellOrderPayment.objects.filter(pay_date__year=current_year.year)
    supplierpayments = BuyOrderPayment.objects.filter(pay_date__year=current_year.year)
    servicepayments = ServicePayment.objects.filter(pay_date__year=current_year.year)
    # today Caisse

    today_transactions = Transaction.objects.all().filter(trans_date__year=current_year.year,
                                                          trans_date__month=now.month,
                                                          trans_date__day=now.day)
    today_customerpayments = SellOrderPayment.objects.all().filter(pay_date__year=current_year.year,
                                                                   pay_date__month=now.month,
                                                                   pay_date__day=now.day)
    today_supplierpayments = BuyOrderPayment.objects.all().filter(pay_date__year=current_year.year,
                                                                  pay_date__month=now.month,
                                                                  pay_date__day=now.day)

    today_servicepayments = ServicePayment.objects.all().filter(pay_date__year=current_year.year,
                                                                pay_date__month=now.month,
                                                                pay_date__day=now.day)

    # caisse = Caisse.objects.all().filter()[:1].get().caisse_value
    today_caisse = 0
    caisse = 0
    # Bank
    bank = 0
    bank_transactions = BankTransaction.objects.filter(trans_date__year=current_year.year)
    # Customer
    #customers = Customer.objects.all().count()
    # Supplier
    #suppliers = Supplier.objects.all().count()
    # Total customers Debt
    totaldebt = 0
    for customer in allcustomers:
        totaldebt += customer.get_debt()

    # Total suppliers Credit
    totalcredit = 0
    for supplier in allsuppliers:
        totalcredit += supplier.get_credit()

    # total provider credit
    total_provider_credit = 0
    for provider in providers:
        total_provider_credit += provider.get_credit()

    # BuyOrder
    # buyorder_number = BuyOrder.objects.all().filter(created__year=current_year.year).count()
    # SellOrder
    # sellorder_number = Order.objects.all().filter(confirmed=True,created__year=current_year.year).count()
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
    chief_percentage = 0
    for order in today_sellorders:
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

    # Sell Orders today total
    payed_totaltodaypanne = 0
    payed_totaltodaypiece = 0
    today_caisse = 0
    for order in payed_today_sellorders:
        payed_totaltodaypanne += order.get_total_panne()
        payed_totaltodaypiece += order.get_total_cost()

    # Stock Qt Alert
    stockproductsalertcount = 0
    # products = Product.objects.all()
    for product in StockProduct.objects.all().filter(quantity__lte=10):
        stockproductsalertcount = StockProduct.objects.all().filter(
            quantity__lte=product.product.alert_quantity).count()

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

        'caisse': caisse, 'bank': bank,
        # 'customers': customers, 'suppliers': suppliers,
        # 'buyorder_number': buyorder_number, 'sellorder_number': sellorder_number,
        # total orders
        'totalsellorders': totalsellorders, 'totalbuyorders': totalbuyorders,

        'stockproductsalertcount': stockproductsalertcount,
        # total debts & credits
        'totaldebt': totaldebt, 'totalcredit': totalcredit, 'total_provider_credit': total_provider_credit,
        # daily data
        'totaltodaypanne': totaltodaypanne, 'totaltodaypiece': totaltodaypiece,
        'payed_totaltodaypanne': payed_totaltodaypanne, 'payed_totaltodaypiece': payed_totaltodaypiece,
        'today_caisse': today_caisse, 'daily_salary': daily_salary,

        'total_salary': total_salary, 'chief_percentage': chief_percentage,
        'current_year': current_year,

        # top five debts
        'top_five_suppliers': top_five_suppliers, 'top_five_customers': top_five_customer,
        'top_five_providers': top_five_providers,
    }
    return render(request, 'dashboard.html', context)


# choosing the current year
def choose_the_year(request):
    yearform = CurrentYearForm()

    if request.method == 'POST':
        yearform = CurrentYearForm(request.POST)
        print(request.POST)
        if yearform.is_valid():
            chosen_year = yearform.save(commit=False)
            print("chosen year ===", chosen_year)
            if CurrentYear.objects.all().filter(user=request.user):
                current_year = CurrentYear.objects.all().filter(user=request.user)[:1].get()
            else:
                current_year = CurrentYear.objects.create(year=2022, user=request.user)
            print(current_year)
            if chosen_year.year == current_year.year:
                pass
            else:
                current_year.year = chosen_year.year
                current_year.user = request.user
                current_year.save()
            # return redirect("/")

    context = {
        'yearform': yearform,
    }

    return render(request, "setting.html", context)
