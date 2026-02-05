from django.urls import path
from . import views

app_name = "fees"

urlpatterns = [
    path("", views.fee_list, name="list"),
    path("add/", views.fee_create, name="add"),
    path("receipt/<int:pk>/", views.fee_receipt, name="receipt"),
    path("report/", views.monthly_report, name="report"),
    path("export/", views.export_excel, name="export"),
]
