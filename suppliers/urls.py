from django.urls import path
from . import views

app_name = 'suppliers'

urlpatterns = [
    path('', views.suppliers_list,name='suppliers_list'),
    path('create/',views.suppliers_create,name='suppliers_create'),
    path('<int:pk>/edit/',views.suppliers_edit,name='suppliers_edit'),
    path('<int:pk>/delete/',views.suppliers_delete,name='suppliers_delete'),
]