from django.urls import path
from . import views

app_name = 'materials'

urlpatterns = [
    path('', views.material_list,name='material_list'),
    path('create/',views.material_create,name='material_create'),
]