from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.urls import reverse
def role_required(allowed_roles):
    def decorators(view_func):
        def wrap(request, *args, **kwargs):
            if request.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseRedirect(reverse('employee_list'))
        return wrap
    return decorators

def admin_only(view_func):
    def wrap(request, *args, **kwargs):
        if request.role == 'Admin':
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('employee_list'))
    return wrap
def admin_hr_required(view_func):
    def wrap(request, *args, **kwargs):
        allowed_roles=["Admin", "HR"]
        if request.role in allowed_roles:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('employee_list'))
    return wrap
