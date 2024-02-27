# Generated by Django 5.0 on 2023-12-27 11:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicine', '0004_remove_medicine_box_size_remove_medicine_cost_price_and_more'),
        ('stocks', '0003_remove_stocks_medicine_name_stocks_last_purchase'),
    ]

    operations = [
        migrations.AddField(
            model_name='stocks',
            name='medicine_name',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='medicine.medicine'),
            preserve_default=False,
        ),
    ]
