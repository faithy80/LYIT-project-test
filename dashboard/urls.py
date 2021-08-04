from django.urls import path, include
from .views import dashboard, save_site_settings, relay_off, relay_on


urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('accounts/profile/', dashboard, name='dashboard'),
    path('accounts/profile/save', save_site_settings, name='save_site_settings'),
    path('accounts/profile/relay_on', relay_on, name='relay_on'),
    path('accounts/profile/relay_off', relay_off, name='relay_off'),
]
