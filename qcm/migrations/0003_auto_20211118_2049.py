# Generated by Django 3.2.9 on 2021-11-18 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qcm', '0002_alter_training_questions_set'),
    ]

    operations = [
        migrations.AlterField(
            model_name='training',
            name='choice_order',
            field=models.CharField(max_length=1500, null=True),
        ),
        migrations.AlterField(
            model_name='training',
            name='questions_answers',
            field=models.CharField(max_length=1500, null=True),
        ),
    ]
