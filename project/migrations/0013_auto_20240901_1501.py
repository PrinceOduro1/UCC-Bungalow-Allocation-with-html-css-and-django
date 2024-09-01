# Generated by Django 3.2 on 2024-09-01 15:01

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0012_auto_20240829_1448'),
    ]

    operations = [
        migrations.CreateModel(
            name='designation_point_junior',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_name', models.CharField(max_length=100)),
                ('point', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='junior_staff_appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('staff_number', models.CharField(max_length=100)),
                ('department', models.CharField(max_length=100)),
                ('mobile_no', models.IntegerField()),
                ('dateOf_Uni_Appointment', models.DateField(default=datetime.date.today)),
                ('presentUni_bungalow', models.CharField(max_length=100)),
                ('designation_point', models.IntegerField(default=0)),
                ('marital_status', models.CharField(choices=[('single', 'Single'), ('married', 'Married'), ('none', 'None')], default='Single', max_length=50)),
                ('spouse_id', models.CharField(blank=True, max_length=100, null=True)),
                ('num_of_children', models.IntegerField()),
                ('total_points', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='appointment',
            name='total_points',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='senior_staff_appointment',
            name='spouse_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.CreateModel(
            name='Preference_junior_staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preference', models.CharField(default='sn1', max_length=255)),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='preference_set', to='project.junior_staff_appointment')),
            ],
        ),
        migrations.CreateModel(
            name='assign_point_and_preference_junior',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preference_assigned', models.CharField(blank=True, max_length=255, null=True)),
                ('total_points', models.IntegerField(default=0)),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assigned_point_and_preference_set', to='project.junior_staff_appointment')),
            ],
        ),
    ]
