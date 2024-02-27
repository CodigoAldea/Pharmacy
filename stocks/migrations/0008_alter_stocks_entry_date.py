# Generated by Django 5.0 on 2023-12-27 17:51

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0007_alter_stocks_entry_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stocks',
            name='entry_date',
            field=models.DateField(blank=True, default=django.utils.timezone.now, null=True),
        ),
    ]
