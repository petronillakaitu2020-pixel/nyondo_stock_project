from django.urls import path

from . import views


urlpatterns = [

    path(
        '',
        views.supplier_list,
        name='supplier_list'
    ),

    path(
        'add/',
        views.add_supplier,
        name='add_supplier'
    ),

    path(
        'view/<int:id>/',
        views.supplier_detail,
        name='supplier_detail'
    ),

    path(
        'edit/<int:id>/',
        views.edit_supplier,
        name='edit_supplier'
    ),

    path(
        'delete/<int:id>/',
        views.delete_supplier,
        name='delete_supplier'
    ),
path(
    'payment/<int:id>/',
    views.add_supplier_payment,
    name='add_supplier_payment'
),
]