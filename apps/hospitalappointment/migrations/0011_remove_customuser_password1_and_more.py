# Generated by Django 4.0.2 on 2022-05-18 09:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hospitalappointment', '0010_customuser_password1_customuser_password2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='password1',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='password2',
        ),
    ]
