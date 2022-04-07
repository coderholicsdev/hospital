# Generated by Django 3.2.12 on 2022-04-03 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_doctorprofile_hospital_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctorprofile',
            name='profile_picture',
            field=models.ImageField(default='default.jpg', upload_to='doctor/profile_picture'),
            preserve_default=False,
        ),
    ]
