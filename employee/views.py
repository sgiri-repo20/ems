from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView
from employee.forms import UserForm
from employee.decorators import admin_only,role_required
# Create your views here.
def home(request):
    return HttpResponse('Welcome to home page')

@login_required(login_url="/login/")
@role_required(allowed_roles=['HR'])
# @admin_only
def employee_add(request):
    context = {}
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        context['user_form'] = user_form
        if user_form.is_valid():
            u = user_form.save()    
            return HttpResponseRedirect(reverse('employee_list'))
        else:
            return render(request, 'employee/add.html', context)
    else:
        user_form = UserForm()
        context['user_form'] = user_form
        return render(request, 'employee/add.html', context)
@login_required(login_url="/login/")
def employee_list(request):
    print(request.role)
    context = {}
    context['users'] = User.objects.all()
    context['title'] = 'Employees'
    return render(request, 'employee/index.html', context)

def employee_details(request, id=None):
    context = {}
    context['user'] = get_object_or_404(User, id=id)
    return render(request, 'employee/details.html', context)

def employee_edit(request, id=None):
    user = get_object_or_404(User, id=id)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('employee_list'))
        else:
            return render(request, 'employee/edit.html', {"user_form": user_form})
    else:
        user_form = UserForm(instance=user)
        return render(request, 'employee/edit.html', {"user_form": user_form})
    
def employee_delete(request, id=None):
    print(id)
    user = get_object_or_404(User, id=id)
    if request.method == 'POST':
        user.delete()
        return HttpResponseRedirect(reverse('employee_list'))
    else:
        context = {}
        context['user'] = user
        return render(request, 'employee/delete.html', context)

class ProfileUpdateView(UpdateView):
    fields = ['designation', 'salary']
    template_name = 'employee/profile_update.html'
    success_url = reverse_lazy('my_profile')

    def get_object(self):
        return self.request.user.employee

class MyProfile(DetailView):
    template_name = 'employee/profile.html'
    def get_object(self):
        return self.request.user.employee

def user_login(request):
    context = {}
    if request.method == 'POST':
        print('111')
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            print('1')
            login(request, user)
            if request.GET.get('next', None):
                HttpResponseRedirect(request.GET['next'])
            return HttpResponseRedirect(reverse('user_success'))
        else:
            context['error'] = 'Please provide valid username or password'
            return render(request, 'employee/login.html', context)
    else:        
        return render(request, 'employee/login.html', context)
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('user_login'))

@login_required(login_url="/login/")
def success(request):
    context = {}
    context['username'] = request.user.username
    return render(request, 'employee/success.html', context)

