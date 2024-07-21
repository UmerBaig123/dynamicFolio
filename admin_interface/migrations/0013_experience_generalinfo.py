# Generated by Django 4.2.13 on 2024-07-21 08:00

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('admin_interface', '0012_remove_courses_course_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='experience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('experience_from_year', models.IntegerField()),
                ('experience_to_year', models.IntegerField()),
                ('experience_name', models.CharField(default='', max_length=100)),
                ('experience_type', models.CharField(default='', max_length=100)),
                ('experience_place', models.TextField(default='')),
                ('experience_description', models.TextField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='generalInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_birth', models.DateField(default=django.utils.timezone.now)),
                ('languages', models.TextField(default='Languages')),
                ('cv', models.FileField(blank=True, default='', upload_to='cv')),
                ('phone', models.CharField(default='Phone', max_length=100)),
                ('hobbies', models.TextField(default='')),
            ],
        ),
    ]
