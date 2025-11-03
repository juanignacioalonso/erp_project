from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Material
from .forms import MaterialForm
from django.core.paginator import Paginator
from django.http import HttpResponse
import csv
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
    if status not in [None, '']:
        material_list = material_list.filter(status=status)

    if request.GET.get('export') == 'csv':
        # Configura respuesta HTTP
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="materials.csv"'

        # BOM UTF-8 → evita caracteres raros en Excel
        response.write('\ufeff')

        writer = csv.writer(response, delimiter=';', quoting=csv.QUOTE_MINIMAL)

        # Cabeceras del archivo
        writer.writerow([
        'ID Material',
        'Name',
        'Description',
        'Unit',
        'Type',
        'Status',
        'Created By',
        'Created At',
        'Updated At'
        ])

        # Filas con datos
        for material in material_list:
            writer.writerow([
                material.id_material or '',
                material.name or '',
                material.description or '',
                material.unit or '',
                material.material_type or '',
                material.status or '',
                material.created_by.username if material.created_by else 'N/A',
                material.created_at.strftime('%Y-%m-%d %H:%M:%S') if material.created_at else '',
                material.updated_at.strftime('%Y-%m-%d %H:%M:%S') if material.updated_at else '',
            ])

        return response

    paginator = Paginator(material_list,10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'materials/materials_list.html', {
    'page_obj': page_obj,
    'permissions': {'materials': max_permission},  
})


@login_required
def material_create(request):

    max_permission = UserRole.objects.filter(user_id=request.user).aggregate(max_permission=models.Max('role__materials'))['max_permission'] or 0

    if max_permission == 1:
        return redirect('materials')
    if max_permission == 0:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = MaterialForm(request.POST)
        if form.is_valid():

            material = form.save(commit=False)
            material.created_by =request.user
            material.save()

            return redirect('materials:material_create')
    else:
        form = MaterialForm()
        
    return render(request, 'materials/Material_form.html', {'form': form})

@login_required
def material_edit(request,pk):

    material = get_object_or_404(Material,pk=pk)

    max_permission = UserRole.objects.filter(user_id=request.user).aggregate(max_permission=models.Max('role__materials'))['max_permission'] or 0

    if max_permission == 1:
        return redirect('materials')
    if max_permission == 0:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = MaterialForm(request.POST, instance=material)
        if form.is_valid():
            form.save()
            return redirect('materials:materials_list')
    else:
        form = MaterialForm(instance=material)

    context = {
        'form': form,
        'material': material,
    }

    return render(request, 'materials/material_form.html', context)


@login_required
def material_delete(request,pk):

    max_permission = UserRole.objects.filter(user_id=request.user).aggregate(max_permission=models.Max('role__materials'))['max_permission'] or 0

    if max_permission <2:
        return redirect('material:material_list')
    
    material = get_object_or_404(Material,pk=pk)

    if request.method == 'POST':
        material.delete()
        return redirect('materials:materials_list')
    
    return redirect('materials:materials_list')
