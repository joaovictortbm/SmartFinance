from django.urls import path
from .views import ExpenseDetailView, ExpenseListCreateView, ExpenseDashboardView

urlpatterns = [
    path('expense/', ExpenseListCreateView.as_view(), name='expense-list-create'),
    path('expense/<int:pk>/', ExpenseDetailView.as_view(), name='expense-detail'),
    path('expense/dashboard/', ExpenseDashboardView.as_view(), name='dashboard'),
]
