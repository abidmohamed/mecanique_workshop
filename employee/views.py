from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from employee.forms import JobForm, EmployeeForm

# Job
from employee.models import Job, Employee


def add_job(request):
    job_form = JobForm()

    if request.method == 'POST':
        job_form = JobForm(request.POST)

        if job_form.is_valid():
            job_form.save()

            return redirect("employee:list_job")

    context = {
        'job_form': job_form
    }

    return render(request, 'job/add.html', context)


def list_job(request):
    jobs = Job.objects.all()

    context = {
        'jobs': jobs
    }

    return render(request, 'job/list.html', context)


def add_employee(request):
    employee_form = EmployeeForm()

    if request.method == 'POST':
        employee_form = EmployeeForm(request.POST)

        if employee_form.is_valid():
            employee_form.save()

            return redirect("employee:list_employee")

    context = {
        'employee_form': employee_form
    }

    return render(request, 'employee/add.html', context)


def list_employee(request):
    employees = Employee.objects.all()

    context = {
        'employees': employees
    }

    return render(request, 'employee/list.html', context)


def update_employee(request, pk):
    employee = get_object_or_404(Employee, id=pk)
    employee_form = EmployeeForm(instance=employee)

    if request.method == 'POST':
        employee_form = EmployeeForm(request.POST, instance=employee)

        if employee_form.is_valid():
            employee_form.save()

            return redirect("employee:list_employee")

    context = {
        'employee_form': employee_form
    }

    return render(request, 'employee/add.html', context)

