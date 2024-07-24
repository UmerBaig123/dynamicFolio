# Generated by Django 4.2.13 on 2024-07-23 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_interface', '0015_selected_gitlab_repos_userdata_gitlab_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='gitlab_id',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gitlab_id', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='userdata',
            name='gitlab_id',
        ),
    ]