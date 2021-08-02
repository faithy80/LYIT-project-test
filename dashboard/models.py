from django.db import models

class TempHistory(models.Model):
    """
    Model definition for temperature history
    """

    temp_data = models.FloatField('Temperature')
    temp_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Temperature'
        verbose_name_plural = 'Temperatures'

    def __str__(self):
        """
        Unicode representation of temperature history
        """

        return str(self.temp_date)
