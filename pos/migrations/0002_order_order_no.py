# Generated by Django 5.0 on 2023-12-25 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_no',
            field=models.CharField(default=0, max_length=50),
            preserve_default=False,
        ),
    ]
