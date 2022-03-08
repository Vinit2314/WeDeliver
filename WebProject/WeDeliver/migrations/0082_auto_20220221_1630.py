# Generated by Django 3.2.4 on 2022-02-21 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WeDeliver', '0081_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='weight',
            new_name='quantity',
        ),
        migrations.AddField(
            model_name='order',
            name='type',
            field=models.CharField(default='1', max_length=10),
            preserve_default=False,
        ),
    ]