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
    weight = models.CharField(max_length=2, choices=[('1', 'Up to 1 kg'),
                                                     ('5', 'Up to 5 kg'),
                                                     ('10', 'Up to 10 kg'),
                                                     ('15', 'Up to 15 kg'),
                                                     ('20', 'Up to 20 kg')])
    mode_of_payemnt = models.CharField(max_length=20, choices=[('Credit/Debit Card', 'Credit/Debit Card'),
                                                              ('Net-Banking','Net-Banking'),
                                                              ('UPI/QR','UPI/QR'),
                                                              ('Pay on Delivery', 'Pay on Delivery')])
    amount = models.IntegerField()  

    order_id = models.CharField(max_length=20
    )