# Generated by Django 3.2.4 on 2021-10-27 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WeDeliver', '0044_auto_20211027_1947'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, default='pic/default.jpg', null=True, upload_to='user_directory_path'),
        ),
    ]
