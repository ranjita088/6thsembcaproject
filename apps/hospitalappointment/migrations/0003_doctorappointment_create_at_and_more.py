# Generated by Django 4.0.2 on 2022-05-03 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospitalappointment', '0002_doctorappointment_done'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctorappointment',
            name='create_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='doctorappointment',
            name='uodate_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
