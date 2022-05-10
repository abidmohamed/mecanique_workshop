from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
# Create your views here.
from accounts.models import CurrentYear
from customer.forms import CustomerForm
from customer.models import Customer
from rdv.filters import PanneFilter
from rdv.forms import RdvFrom, PanneForm
from rdv.models import Panne, RdvItem, Rdv
from sellorder.models import Order, PanneItem
from vehicule.forms import VehiculeFrom, TypeForm
from vehicule.models import Vehicle, Type
import calendar


def create_rdv_customer(request):
    customer_form = CustomerForm()
    customers = Customer.objects.all()
    if request.method == 'POST':
        # print(customer_id)
        # get chosen customer
        customer_id = request.POST.get("customer")
        # remove white space from id
        customer_id = ''.join(customer_id.split())
        customer = Customer.objects.get(id=customer_id)
        return redirect('rdv:rdv_vehicle_list', customer.id)

    context = {'customers': customers,
               'customer_form': customer_form,
               }
    return render(request, 'rdv/customer_list.html', context)


def rdv_vehicle_list(request, pk):
    customer = Customer.objects.get(id=pk)
    vehicles = Vehicle.objects.all().filter(customer=customer)
    types = Type.objects.all()
    vehiculeform = VehiculeFrom()
    typeform = TypeForm()
    if request.method == 'POST':
        vehicle_id = request.POST.get("vehicle")
        print(vehicle_id)
        return redirect('rdv:create_rdv', vehicle_id)

    context = {'vehicles': vehicles,
               'customer': customer,
               'types': types,
               'vehiculeform': vehiculeform,
               'typeform': typeform,
               }
    return render(request, 'rdv/vehicle_list.html', context)


def create_rdv(request, pk):
    # Remove white spaces
    pk = ''.join(pk.split())
    vehicle = Vehicle.objects.get(id=pk)
    rdvform = RdvFrom()
    pannes = Panne.objects.all()

    if request.method == 'POST':
        rdvform = RdvFrom(request.POST)
        pannes_list = request.POST.getlist('pannes')
        if rdvform.is_valid():
            rdv = rdvform.save(commit=False)
            rdv.vehicle = vehicle
            rdv.customer = vehicle.customer
            rdv.save()
            if len(pannes_list):
                for panne in pannes_list:
                    rdvitem = RdvItem()
                    rdvitem.rdv = rdv
                    rdvitem.panne = Panne.objects.get(id=panne)
                    rdvitem.price = Panne.objects.get(id=panne).price
                    rdvitem.save()
            return redirect('rdv:rdv_list')

    context = {
        'rdvform': rdvform,
        'pannes': pannes,
    }
    return render(request, 'rdv/add_rdv.html', context)


def rdv_details(request, pk):
    rdv = Rdv.objects.get(id=pk)
    context = {
        'rdv': rdv,
    }
    return render(request, 'rdv/rdv_detail.html', context)


def rdv_pdf(request, pk):
    rdv = get_object_or_404(Rdv, id=pk)
    html = render_to_string('rdv/pdf.html', {'rdv': rdv})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=rdv_{rdv.id}_{rdv.rdv_date}_{rdv.customer}.pdf'

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def rdv_list(request):
    rdvs = Rdv.objects.all()
    context = {
        'rdvs': rdvs,
    }
    return render(request, 'rdv/rdv_list.html', context)


def delete_rdv(request, pk):
    rdv = Rdv.objects.get(id=pk)
    context = {'rdv': rdv}
    if request.method == 'POST':
        rdv.delete()
        return redirect('rdv:rdv_list')
    return render(request, 'rdv/delete_rdv.html', context)


# Panne
def create_panne(request):
    panneform = PanneForm()
    if request.method == 'POST':
        panneform = PanneForm(request.POST)
        if panneform.is_valid():
            panneform.save()
            return redirect('rdv:panne_list')

    context = {
        'panneform': panneform,
    }
    return render(request, 'panne/add_panne.html', context)


