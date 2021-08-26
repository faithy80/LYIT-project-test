from django.test import TestCase
from .models import TempHistory, SiteSettings


class TempHistoryTestCase(TestCase):
    
    def test_temp_history_model(self):
        print('\nTesting TempHistory model...')

        # Creating the object from the model
        model = TempHistory.objects.create(
            temp_data=23.8,
        )

        # Get the created data as a query
        data_query = TempHistory.objects.filter(pk=1).values('temp_data')
        
        # Fetch and test the value
        for data in data_query:
            self.assertEquals(data['temp_data'], 23.8)

        # Test if model is an instance of TempHistory
        self.assertTrue(isinstance(model, TempHistory))

class SiteSettingsTestCase(TestCase):

    def test_site_settings_model(self):
        print('\nTesting SiteSettings model...')

        # Creating the object using the default parameters
        settings = SiteSettings.load()
        
        # Get the created data as a query
        data_query = SiteSettings.objects.filter(pk=1).values()
        
        # Fetch and test each value
        for data in data_query:
            self.assertEquals(data['temp_limit'], 20.0)
            self.assertEquals(data['temp_offset'], 1.0)
            self.assertFalse(data['auto_mode'])
            self.assertFalse(data['relay_state'])

         # Test if model is an instance of SiteSettings
        self.assertTrue(isinstance(settings, SiteSettings))
