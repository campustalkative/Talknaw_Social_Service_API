# Generated by Django 4.2.4 on 2023-09-29 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.CharField(blank=True, default='', max_length=1000),
        ),
    ]
