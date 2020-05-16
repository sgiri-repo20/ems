from django.urls import path
from employee import views

urlpatterns = [
    path('', views.home, name='employee_home'),
    path('list/', views.employee_list, name='employee_list'),
    path('add/', views.employee_add, name='employee_add'),
    path('<int:id>/details/', views.employee_details, name='employee_details'),
    path('<int:id>/edit/', views.employee_edit, name='employee_edit'),
    path('<int:id>/delete/', views.employee_delete, name='employee_delete'),
    # path('profile-edit/', views.ProfileUpdateView.as_view(), name='my_profile'),
    # path('', views.MyProfile.as_view(), name='profile'),

    path('profile/', views.MyProfile.as_view(), name="my_profile"),
    path('profile/update', views.ProfileUpdateView.as_view(), name="update_profile"),
    
]