# Generated by Django 3.2.4 on 2021-10-03 12:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('WeDeliver', '0003_delete_sign_up'),
    ]

    operations = [
        migrations.DeleteModel(
            name='login',
        ),
    ]