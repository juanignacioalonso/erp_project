from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Supplier
from .forms import SupplierForm
from django.core.paginator import Paginator
from django.http import HttpResponse
import csv
from django.db import models
from users.models import UserRole

# Create your views here.

@login_required
def suppliers_list(request):

    max_permission = UserRole.objects.filter(user_id=request.user).aggregate(max_permission=models.Max('role__suppliers'))['max_permission'] or 0

    if max_permission == 0:
        return redirect('dashboard')
    
    supplier_list = Supplier.objects.all().order_by('id_supplier')

    id_supplier = request.GET.get('id_supplier')
    name = request.GET.get('name')
    country = request.GET.get('country')
    status = request.GET.get('status')

    if id_supplier:
        supplier_list = supplier_list.filter(id_supplier__icontains=id_supplier)
    if name:
        supplier_list = supplier_list.filter(name__icontains=name)
    if country:
        supplier_list = supplier_list.filter(country__icontains=country)
    if status not in [None, '']:
        supplier_list = supplier_list.filter(status=status)

    if request.GET.get('export') == 'csv':
        # Configura respuesta HTTP
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="suppliers.csv"'

        # BOM UTF-8 → evita caracteres raros en Excel
        response.write('\ufeff')

        writer = csv.writer(response, delimiter=';', quoting=csv.QUOTE_MINIMAL)

        # Cabeceras del archivo
        writer.writerow([
        'Suplier ID',
        'Legal Name',
        'Name',
        'Tax ID',
        'Country',
        'State/Province',
        'City',
        'Address',
        'Zip Code',
        'Phone',
        'Email',
        'Contact name',
        'Contact role',
        'Category',
        'Payment terms',
        'Currency',
        'Payment method',
        'Bank account',
        'Status',
        'Created By',
        'Created At',
        'Updated At'
        ])

        # Filas con datos
        for supplier in supplier_list:
            writer.writerow([
                supplier.id_supplier or '',
                supplier.legal_name or '',
                supplier.name or '',
                supplier.tax_id or '',
                supplier.country or '',
                supplier.state_province or '',
                supplier.city or '',
                supplier.address or '',
                supplier.zip_code or '',
                supplier.phone or '',
                supplier.email or '',
                supplier.contact_name or '',
                supplier.contact_role or '',
                supplier.category or '',
                supplier.payment_terms or '',
                supplier.currency or '',
                supplier.payment_method or '',
                supplier.bank_account or '',
                supplier.status or '',
                supplier.created_by.username if supplier.created_by else 'N/A',
                supplier.created_at.strftime('%Y-%m-%d %H:%M:%S') if supplier.created_at else '',
                supplier.updated_at.strftime('%Y-%m-%d %H:%M:%S') if supplier.updated_at else '',
            ])

        return response

    paginator = Paginator(supplier_list,10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'suppliers/suppliers_list.html', {
    'page_obj': page_obj,
    'permissions': {'suppliers': max_permission},  
})


@login_required
def suppliers_create(request):

    max_permission = UserRole.objects.filter(user_id=request.user).aggregate(max_permission=models.Max('role__suppliers'))['max_permission'] or 0

    if max_permission == 1:
        return redirect('suppliers')
    if max_permission == 0:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():

            supplier = form.save(commit=False)
            supplier.created_by =request.user
            supplier.save()

            return redirect('suppliers:suppliers_create')
    else:
        form = SupplierForm()
        
    return render(request, 'suppliers/suppliers_form.html', {'form': form})

@login_required
def suppliers_edit(request,pk):

    supplier = get_object_or_404(Supplier,pk=pk)

    max_permission = UserRole.objects.filter(user_id=request.user).aggregate(max_permission=models.Max('role__suppliers'))['max_permission'] or 0

    if max_permission == 1:
        return redirect('suppliers')
    if max_permission == 0:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect('suppliers:suppliers_list')
    else:
        form = SupplierForm(instance=supplier)

    context = {
        'form': form,
        'supplier': supplier,
    }

    return render(request, 'suppliers/suppliers_form.html', context)


@login_required
def suppliers_delete(request,pk):

    max_permission = UserRole.objects.filter(user_id=request.user).aggregate(max_permission=models.Max('role__suppliers'))['max_permission'] or 0

    if max_permission <2:
        return redirect('supplier:supplier_list')
    
    supplier = get_object_or_404(Supplier,pk=pk)

    if request.method == 'POST':
        supplier.delete()
        return redirect('suppliers:suppliers_list')
    
    return redirect('suppliers:suppliers_list')
