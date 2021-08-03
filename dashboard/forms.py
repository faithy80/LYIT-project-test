from django import forms
from .models import SiteSettings


class SiteSettingsForm(forms.ModelForm):
    """
    A form to change site settings
    """

    class Meta:
        model = SiteSettings
        fields = ['temp_limit', 'temp_offset', 'auto_mode']
