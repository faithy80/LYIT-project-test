# Generated by Django 3.2.5 on 2021-08-03 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_sitesettings_auto_mode'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='relay_state',
            field=models.BooleanField(default=False, verbose_name='Relay state'),
        ),
    ]
