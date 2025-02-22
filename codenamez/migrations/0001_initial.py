# Generated by Django 2.1.7 on 2019-03-22 06:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import time
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('created', models.FloatField(default=time.time)),
                ('visible', models.BooleanField(default=True)),
                ('deleted', models.BooleanField(default=False)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=128)),
                ('password', models.CharField(blank=True, editable=False, max_length=128, null=True)),
                ('max_players', models.IntegerField()),
                ('current_team', models.IntegerField(blank=True, null=True)),
                ('current_round', models.IntegerField(blank=True, null=True)),
                ('current_clue', models.CharField(default={}, max_length=128)),
                ('cards', models.TextField(default='{}')),
                ('winner', models.IntegerField(blank=True, null=True)),
                ('created', models.FloatField(default=time.time)),
                ('started', models.FloatField(blank=True, null=True)),
                ('ended', models.FloatField(blank=True, null=True)),
                ('cancelled', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GamePlayer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.IntegerField(default=0)),
                ('team', models.IntegerField(default=0)),
                ('joined', models.FloatField(blank=True, null=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_spymaster', models.BooleanField(default=False)),
                ('locked_in', models.BooleanField(default=False)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='codenamez.Game')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PrivateMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('created', models.FloatField(default=time.time)),
                ('visible', models.BooleanField(default=True)),
                ('deleted', models.BooleanField(default=False)),
                ('target', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='target_pm_set', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_pm_set', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ipaddress', models.GenericIPAddressField()),
                ('avatar', models.ImageField(blank=True, upload_to='profile_images')),
                ('options', models.TextField(default='null')),
                ('games_won', models.IntegerField(default=0)),
                ('games_lost', models.IntegerField(default=0)),
                ('games_played', models.IntegerField(default=0)),
                ('ranking', models.IntegerField(default=1000)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WordList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=128)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='gameplayer',
            unique_together={('game', 'user')},
        ),
    ]
