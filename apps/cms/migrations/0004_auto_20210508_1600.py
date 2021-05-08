# Generated by Django 3.1.7 on 2021-05-08 08:00

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0003_clothesorder'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clothesorder',
            name='uid',
        ),
        migrations.AddField(
            model_name='clothesorder',
            name='id',
            field=models.AutoField(auto_created=True, default=django.utils.timezone.now, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]
