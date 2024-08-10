# Generated by Django 4.2.13 on 2024-08-10 01:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_interface', '0034_about_me_selected_publications_add_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='google_scholar_article',
            name='pub_date',
        ),
        migrations.AddField(
            model_name='publication',
            name='pub_date',
            field=models.DateField(auto_now=True, null=True),
        ),
    ]
