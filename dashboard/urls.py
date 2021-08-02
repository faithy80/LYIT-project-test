from django.urls import path, include
from .views import dashboard

urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('accounts/profile/', dashboard, name='dashboard'),
]