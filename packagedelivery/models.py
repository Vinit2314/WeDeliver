from django.db import models

class login_form(models.Model):
    user_name = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    remember_me = models.BooleanField()

class order(models.Model):
    pickup_point_name = models.CharField(max_length=50)
    pickup_point_address = models.CharField(max_length=100)
    pickup_point_phone_number = models.CharField(max_length=10)
    delivery_point_name = models.CharField(max_length=50)
    delivery_point_address = models.CharField(max_length=100)
    delivery_point_phone_number = models.CharField(max_length=10)
    weight = models.CharField(max_length=2)
    mode_of_payment = models.CharField(max_length=20,)
    amount = models.IntegerField()  
    order_id = models.CharField(max_length=20, unique=True)