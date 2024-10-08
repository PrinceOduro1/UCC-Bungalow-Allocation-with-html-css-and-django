# Generated by Django 5.0 on 2024-08-27 20:28

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0007_alter_preference_preference'),
    ]

    operations = [
        migrations.CreateModel(
            name='designation_point',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_name', models.CharField(max_length=100)),
                ('point', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='senior_staff_appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('staff_number', models.CharField(max_length=100)),
                ('department', models.CharField(max_length=100)),
                ('mobile_no', models.IntegerField()),
                ('dateOf_Uni_Appointment', models.DateField(default=datetime.date.today)),
                ('presentUni_bungalow', models.CharField(max_length=100)),
                ('date_of_occupation_ofAccomodation', models.DateField(blank=True, null=True)),
                ('designation_point', models.IntegerField(default=0)),
                ('marital_status', models.CharField(choices=[('single', 'Single'), ('married', 'Married'), ('none', 'None')], default='Single', max_length=50)),
                ('num_of_children', models.IntegerField()),
                ('total_points', models.IntegerField(default=0)),
                ('present_accommodation', models.CharField(choices=[('Senior staff university accommodation', 'Senior staff university accommodation'), ('Junior staff bungalow', 'Junior Staff Bungalow'), ('not_accommodated', 'Not Accommodated')], default='Not Accomodated', max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='preference',
            name='application',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='preference_set', to='project.appointment'),
        ),
        migrations.CreateModel(
            name='assign_point_and_preference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preference_assigned', models.CharField(blank=True, max_length=255, null=True)),
                ('total_points', models.IntegerField(default=0)),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assigned_point_and_preference_set', to='project.appointment')),
            ],
        ),
        migrations.CreateModel(
            name='Preference_senior_staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preference', models.CharField(default='sn1', max_length=255)),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='preference_set', to='project.senior_staff_appointment')),
            ],
        ),
    ]
