# Generated by Django 4.0 on 2024-02-01 12:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_user_searchs'),
    ]

    operations = [
        migrations.CreateModel(
            name='user_orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordered_item', models.CharField(max_length=30, null=True)),
                ('order_status', models.CharField(max_length=10, null=True)),
                ('ordered_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.user')),
            ],
        ),
    ]