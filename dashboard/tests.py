from django.test import TestCase
from .models import TempHistory, SiteSettings


# Create your tests here.
class TempHistoryTestCase(TestCase):
    
    def test_temp_history_creation(self):
        print('This is a test!')
