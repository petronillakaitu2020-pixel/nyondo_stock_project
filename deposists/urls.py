from django.urls import path

from . import views


urlpatterns = [

    path('',views.deposit_list, name='deposit_list'),
    path('<int:id>/', views.deposit_detail, name='deposit_detail'),
    path('payment/<int:id>/', views.add_payment, name='add_payment'),
    path('delete/<int:id>/', views.delete_deposit, name='delete_deposit'),
    path('receipt/<int:id>/', views.payment_receipt, name='payment_receipt'),
]