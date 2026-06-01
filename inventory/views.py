from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

from .models import Product
from .forms import ProductForm


def product_list(request):
    products = Product.objects.all().order_by('-created_at')
    total_products = products.count()
    low_stock_products = products.filter(quantity__lt=10)

    context = {
        'products': products,  
        'total_products': total_products,
        'low_stock_products': low_stock_products,   
    }
    return render(request, 'product_list.html', context)


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = request.user
            product.available_stock = product.quantity
            product.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})


def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk) 
    if request.method == 'POST':
        form = ProductForm(request.POST or None, instance=product)
        if form.is_valid():
            updated_product = form.save(commit=False)
        # maintain creator
            updated_product.created_by = product.created_by
            updated_product.available_stock = updated_product.quantity
            updated_product.save()
        return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, "edit_product.html", {'form':form})


def delete_product(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == "POST":
        product.delete()
    return redirect('product_list')


def product_detail(request, id):
    product = get_object_or_404(Product,id=id)
    return render(request,'product_detail.html',{'product': product})


def low_stock_products(request):
    products = Product.objects.filter( quantity__lt=10)
    return render(request,'low_stock.html', {'products': products})