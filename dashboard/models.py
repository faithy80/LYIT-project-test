from django.db import models

class TempHistory(models.Model):
    """
    Model definition for temperature history
    """

    temp_data = models.DecimalField('Temperature', decimal_places=2, max_digits=2)
    temp_date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Temperature'
        verbose_name_plural = 'Temperatures'

    def __str__(self):
        """
        Unicode representation of temperature history
        """

        return self.temp_date
