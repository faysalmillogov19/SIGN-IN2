# Generated by Django 3.2.5 on 2022-04-06 12:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cryptographie', '0003_remove_signataire_document'),
    ]

    operations = [
        migrations.AddField(
            model_name='signataire',
            name='document',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='cryptographie.document'),
            preserve_default=False,
        ),
    ]
