from customer.forms import UserForm, CustomerForm, CityForm, EnterpriseForm
from customer.models import Customer, City, Enterprise
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect, get_object_or_404

from rdv.models import Rdv
from sellorder.models import Order, SellOrderFacture


def add_customer(request):
    # user_form = UserForm()
    customer_form = CustomerForm()

    if request.method == 'POST':
        # user_form = UserForm(request.POST)
        customer_form = CustomerForm(request.POST)

        if customer_form.is_valid():
            # user = user_form.save()
            customer = customer_form.save(commit=False)

            group = Group.objects.get(name='customer')
            # user.groups.add(group)

            # customer.user = user
            # customer.firstname = user.first_name
            # customer.lastname = user.last_name
            # customer.email = user.email
            customer.save()
            if customer.enterprise:
                return redirect('customer:add_enterprise', customer.id)
            else:
                return redirect('customer:customer_list')

    context = {
        # 'user_form': user_form,
        'customer_form': customer_form
    }
    return render(request, 'customer/add_customer.html', context)


def add_enterprise(request, pk):
    customer = Customer.objects.get(id=pk)
    # Enterprise form
    enter_form = EnterpriseForm()
    if request.method == 'POST':
        enter_form = EnterpriseForm(request.POST)
        if enter_form.is_valid():
            enterprise = enter_form.save(commit=False)
            enterprise.customer = customer
            enterprise.save()
            return redirect('customer:customer_list')

    context = {
        'enter_form': enter_form
    }
    return render(request, 'customer/add_enterprise.html', context)


def update_enterprise(request, pk):
    # customer = Customer.objects.get(id=pk)
    # get entrprise
    enterprise = Enterprise.objects.get(id=pk)
    # Enterprise form
    enter_form = EnterpriseForm(instance=enterprise)
    if request.method == 'POST':
        enter_form = EnterpriseForm(request.POST, instance=enterprise)
        if enter_form.is_valid():
            enter_form.save()
            return redirect('customer:customer_list')

    context = {
        'enter_form': enter_form
    }
    return render(request, 'customer/add_enterprise.html', context)


def enterprise_list(request):
    enterprises = Enterprise.objects.all()
    context = {
        'enterprises': enterprises
    }
    return render(request, 'customer/list_enterprise.html', context)


def delete_enterprise(request, pk):
    enterprise = Enterprise.objects.get(id=pk)
    context = {
        'enterprise': enterprise,
    }
    if request.method == 'POST':
        enterprise.delete()
        return redirect('customer:enterprise_list')
    return render(request, 'customer/delete_enterprise.html', context)


def add_customer_rdv(request):
    # user_form = UserForm()
    if request.method == 'GET':
        customer_form = CustomerForm()
    elif request.method == 'POST':
        # user_form = UserForm(request.POST)
        customer_form = CustomerForm(request.POST)
        if customer_form.is_valid():
            # user = user_form.save()
            customer = customer_form.save()
            # customer = customer_form.save(commit=False)
            group = Group.objects.get(name='customer')
            # user.groups.add(group)
            # customer.user = user
            # customer.firstname = user.first_name
            # customer.lastname = user.last_name
            # customer.email = user.email
            # customer.save()
            return redirect('rdv:create_rdv_customer')
    context = {
        # 'user_form': user_form,
        'customer_form': customer_form
    }
    return render(request, 'customer/add_customer.html', context)


def customer_list(request):
    customers = Customer.objects.all()
    context = {
        'customers': customers
    }
    return render(request, 'customer/list_customer.html', context)


def customer_debt_list(request):
    customers = Customer.objects.all().filter(debt__gt=0)
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
            if customer.enterprise:
                if Enterprise.objects.filter(customer=customer):
                    enterprise = Enterprise.objects.get(customer=customer)
                    return redirect('customer:update_enterprise', enterprise.id)
                else:
                    return redirect('customer:add_enterprise', customer.id)
            else:
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
        if Order.objects.filter(customer=customer):
            pass
        else:
            customer.delete()
        return redirect('customer:customer_list')
    return render(request, 'customer/delete_customer.html', context)


def customer_detail(request, pk):
    customer = get_object_or_404(Customer, id=pk)
    orders = Order.objects.all().filter(customer=customer, confirmed=True, factured=False)
    proforma_orders = Order.objects.all().filter(customer=customer, confirmed=False)
    factured_orders = SellOrderFacture.objects.all().filter(order__customer=customer)
    rdvs = Rdv.objects.all().filter(customer=customer)
    context = {
        'customer': customer,
        'orders': orders,
        'proforma_orders': proforma_orders,
        'factured_orders': factured_orders,
        'rdvs': rdvs,
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
