from django.urls import path
from .views import *

urlpatterns = [
    path('', ImportProductsView.as_view(), name='imports'),
    path('sales/', SalesView.as_view(), name='sales'),
    path('import-product/<int:pk>/edit/', ImportProducEditView.as_view(), name='import-product-edit'),
    path('client-debt-payments/', PayDebtsView.as_view(), name='pay-debts'),
    path('pay-debts/edit/<int:pk>/', edit_pay_debt, name='edit-pay-debt'),

]
