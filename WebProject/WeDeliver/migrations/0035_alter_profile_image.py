# Generated by Django 3.2.4 on 2021-10-26 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WeDeliver', '0034_alter_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='profilepic'),
        ),
    ]
