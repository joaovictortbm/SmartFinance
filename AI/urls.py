from django.urls import path
from . import views


urlpatterns = [
    path('insights/', views.financialInsightsView.as_view(),
         name='financial-insights'),
]
