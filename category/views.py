from django.shortcuts import render, redirect

# Create your views here.
from category.forms import CategoryForm
from category.models import Category
from customer.models import Customer
from family.models import Family


def add_category(request):
    if request.method == 'GET':
        categoryform = CategoryForm()
    elif request.method == 'POST':
        categoryform = CategoryForm(request.POST, request.FILES)
        if categoryform.is_valid():
            categoryform.save()
            return redirect('/')
    context = {'categoryform': categoryform}
    return render(request, 'category/add_category.html', context)


def category_list(request, pk):
    family = Family.objects.get(id=pk)
    families = Family.objects.all()
    categories = Category.objects.all().filter(family=family)

    context = {
        'family': family,
        'families': families,
        'categories': categories,
    }
    return render(request, 'category/list_category.html', context)


def all_category_list(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'category/all_list_category.html', context)


def update_category(request, pk):
    category = Category.objects.get(id=pk)
    categoryform = CategoryForm(instance=category)
    if request.method == 'POST':
        categoryform = CategoryForm(request.POST, request.FILES, instance=category)
        if categoryform.is_valid():
            categoryform.save()
            return redirect('/')
    context = {'categoryform': categoryform}
    return render(request, 'category/add_category.html', context)


def delete_category(request, pk):
    category = Category.objects.get(id=pk)
    context = {'category': category}
    if request.method == 'POST':
        category.delete()

        return redirect('/')
    return render(request, 'category/delete_category.html', context)
