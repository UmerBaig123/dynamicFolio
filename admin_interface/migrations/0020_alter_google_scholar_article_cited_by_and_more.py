# Generated by Django 4.2.13 on 2024-07-24 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_interface', '0019_gs_article_data_google_scholar_article_article_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='google_scholar_article',
            name='cited_by',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='google_scholar_article',
            name='year',
            field=models.IntegerField(null=True),
        ),
    ]