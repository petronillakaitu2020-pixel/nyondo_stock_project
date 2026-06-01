from django.urls import path
from . import views


urlpatterns = [
    path('',views.sales_list, name='sales_list'),
    path('create/', views.create_sale, name='create_sale'),
    path('sales/<int:sale_id>/', views.add_sale_items, name='add_sale_items'),
    path('receipt/<int:sale_id>/', views.sale_receipt, name='sale_receipt'),
    path('sale/<int:sale_id>/finalise/', views.finalise_sale, name='finalise_sale'),
]