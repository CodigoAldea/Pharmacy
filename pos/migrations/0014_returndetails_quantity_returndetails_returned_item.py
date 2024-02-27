# Generated by Django 5.0 on 2024-01-10 12:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicine', '0004_remove_medicine_box_size_remove_medicine_cost_price_and_more'),
        ('pos', '0013_alter_return_invoice_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='returndetails',
            name='quantity',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='returndetails',
            name='returned_item',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='medicine.medicine'),
            preserve_default=False,
        ),
    ]
