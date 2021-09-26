# Generated by Django 3.2.4 on 2021-09-26 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('packagedelivery', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pickup_point_name', models.CharField(max_length=50)),
                ('pickup_point_address', models.CharField(max_length=50)),
                ('pickup_point_phone_number', models.CharField(max_length=10)),
                ('delivery_point_name', models.CharField(max_length=50)),
                ('delivery_point_address', models.CharField(max_length=50)),
                ('delivery_point_phone_number', models.CharField(max_length=10)),
                ('weight', models.BooleanField()),
                ('mode_of_payemnt', models.BooleanField()),
                ('amount', models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='login_form',
            name='remember_me',
            field=models.BooleanField(),
        ),
    ]