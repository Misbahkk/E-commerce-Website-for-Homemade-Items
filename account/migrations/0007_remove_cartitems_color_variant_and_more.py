# Generated by Django 5.1.3 on 2024-12-11 13:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_cart_payment_date_cart_payment_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitems',
            name='color_variant',
        ),
        migrations.RemoveField(
            model_name='cartitems',
            name='size_variant',
        ),
    ]
