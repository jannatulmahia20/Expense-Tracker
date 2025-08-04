from django.urls import path
from . import views



urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add/', views.add_expense, name='add_expense'),
    path('edit/<int:pk>/', views.edit_expense, name='edit_expense'),
    path('delete/<int:pk>/', views.delete_expense, name='delete_expense'),
    path('set-budget/', views.set_budget, name='set_budget'),
    path('monthly-history/', views.monthly_history, name='monthly_history'),
    path('edit-budget/<int:pk>/', views.edit_budget, name='edit_budget'),



]
