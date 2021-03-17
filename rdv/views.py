
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
# Create your views here.
from customer.models import Customer
from rdv.forms import RdvFrom, PanneForm
from rdv.models import Panne, RdvItem, Rdv
from sellorder.models import Order, PanneItem
from vehicule.models import Vehicle
import calendar


def create_rdv_customer(request):
    customers = Customer.objects.all()
    if request.method == 'POST':
        customer_id = request.POST.get("customer")
        print(customer_id)
        customer = Customer.objects.get(id=customer_id)
        return redirect('rdv:rdv_vehicle_list', customer.id)

    context = {'customers': customers, }
    return render(request, 'rdv/customer_list.html', context)


def rdv_vehicle_list(request, pk):
    customer = Customer.objects.get(id=pk)
    vehicles = Vehicle.objects.all().filter(customer=customer)
    if request.method == 'POST':
        vehicle_id = request.POST.get("vehicle")
        print(vehicle_id)
        return redirect('rdv:create_rdv', vehicle_id)

    context = {'vehicles': vehicles, }
    return render(request, 'rdv/vehicle_list.html', context)


def create_rdv(request, pk):
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
            return redirect('rdv:rdv_pdf', rdv.id)

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


def panne_list(request):
    pannes = Panne.objects.all()
    context = {
        'pannes': pannes,
    }
    return render(request, 'panne/panne_list.html', context)


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


