# Generated by Django 4.0 on 2024-02-05 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_alter_user_orders_expected_delivery_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_orders',
            name='cost',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='user_orders',
            name='expected_delivery',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='user_orders',
            name='order_status',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
