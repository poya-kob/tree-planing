# Generated by Django 5.1.6 on 2025-03-03 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='treeimage',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
