# Generated by Django 2.1.7 on 2019-03-20 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codenamez', '0011_auto_20190320_1400'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameplayer',
            name='is_spymaster',
            field=models.BooleanField(default=False),
        ),
    ]
