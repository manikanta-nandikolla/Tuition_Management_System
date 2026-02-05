from django.urls import path
from . import views

app_name = "students"

urlpatterns = [
    path('', views.student_list, name='list'),
    path('add/', views.student_create, name='add'),
    path('edit/<int:pk>/', views.student_update, name='edit'),
    path('delete/<int:pk>/', views.student_delete, name='delete'),
]
