# Generated by Django 4.2.13 on 2024-07-23 10:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_interface', '0016_gitlab_id_remove_userdata_gitlab_id'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='gitlab_id',
            new_name='gitlab_ids',
        ),
    ]