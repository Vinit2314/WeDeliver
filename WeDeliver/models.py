from django.db import models

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
    username = models.CharField(max_length=20)
    flag = models.CharField(max_length=2, choices=(('CM' , 'Completed'),
                                                    ('P', 'Pending'),
                                                    ('C', 'Canceled')))
    payment = models.CharField(max_length=10, choices=(('Pending' , 'Pending'),
                                                         ('Done' ,'Done')) )                                