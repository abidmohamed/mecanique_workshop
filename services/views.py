from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime, date
# Create your views here.
from accounts.models import CurrentYear
from caisse.forms import DateForm
from sellorder.models import Order, ServiceItem
from services.forms import ServiceForm, ServiceProviderForm
from services.models import Service, ServiceProvider


def add_service(request):
    serviceform = ServiceForm()
    if request.method == 'POST':
        serviceform = ServiceForm(request.POST)
        if serviceform.is_valid():
            serviceform.save()
            return redirect("services:service_list")
    context = {
        'serviceform': serviceform
    }
    return render(request, 'services/add_service.html', context)


def service_list(request):
    services = Service.objects.all()
    context = {
        'services': services,
    }
    return render(request, 'services/service_list.html', context)


def update_service(request, pk):
    service = Service.objects.get(id=pk)
    serviceform = ServiceForm(instance=service)
    if request.method == 'POST':
        serviceform = ServiceForm(request.POST, instance=service)
        if serviceform.is_valid():
            serviceform.save()
            return redirect("services:service_list")
    context = {
        'serviceform': serviceform
    }
    return render(request, 'services/add_service.html', context)


def delete_service(request, pk):
    service = Service.objects.get(id=pk)
    context = {'service': service}
    if request.method == 'POST':
        service.delete()
        return redirect('/')
    return render(request, 'services/delete_service.html', context)


# Add Service to confirm order
def confirm_order_service_list(request, pk):
    sellorder = Order.objects.get(id=pk)
    services = Service.objects.all()
    if request.method == 'POST':
        chosenservices = request.POST.getlist("services")
        if len(chosenservices) != 0:
            for service in chosenservices:
                currentservice = Service.objects.get(id=service)
                ServiceItem.objects.create(
                    order=sellorder,
                    service=currentservice,
                    price=currentservice.price + currentservice.charge
                )
        return redirect('sellorder:confirm_order', sellorder.id)

    context = {
        'services': services,
    }
    return render(request, 'services/modal_order_list_service.html', context)


# Add Service to update order
def update_order_service_list(request, pk):
    sellorder = Order.objects.get(id=pk)
    services = Service.objects.all()
    if request.method == 'POST':
        chosenservices = request.POST.getlist("services")
        if len(chosenservices) != 0:
            for service in chosenservices:
                currentservice = Service.objects.get(id=service)
                ServiceItem.objects.create(
                    order=sellorder,
                    service=currentservice,
                    price=currentservice.price + currentservice.charge
                )
        return redirect('sellorder:update_order', sellorder.id)

    context = {
        'services': services,
    }
    return render(request, 'services/modal_order_list_service.html', context)


def add_provider(request):
    providerform = ServiceProviderForm()
    if request.method == 'POST':
        providerform = ServiceProviderForm(request.POST)
        if providerform.is_valid():
            providerform.save()
            return redirect("services:provider_list")
    context = {
        'providerform': providerform
    }
    return render(request, 'services/add_provider.html', context)


def provider_list(request):
    providers = ServiceProvider.objects.all()
    current_year = CurrentYear.objects.all().filter()[:1].get()

    context = {
        'providers': providers,
        'current_year': current_year,
    }
    return render(request, 'services/provider_list.html', context)


def update_provider(request, pk):
    provider = ServiceProvider.objects.get(id=pk)
    providerform = ServiceProviderForm(instance=provider)
    if request.method == 'POST':
        providerform = ServiceProviderForm(request.POST, instance=provider)
        if providerform.is_valid():
            providerform.save()
            return redirect("services:provider_list")
    context = {
        'providerform': providerform
    }
    return render(request, 'services/add_provider.html', context)


def delete_provider(request, pk):
    provider = ServiceProvider.objects.get(id=pk)
    context = {'provider': provider}
    if request.method == 'POST':
        provider.delete()
        return redirect('/')
    return render(request, 'services/delete_provider.html', context)


def provider_details(request, pk):
    provider = get_object_or_404(ServiceProvider, id=pk)
    # TimeField related
    # current year
    current_year = CurrentYear.objects.all().filter()[:1].get()
    dateform = DateForm()
    # now time
    chosen_date = datetime.now()

    # services in confirmed orders
    confirmed_services = provider.provided_item.filter(
        provider=provider,
        order__confirmed=True,
        order__factured=False,
        order__order_date__year=current_year.year
    )

    # total services
    total_confirmed_services = 0
    for service in confirmed_services:
        total_confirmed_services += service.price

    # services in proforma orders
    proforma_services = provider.provided_item.filter(
        provider=provider,
        order__confirmed=False,
        order__factured=False,
        order__order_date__year=current_year.year
    )

    # Total Proforma
    total_proforma_services = 0
    for service in proforma_services:
        total_proforma_services += service.price

    # services in billed orders
    billed_services = provider.provided_item.filter(
        provider=provider,
        order__confirmed=True,
        order__factured=True,
        order__order_date__year=current_year.year
    )
    # total Billed
    total_billed_services = 0
    for service in billed_services:
        total_billed_services += service.price

    # provider Payments
    payments = provider.payments.filter(
        provider=provider,
        pay_date__year=current_year.year,
    )

    # total payments
    total_payments = 0
    for payment in payments:
        total_payments += payment.amount

    context = {
        'provider': provider,
        'current_year': current_year,
        'dateform': dateform,
        'chosen_date': chosen_date,
        'confirmed_services': confirmed_services,
        'total_confirmed_services': total_confirmed_services,
        'proforma_services': proforma_services,
        'total_proforma_services': total_proforma_services,
        'billed_services': billed_services,
        'total_billed_services': total_billed_services,
        'payments': payments,
        'total_payments': total_payments,
    }
    return render(request, 'services/provider_detail.html', context)
