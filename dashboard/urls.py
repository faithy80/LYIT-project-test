from django.urls import path, include
from .views import dashboard,save_site_settings

urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('accounts/profile/', dashboard, name='dashboard'),
    path('accounts/profile/save', save_site_settings, name='save_site_settings'),
]
