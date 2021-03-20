from django.shortcuts import render, redirect

# Create your views here.
# Brand Views
from customer.models import Customer
from vehicule.forms import BrandForm, TypeForm, VehiculeFrom
from vehicule.models import Brand, Type, Vehicle


def add_brand(request):
    if request.method == 'GET':
        brandform = BrandForm()
    elif request.method == 'POST':
        brandform = BrandForm(request.POST, request.FILES)
        if brandform.is_valid():
            brandform.save()
            return redirect('vehicule:brand_list')
    context = {'brandform': brandform}
    return render(request, 'brand/add_brand.html', context)


def brand_list(request):
    brands = Brand.objects.all()
    context = {
        'brands': brands
    }
    return render(request, 'brand/list_brand.html', context)


def update_brand(request, pk):
    brand = Brand.objects.get(id=pk)
    brandform = BrandForm(instance=brand)
    if request.method == 'POST':
        brandform = BrandForm(request.POST, request.FILES, instance=brand)
        if brandform.is_valid():
            brandform.save()
            return redirect('vehicule:brand_list')

    context = {'brandform': brandform}
    return render(request, 'brand/add_brand.html', context)


def delete_brand(request, pk):
    brand = Brand.objects.get(id=pk)
    context = {'brand': brand}
    if request.method == 'POST':
        brand.delete()
        return redirect('vehicule:brand_list')
    return render(request, 'brand/delete_brand.html', context)


# Type Views
def add_type(request):
    if request.method == 'GET':
        typeform = TypeForm()
    elif request.method == 'POST':
        typeform = TypeForm(request.POST, request.FILES)
        if typeform.is_valid():
            typeform.save()
            return redirect('vehicule:all_type_list')

    context = {
        'typeform': typeform
    }
    return render(request, 'type/add_type.html', context)


def type_list(request, pk):
    brand = Brand.objects.get(id=pk)
    brands = Brand.objects.all()
    types = Type.objects.all().filter(brand=brand)

    context = {
        'brand': brand,
        'brands': brands,
        'types': types,
    }
    return render(request, 'type/list_type.html', context)


def all_type_list(request):
    types = Type.objects.all()
    context = {
        'types': types,
    }
    return render(request, 'type/all_list_type.html', context)


def update_type(request, pk):
    typo = Type.objects.get(id=pk)
    typeform = TypeForm(instance=typo)
    if request.method == 'POST':
        typeform = TypeForm(request.POST, request.FILES, instance=typo)
        if typeform.is_valid():
            typeform.save()
            return redirect('vehicule:all_type_list')
    context = {'typeform': typeform}
    return render(request, 'type/add_type.html', context)


def delete_type(request, pk):
    typo = Type.objects.get(id=pk)
    context = {'typo': typo}
    if request.method == 'POST':
        typo.delete()

        return redirect('vehicule:all_type_list')
    return render(request, 'type/delete_type.html', context)


# Vehicule views
def add_vehicule(request):
    types = Type.objects.all()
    customers = Customer.objects.all()
    vehiculeform = VehiculeFrom()
    if request.method == 'POST':
        vehiculeform = VehiculeFrom(request.POST)
        if vehiculeform.is_valid():
            vehicle = vehiculeform.save(commit=False)
            vehicle.customer = Customer.objects.get(id=request.POST.get("customer"))
            vehicle.vehicle_type = Type.objects.get(id=request.POST.get("type"))
            # print(request.POST.get("customer"))
            # print(request.POST.get("type"))
            vehicle.save()
            return redirect("vehicule:all_vehicule_list")
    context = {
        'types': types, 'customers': customers, 'vehiculeform': vehiculeform,
    }
    return render(request, 'vehicule/add_vehicule.html', context)


def add_vehicule_rdv(request, pk):
    types = Type.objects.all()
    customer = Customer.objects.get(id=pk)
    vehiculeform = VehiculeFrom()
    if request.method == 'POST':
        vehiculeform = VehiculeFrom(request.POST)
        if vehiculeform.is_valid():
            vehicle = vehiculeform.save(commit=False)
            vehicle.customer = customer
            vehicle.vehicle_type = Type.objects.get(id=request.POST.get("type"))
            # print(request.POST.get("customer"))
            # print(request.POST.get("type"))
            vehicle.save()
            return redirect("rdv:rdv_vehicle_list", customer.pk)
    context = {
        'types': types, 'vehiculeform': vehiculeform,
    }
    return render(request, 'vehicule/add_vehicule.html', context)


def all_vehicule_list(request):
    vehicles = Vehicle.objects.all()
    context = {
        'vehicles': vehicles,
    }
    return render(request, 'vehicule/all_list_vehicule.html', context)


def update_vehicule(request, pk):
    veh = Vehicle.objects.get(id=pk)
    types = Type.objects.all()
    customers = Customer.objects.all()
    vehiculeform = VehiculeFrom(instance=veh)
    if request.method == 'POST':
        vehiculeform = VehiculeFrom(request.POST, instance=veh)
        if vehiculeform.is_valid():
            vehicle = vehiculeform.save(commit=False)
            vehicle.customer = Customer.objects.get(id=request.POST.get("customer"))
            vehicle.vehicle_type = Type.objects.get(id=request.POST.get("type"))
            # print(request.POST.get("customer"))
            # print(request.POST.get("type"))
            vehicle.save()
            return redirect("vehicule:all_vehicule_list")
    context = {
        'types': types, 'customers': customers, 'vehiculeform': vehiculeform,
    }
    return render(request, 'vehicule/add_vehicule.html', context)


def delete_vehicule(request, pk):
    vehicle = Vehicle.objects.get(id=pk)
    context = {'vehicle': vehicle}
    if request.method == 'POST':
        vehicle.delete()

        return redirect('vehicule:all_vehicule_list')
    return render(request, 'vehicule/delete_vehicule.html', context)
