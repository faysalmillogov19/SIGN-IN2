# Generated by Django 3.2.5 on 2022-03-16 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('csrgenerator', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cert',
            name='decrypt',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
