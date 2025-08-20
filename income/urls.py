from django.urls import path
from .views import IncomeDetailView, IncomeListCreateView, DashboardView

urlpatterns = [
    path('income/', IncomeListCreateView.as_view(), name='income-list-create'),
    path('income/<int:pk>/', IncomeDetailView.as_view(),
         name='income-detail-update-delete'),
    path('income/dashboard/', DashboardView.as_view(), name='dashboard-view'),
]
