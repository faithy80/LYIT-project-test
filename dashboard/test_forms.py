from django.test import TestCase
from .forms import SiteSettingsForm


class SiteSettingsFormTestCase(TestCase):
    
    def test_SiteSettingsForm(self):
        print('\nTesting SiteSettingsForm...')

        # Creating a valid form
        valid_form = SiteSettingsForm(
            {
                'temp_limit' : 23.0,
                'temp_offset' : 0.5,
                'auto_mode' : True,
            },
        )

        # Creating an invalid form
        invalid_form = SiteSettingsForm(
            {
                'temp_limit' : 'String',
                'temp_offset' : 'other srtings',
                'auto_mode' : 'third string',
            },
        )

        # Test if the form valid
        self.assertTrue(valid_form.is_valid())

        # Test if the form invalid
        self.assertFalse(invalid_form.is_valid())
