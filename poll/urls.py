from django.urls import path
from poll.views import index, details, polls, PollView

urlpatterns = [
    path('', index, name="home"),
    path('<int:id>/details', details, name="post_details"),
    path('<int:id>/', polls, name="single_poll"),

    path('add/', PollView.as_view(), name='poll_add'),
    path('<int:id>/edit/', PollView.as_view(), name='poll_edit'),
    path('<int:id>/delete/', PollView.as_view(), name='poll_delete'),
]