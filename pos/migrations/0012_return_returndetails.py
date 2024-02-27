# Generated by Django 5.0 on 2024-01-08 07:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0011_alter_pos_date_entry'),
    ]

    operations = [
        migrations.CreateModel(
            name='Return',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_no', models.CharField(max_length=50)),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='ReturnDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inv_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pos.return', verbose_name='invoice number')),
            ],
        ),
    ]