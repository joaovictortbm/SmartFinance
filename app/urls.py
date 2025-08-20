from django.contrib import admin
from django.urls import path
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('authentication.urls')),
    path('', include('users.urls')),
    path('', include('income.urls')),
    path('', include('expense.urls')),
]
