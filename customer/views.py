from customer.forms import UserForm, CustomerForm, CityForm
from customer.models import Customer, City
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect, get_object_or_404


def add_customer(request):
    user_form = UserForm()
    customer_form = CustomerForm()

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        customer_form = CustomerForm(request.POST)

        if customer_form.is_valid():
            user = user_form.save()
            customer = customer_form.save(commit=False)

            group = Group.objects.get(name='customer')
            user.groups.add(group)

            customer.user = user
            customer.firstname = user.first_name
            customer.lastname = user.last_name
            customer.email = user.email
            customer.save()

            return redirect('customer:customer_list')

    context = {
        'user_form': user_form,
        'customer_form': customer_form
    }
    return render(request, 'customer/add_customer.html', context)


def customer_list(request):
    customers = Customer.objects.all()
    context = {
        'customers': customers
    }
    return render(request, 'customer/list_customer.html', context)


def sellorder_customer_list(request):
    customers = Customer.objects.all()
    context = {
        'customers': customers
    }
    return render(request, 'customer/sellorder_list_customer.html', context)


def update_customer(request, pk):
    customer = Customer.objects.get(id=pk)
    customer_form = CustomerForm(instance=customer)
    if request.method == 'POST':
        customer_form = CustomerForm(request.POST, instance=customer)
        if customer_form.is_valid():
            customer_form.save()
            return redirect('customer:customer_list')
    context = {
        'customer_form': customer_form
    }
    return render(request, 'customer/add_customer.html', context)


def delete_customer(request, pk):
    customer = Customer.objects.get(id=pk)
    context = {
        'customer': customer
    }
    if request.method == 'POST':
        customer.delete()
        return redirect('customer:customer_list')
    return render(request, 'customer/delete_customer.html', context)


def customer_detail(request, pk):
    customer = get_object_or_404(Customer, id=pk)
    context = {
        'customer': customer
    }
    return render(request, 'customer/detail.html', context)


def add_city(request):
    city_form = CityForm()

    if request.method == 'POST':
        city_form = CityForm(request.POST)

        if city_form.is_valid():
            city_form.save()
            return redirect('/')
    context = {'city_form': city_form}
    return render(request, 'city/add_city.html', context)


def city_list(request):
    cities = City.objects.all()
    context = {
        'cities': cities
    }
    return render(request, 'city/list_city.html', context)


def update_city(request, pk):
    city = City.objects.get(id=pk)
    city_form = CityForm(instance=city)
    if request.method == 'POST':
        city_form = CityForm(request.POST, instance=city)
        if city_form.is_valid():
            city_form.save()
            return redirect('customer:city_list')
    context = {
        'city_form': city_form
    }
    return render(request, 'city/add_city.html', context)


def delete_city(request, pk):
    city = City.objects.get(id=pk)
    context = {
        'city': city
    }
    if request.method == 'POST':
        city.delete()
        return redirect('customer:city_list')
    return render(request, 'city/delete_family.html', context)
