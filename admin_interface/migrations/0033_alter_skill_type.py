# Generated by Django 4.2.13 on 2024-08-15 22:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin_interface', '0032_skill_type_skill'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skill',
            name='type',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='admin_interface.skill_type'),
        ),
    ]