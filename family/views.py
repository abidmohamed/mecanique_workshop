from django.shortcuts import render, redirect

# Create your views here.
from family.forms import FamilyForm
from family.models import Family


def add_family(request):
    if request.method == 'GET':
        familyform = FamilyForm()
    elif request.method == 'POST':
        familyform = FamilyForm(request.POST, request.FILES)
        if familyform.is_valid():
            familyform.save()
            return redirect('/')
    context = {'familyform': familyform}
    return render(request, 'family/add_family.html', context)


def family_list(request):
    families = Family.objects.all()
    context = {
        'families': families,
    }
    return render(request, 'family/list_family.html', context)


def update_family(request, pk):
    family = Family.objects.get(id=pk)
    familyform = FamilyForm(instance=family)
    if request.method == 'POST':
        familyform = FamilyForm(request.POST, request.FILES, instance=family)
        if familyform.is_valid():
            familyform.save()
            return redirect('/')
    context = {'familyform': familyform}
    return render(request, 'family/add_family.html', context)


def delete_family(request, pk):
    family = Family.objects.get(id=pk)
    context = {'family': family}
    if request.method == 'POST':
        family.delete()
        return redirect('/')
    return render(request, 'family/delete_family.html', context)

