# Generated by Django 4.0.2 on 2022-05-14 03:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospitalappointment', '0004_rename_uodate_at_doctor_update_at_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contactus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=30)),
                ('Email', models.EmailField(max_length=254)),
                ('Number', models.IntegerField()),
                ('Message', models.TextField(max_length=500)),
            ],
        ),
    ]
