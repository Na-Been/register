from django.urls import path
from . import views

urlpatterns = [
    path('', views.register, name='home'),
    path('form/',views.showForm, name='form'),
    path('list/',views.profile_list, name='list'),
]
