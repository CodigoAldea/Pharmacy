# Generated by Django 5.0 on 2024-01-15 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchase', '0005_alter_purchase_details_expiry'),
    ]

    operations = [
        migrations.CreateModel(
            name='YourModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
        ),
    ]
