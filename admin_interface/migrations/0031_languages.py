# Generated by Django 4.2.13 on 2024-08-15 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_interface', '0030_userdata_onload_animation'),
    ]

    operations = [
        migrations.CreateModel(
            name='languages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_name', models.CharField(default='', max_length=100)),
                ('language_proficiency', models.CharField(default='', max_length=100)),
            ],
        ),
    ]
