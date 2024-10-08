# Generated by Django 3.2 on 2024-09-01 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0013_auto_20240901_1501'),
    ]

    operations = [
        migrations.CreateModel(
            name='CouplePoints',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('staff_number', models.CharField(max_length=100)),
                ('spouse_id', models.CharField(max_length=100)),
                ('couple_points', models.IntegerField()),
                ('total_points', models.IntegerField()),
                ('date_calculated', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
