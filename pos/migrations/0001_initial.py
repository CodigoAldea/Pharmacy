# Generated by Django 5.0 on 2023-12-25 15:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('medicine', '0003_remove_medicine_unit_alter_medicine_strength'),
        ('stocks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medicine_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medicine.medicine')),
            ],
        ),
        migrations.CreateModel(
            name='POS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.customer')),
            ],
        ),
        migrations.CreateModel(
            name='OrderPOS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('unit', models.CharField(max_length=30)),
                ('batch_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stocks.batch')),
                ('medicine_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pos.order')),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pos.pos')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='order_id',
            field=models.ManyToManyField(through='pos.OrderPOS', to='pos.pos'),
        ),
    ]
