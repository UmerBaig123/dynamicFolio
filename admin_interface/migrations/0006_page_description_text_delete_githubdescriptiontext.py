# Generated by Django 4.2.13 on 2024-07-19 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_interface', '0005_githubdescriptiontext'),
    ]

    operations = [
        migrations.CreateModel(
            name='page_description_text',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_name', models.CharField(max_length=100)),
                ('text', models.TextField()),
            ],
        ),
        migrations.DeleteModel(
            name='githubDescriptionText',
        ),
    ]
