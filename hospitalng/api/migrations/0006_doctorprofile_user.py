# Generated by Django 3.2.12 on 2022-04-03 19:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_doctorprofile_profile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctorprofile',
            name='user',
            field=models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, to='api.user'),
            preserve_default=False,
        ),
    ]