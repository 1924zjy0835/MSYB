# Generated by Django 3.1.7 on 2021-05-14 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0004_auto_20210509_1728'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('thumbnail', models.URLField()),
            ],
            options={
                'db_table': 'models',
            },
        ),
    ]
