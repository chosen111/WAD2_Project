# Generated by Django 2.1.7 on 2019-03-19 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codenamez', '0007_auto_20190319_1557'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameplayer',
            name='admin',
            field=models.BooleanField(default=False),
        ),
    ]
