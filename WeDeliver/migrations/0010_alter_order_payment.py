# Generated by Django 3.2.4 on 2021-10-12 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WeDeliver', '0009_rename_paymentt_order_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Done', 'Done'), ('Cancel', 'Cancel'), ('Refund', 'Refund')], max_length=10),
        ),
    ]
