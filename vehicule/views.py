from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect

# Create your views here.
# Brand Views
from accounts.models import CurrentYear
from customer.models import Customer
from vehicule.filters import VehicleFilter
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


def add_type_rdv(request, pk):
    customer = Customer.objects.get(id=pk)
    if request.method == 'GET':
        typeform = TypeForm()
    elif request.method == 'POST':
        typeform = TypeForm(request.POST, request.FILES)
        if typeform.is_valid():
            typeform.save()
            return redirect('rdv:rdv_vehicle_list', customer.pk)

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
            # Remove white spaces
            chosencustomer = request.POST.get("customer")
            chosencustomer = ''.join(chosencustomer.split())
            vehicle.customer = Customer.objects.get(id=chosencustomer)

            chosentype = request.POST.get("type")
            chosentype = ''.join(chosentype.split())
            vehicle.vehicle_type = Type.objects.get(id=chosentype)
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
    # chosenyear
    if CurrentYear.objects.all().filter(user=request.user):
        current_year = CurrentYear.objects.all().filter(user=request.user)[:1].get()
    else:
        current_year = CurrentYear.objects.create(year=2022, user=request.user)

    vehicles_list = Vehicle.objects.all().order_by('-vehicle_name')

    myFilter = VehicleFilter(request.GET, queryset=vehicles_list)

    # paginate after filtering
    customers_list = myFilter.qs

    # Page
    page = request.GET.get('page', 1)
    # Number of customers in the page
    paginator = Paginator(customers_list, 5)

    try:
        vehicles = paginator.page(page)
    except PageNotAnInteger:
        vehicles = paginator.page(1)
    except EmptyPage:
        vehicles = paginator.page(paginator.num_pages)

    context = {
        'vehicles': vehicles,
        'current_year': current_year,
        'myFilter': myFilter,
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

            # Remove white spaces
            chosencustomer = request.POST.get("customer")
            chosencustomer = ''.join(chosencustomer.split())
            vehicle.customer = Customer.objects.get(id=chosencustomer)
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
