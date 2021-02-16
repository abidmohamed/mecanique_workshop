from django.shortcuts import render
import calendar
from datetime import date, datetime
from datetime import timedelta
# Create your views here.
from django.utils.safestring import mark_safe

from buyorder.models import BuyOrder
from caisse.models import Caisse
from customer.models import Customer
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


# Dashboard
def home(request):
    calendar_date = get_date(request.GET.get('month', None))
    none_html_calendar = Calendar(calendar_date.year, calendar_date.month)
    html_calendar = none_html_calendar.formatmonth(withyear=True)
    sellorders = Order.objects.all()  # .filter(created__year=now.year, created__month=now.month)
    buyorders = BuyOrder.objects.all()  # can be filtred by year & month
    # customers + suppliers all objects
    allcustomers = Customer.objects.all()
    allsuppliers = Supplier.objects.all()
    # Caisse
    caisse = Caisse.objects.all().filter()[:1].get().caisse_value
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
    sellorder_number = Order.objects.all().count()
    # sell orders total
    totalsellorders = 0
    totalbuyorders = 0
    for order in sellorders:
        totalsellorders += order.get_total_cost()
    # Buy orders total
    for order in buyorders:
        totalbuyorders += order.get_total_cost()

    # Stock Qt Alert
    stockproductsalertcount=0
    products = Product.objects.all()
    for product in products:
        stockproductsalertcount = StockProduct.objects.all().filter(quantity__lte=product.alert_quantity).count()

    if not stockproductsalertcount:
        stockproductsalertcount= 0

    context = {
        'calendar': mark_safe(html_calendar),
        'prev_month': prev_month(calendar_date),
        'next_month': next_month(calendar_date),
        'caisse': caisse, 'customers': customers,
        'buyorder_number': buyorder_number, 'sellorder_number': sellorder_number,
        'totalsellorders': totalsellorders, 'totalbuyorders': totalbuyorders,
        'stockproductsalertcount': stockproductsalertcount, 'suppliers': suppliers,
        'totaldebt': totaldebt, 'totalcredit': totalcredit,
    }
    return render(request, 'dashboard.html', context)
