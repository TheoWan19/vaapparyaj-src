from django.urls import path
from . import views

urlpatterns = [ 
    path('', views.HomeView.as_view(), name='home'),
    path('add-client', views.AddClientView.as_view(), name='add-client'),
    path('add-invoice', views.AddInvoiceView.as_view(), name='add-invoice'),
    path('view-invoice/<int:pk>', views.InvoiceVisualizationView.as_view(), name='view-invoice'),
    path('invoice-pdf/<int:pk>', views.get_invoice_pdf, name="invoice-pdf"),
    path('invoice-live', views.invoice_live, name='invoice-live'),
    path('team/<int:pk>', views.team_details, name='team'),
]