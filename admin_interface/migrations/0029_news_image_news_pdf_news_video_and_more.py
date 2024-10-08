# Generated by Django 4.2.13 on 2024-07-28 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_interface', '0028_userdata_showgithubuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='image',
            field=models.ImageField(blank=True, upload_to='news_images'),
        ),
        migrations.AddField(
            model_name='news',
            name='pdf',
            field=models.FileField(blank=True, default='', upload_to='news_pdfs'),
        ),
        migrations.AddField(
            model_name='news',
            name='video',
            field=models.FileField(blank=True, default='', upload_to='news_videos'),
        ),
        migrations.AlterField(
            model_name='userdata',
            name='view_news',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
    ]
