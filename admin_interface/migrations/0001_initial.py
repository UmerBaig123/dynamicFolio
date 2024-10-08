# Generated by Django 4.2.13 on 2024-07-18 12:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='news',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('news_date', models.DateField()),
                ('news_description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='publication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('publication_image', models.ImageField(blank=True, upload_to='publication_images')),
                ('title', models.CharField(max_length=100)),
                ('authors', models.CharField(max_length=100)),
                ('publication_date', models.DateField()),
                ('publication_url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='selected_repos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('repo_id', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='userdata',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_pic', models.ImageField(blank=True, upload_to='profile_pics')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('github_username', models.CharField(max_length=100)),
                ('linkedin_url', models.URLField()),
                ('qualification', models.TextField()),
                ('view_news', models.BooleanField(default=True)),
                ('summary', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='publicationLinks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link_name', models.CharField(max_length=100)),
                ('link', models.URLField()),
                ('publication', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_interface.publication')),
            ],
        ),
    ]
