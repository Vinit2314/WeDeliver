# Generated by Django 3.2.4 on 2022-02-22 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WeDeliver', '0082_auto_20220221_1630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='quantity',
            field=models.CharField(max_length=10),
        ),
    ]