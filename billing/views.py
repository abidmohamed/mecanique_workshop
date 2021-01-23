from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from xhtml2pdf import pisa

from billing.models import BuyOrderBilling, OrderBilling


def buybill_list(request):
    bills = BuyOrderBilling.objects.all()
    context = {'bills': bills}

    return render(request, 'billingbuyorder/list_bill.html', context)


def delete_billbuy(request, pk):
    bill = get_object_or_404(BuyOrderBilling, id=pk)
    context = {'bill': bill}
    if request.method == 'POST':
        bill.delete()

        return redirect('billing:buybill_list')
    return render(request, 'billingbuyorder/list_bill.html', context)


def buybill_pdf(request, pk):
    bill = get_object_or_404(BuyOrderBilling, id=pk)
    html = render_to_string('billingbuyorder/pdf.html', {'bill': bill})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=bill_{bill.id}_{bill.supplier}.pdf'
    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def sellbill_list(request):
    bills = OrderBilling.objects.all()
    context = {'bills': bills}

    return render(request, 'billingsellorder/list_bill.html', context)


def delete_billsell(request, pk):
    bill = get_object_or_404(OrderBilling, id=pk)
    context = {'bill': bill}
    if request.method == 'POST':
        bill.delete()

        return redirect('billing:sellbill_list')
    return render(request, 'billingsellorder/list_bill.html', context)


def sellbill_pdf(request, pk):
    bill = get_object_or_404(OrderBilling, id=pk)
    html = render_to_string('billingsellorder/pdf.html', {'bill': bill})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=bill_{bill.id}_{bill.customer}.pdf'
    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
