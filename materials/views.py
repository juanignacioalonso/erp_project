from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Material
from .forms import MaterialForm
from django.core.paginator import Paginator
from django.db import models
from users.models import UserRole

# Create your views here.

@login_required
def material_list(request):

    max_permission = UserRole.objects.filter(user_id=request.user).aggregate(max_permission=models.Max('role__materials'))['max_permission'] or 0

    if max_permission == 0:
        return redirect('dashboard')
    
    material_list = Material.objects.all().order_by('id_material')

    id_material = request.GET.get('id_material')
    name = request.GET.get('name')
    material_type = request.GET.get('material_type')
    status = request.GET.get('status')

    if id_material:
        material_list = material_list.filter(id_material__icontains=id_material)
    if name:
        material_list = material_list.filter(name__icontains=name)
    if material_type:
        material_list = material_list.filter(material_type__icontains=material_type)
    if status is not None and status != '':
        material_list = material_list.filter(status=status)

    paginator = Paginator(material_list,10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'materials/materials_list.html',{'page_obj':page_obj})


@login_required
def material_create(request):

    max_permission = UserRole.objects.filter(user_id=request.user).aggregate(max_permission=models.Max('role__materials'))['max_permission'] or 0

    if max_permission == 1:
        return redirect('materials:material_list')
    if max_permission == 0:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = MaterialForm(request.POST)
        if form.is_valid():

            material = form.save(commit=False)
            material.created_by =request.user
            material.save()

            return redirect('materials:material_list')
    else:
        form = MaterialForm()
        
    return render(request, 'materials/Material_form.html', {'form': form})