# Generated by Django 3.2.9 on 2021-12-01 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='erauser',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
