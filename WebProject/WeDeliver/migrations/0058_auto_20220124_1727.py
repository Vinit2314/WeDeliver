# Generated by Django 3.2.4 on 2022-01-24 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WeDeliver', '0057_auto_20220124_1722'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='email_verification',
            field=models.CharField(choices=[('V', 'Verified'), ('NV', 'Not Verified')], max_length=225, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone_no_verification',
            field=models.CharField(choices=[('V', 'Verified'), ('NV', 'Not Verified')], max_length=225, null=True),
        ),
    ]
