# Generated by Django 2.1.7 on 2019-03-21 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codenamez', '0017_auto_20190321_2235'),
    ]

    operations = [
        migrations.RenameField(
            model_name='game',
            old_name='board',
            new_name='cards',
        ),
        migrations.AddField(
            model_name='game',
            name='current_clue',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='current_round',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='current_team',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='winner',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
