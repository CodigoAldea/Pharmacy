# Generated by Django 5.0.1 on 2024-01-19 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0023_invoice_date_entry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='date_entry',
            field=models.DateField(auto_now_add=True, help_text='Date of invoice entry', null=True),
        ),
    ]
