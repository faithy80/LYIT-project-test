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


class SingletonModel(models.Model):
    """
    Abstract definition for a singleton model
    """

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class SiteSettings(SingletonModel):
    """
    Model definition for site settings
    """

    temp_limit = models.FloatField('Temperature limit', default=20.0)
    temp_offset = models.FloatField('Temperature offset', default=1.0)
    auto_mode = models.BooleanField('Automatic mode', default=False)

    class Meta:
        verbose_name = 'Site settings'
        verbose_name_plural = 'Site settings'

    def __str__(self):
        """
        Unicode representation of site settings
        """

        return 'Site settings'
