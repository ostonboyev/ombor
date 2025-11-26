from django.urls import path
from main.views import *

urlpatterns = [
   path('', Home, name='home'),
   path('sections/', Sectionsview.as_view(), name='sections'),
   path('products/', ProductsView.as_view(), name='products'),
   path('products/<int:pk>/update/', ProductUpdateview.as_view(), name='product-update'),
   path('products/<int:pk>/delete/', DeleteProductView.as_view(), name='delete_product'),
   path('clients/', ClientsView.as_view(), name='clients'),
   path('clients/<int:pk>/edit/', CliendUpdateview.as_view(), name='client-edit'),
   path('clients/<int:pk>/delete/', DeleteCliendView.as_view(), name='delete-cliend'),

]