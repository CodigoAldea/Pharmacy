# Generated by Django 5.0.1 on 2024-02-06 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0026_returnpurchase_last_purchase_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='returndetails',
            name='unit',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