# Add Panne To update order
def update_order_panne_list(request, pk):
    sellorder = Order.objects.get(id=pk)
    pannes = Panne.objects.all()
    if request.method == 'POST':
        # get submitted order
        chosenpannes = request.POST.getlist("pannes")
        if len(chosenpannes) != 0:
            for panne in chosenpannes:
                currentpanne = Panne.objects.get(id=panne)

                PanneItem.objects.create(
                    order=sellorder,
                    panne=currentpanne,
                    price=currentpanne.price,
                )
        return redirect('sellorder:update_order', sellorder.id)
    context = {
        'pannes': pannes,
    }
    return render(request, 'panne/modal_order_list_panne.html', context)


# Add Panne to Confirm order
def confirm_order_panne_list(request, pk):
    sellorder = Order.objects.get(id=pk)
    pannes = Panne.objects.all()
    if request.method == 'POST':
        # get submitted order
        chosenpannes = request.POST.getlist("pannes")
        if len(chosenpannes) != 0:
            for panne in chosenpannes:
                currentpanne = Panne.objects.get(id=panne)

                PanneItem.objects.create(
                    order=sellorder,
                    panne=currentpanne,
                    price=currentpanne.price,
                )
        return redirect('sellorder:confirm_order', sellorder.id)
    context = {
        'pannes': pannes,
    }
    return render(request, 'panne/modal_order_list_panne.html', context)


def panne_list(request):
    pannes = Panne.objects.all()
    context = {
        'pannes': pannes,
    }
    return render(request, 'panne/panne_list.html', context)


def order_panne_list(request, pk):
    # Sell Order
    sellorder = get_object_or_404(Order, id=pk)
    list_index = list(sellorder.items.all())
    # chosenyear
    if CurrentYear.objects.all().filter(user=request.user):
        current_year = CurrentYear.objects.all().filter(user=request.user)[:1].get()
    else:
        current_year = CurrentYear.objects.create(year=2022, user=request.user)
    pannes_list = Panne.objects.all().order_by('-id')

    myFilter = PanneFilter(request.GET, queryset=pannes_list)

    # paginated after filtering
    pannes_list = myFilter.qs

    #page
    page = request.GET.get('page', 1)
    # Number of customers in the page
    paginator = Paginator(pannes_list, 5)

    try:
        pannes = paginator.page(page)
    except PageNotAnInteger:
        pannes = paginator.page(1)
    except EmptyPage:
        pannes = paginator.page(paginator.num_pages)

    # Form submitting
    if request.method == 'POST':
        chosenpannes = request.POST.getlist("pannes")
        # add pannes
        if len(chosenpannes) != 0:
            for panne in chosenpannes:
                panne = ''.join(panne.split())
                currentpanne = Panne.objects.get(id=panne)
                # print(currentpanne)
                PanneItem.objects.create(
                    order=sellorder,
                    panne=currentpanne,
                    price=currentpanne.price
                )

        return redirect('services:order_service_list', sellorder.pk)

    context = {
        'pannes': pannes,
        'order': sellorder,
        'myFilter': myFilter,
        'current_year': current_year,
        'list_index': list_index,
    }
    return render(request, 'panne/order_panne_list.html', context)




def update_panne(request, pk):
    panne = Panne.objects.get(id=pk)
    panneform = PanneForm(instance=panne)
    if request.method == 'POST':
        panneform = PanneForm(request.POST, instance=panne)
        if panneform.is_valid():
            panneform.save()
            return redirect('rdv:panne_list')

    context = {
        'panneform': panneform,
    }
    return render(request, 'panne/add_panne.html', context)


def delete_panne(request, pk):
    panne = Panne.objects.get(id=pk)
    context = {'panne': panne}
    if request.method == 'POST':
        panne.delete()
        return redirect('rdv:panne_list')
    return render(request, 'panne/delete_panne.html', context)


