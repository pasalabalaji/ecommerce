# Generated by Django 4.0 on 2023-11-11 18:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_cart_cartref_alter_profile_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='pid',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='rating',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='mobile_number',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='premium',
            field=models.CharField(max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='cost',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='details',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.CreateModel(
            name='user_products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pid', models.CharField(max_length=10)),
                ('uid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.user')),
            ],
        ),
    ]