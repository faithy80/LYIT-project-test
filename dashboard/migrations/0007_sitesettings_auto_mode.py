# Generated by Django 3.2.5 on 2021-08-02 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_alter_sitesettings_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='auto_mode',
            field=models.BooleanField(default=False, verbose_name='Automatic mode'),
        ),
    ]
