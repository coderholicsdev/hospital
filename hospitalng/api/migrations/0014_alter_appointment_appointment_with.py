# Generated by Django 3.2.12 on 2022-04-06 07:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_auto_20220406_0749'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='appointment_with',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='api.patientprofile'),
        ),
    ]