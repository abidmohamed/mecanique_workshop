from django.shortcuts import render, redirect

# Create your views here.
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
    context = {
        'providers': providers,
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
