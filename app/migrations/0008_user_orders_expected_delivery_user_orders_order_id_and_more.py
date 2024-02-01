# Generated by Django 4.0 on 2024-02-01 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_user_orders'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_orders',
            name='expected_delivery',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='user_orders',
            name='order_id',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='user_orders',
            name='ordered_date',
            field=models.CharField(max_length=10, null=True),
        ),
    ]