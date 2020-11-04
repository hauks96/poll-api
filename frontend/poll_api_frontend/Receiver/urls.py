from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('vote/', views.vote, name='vote'),
    path('register/', views.register, name='register'),
    path('argument-form/', views.get_arg_form, name='arg-form'),
    path('poll-details/', views.poll_details, name='poll-details'),
    path('receive-data/', views.receive_data, name='receive-data')
]
# TODO: Add urls for all functionality
