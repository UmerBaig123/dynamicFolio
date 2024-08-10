# Generated by Django 4.2.13 on 2024-08-10 01:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_interface', '0036_alter_about_me_selected_publications_add_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='about_me_selected_publications',
            name='add_date',
        ),
        migrations.RemoveField(
            model_name='publication',
            name='pub_date',
        ),
        migrations.AddField(
            model_name='publication',
            name='preference',
            field=models.IntegerField(default=0),
        ),
    ]
