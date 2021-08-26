from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.shortcuts import reverse
from .models import TempHistory, SiteSettings


class DashboardViewsTestCase(TestCase):
    
    def setUp(self):
       
        # Initialising client
        self.client = Client()

        # Creating an admin user
        admin = User.objects.create_superuser(username='admin')
        admin.set_password('12345')
        admin.save()

        # Creating site settings
        settings = SiteSettings.load()

        # Authenticating admin user
        self.client.login(username='admin', password='12345')

    def test_dashboard(self):
        
        # Creating a temperature data
        TempHistory.objects.create(
            temp_data= 23.5,
        )

        # Send a get request to the dashboard page
        response = self.client.get(reverse('dashboard'))

        # Test if the response is OK
        self.assertEquals(response.status_code, 200)

        # Test if the dashboard.html template was used for rendering the dashboard page
        self.assertTemplateUsed(response, 'dashboard.html')

    def test_save_site_settings_post_request(self):

        # Send data in a post request to the function
        response = self.client.post(
            reverse('save_site_settings'),
            {
                'temp_limit' : 23.0,
                'temp_offset' : 0.5,
                'auto_mode' : True,
            }
        )

        # Test if the function redirects to dashboard when finished
        self.assertRedirects(response, reverse('dashboard'))

        # Test if the site settings changed
        new_settings = SiteSettings.objects.filter(pk=1).values()

        # Fetch and test the values
        # The new settings will differ from the old ones
        for data in new_settings:
            self.assertEquals(data['temp_limit'], 23.0)
            self.assertEquals(data['temp_offset'], 0.5)
            self.assertEquals(data['auto_mode'], True)

    def test_save_site_settings_get_request(self):

        # Send data in a get request to the function
        response = self.client.get(
            reverse('save_site_settings'),
            {
                'temp_limit' : 23.0,
                'temp_offset' : 0.5,
                'auto_mode' : True,
            }
        )

        # Test if the function redirects to dashboard when finished
        self.assertRedirects(response, reverse('dashboard'))

        # Test if the site settings changed
        new_settings = SiteSettings.objects.filter(pk=1).values()

        # Fetch and test the values
        # The old settings will remain unchanged
        for data in new_settings:
            self.assertEquals(data['temp_limit'], 20.0)
            self.assertEquals(data['temp_offset'], 1.0)
            self.assertEquals(data['auto_mode'], False)

    def test_relay_on_post_request(self):

         # Send data in a post request to the function
        response = self.client.post(
            reverse('relay_on')
        )

        # Test if the function redirects to dashboard when finished
        self.assertRedirects(response, reverse('dashboard'))

        # Test if the site settings changed
        new_settings = SiteSettings.objects.filter(pk=1).values()

        # Fetch and test the values
        # The relay state will be changed to True
        for data in new_settings:
            self.assertTrue(data['relay_state'], True)

    def test_relay_on_post_request(self):

         # Send data in a get request to the function
        response = self.client.get(
            reverse('relay_on')
        )

        # Test if the function redirects to dashboard when finished
        self.assertRedirects(response, reverse('dashboard'))

        # Test if the site settings changed
        new_settings = SiteSettings.objects.filter(pk=1).values()

        # Fetch and test the values
        # The relay state will remain unchanged
        for data in new_settings:
            self.assertFalse(data['relay_state'], True)
