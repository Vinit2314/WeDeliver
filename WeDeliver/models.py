import os
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from PIL import Image
from django.conf import settings

def pic(instance, filename):
    profile_pic_name = 'user_{0}/profile.jpg'.format(instance.user.id)
    full_path = os.path.join(settings.MEDIA_ROOT, profile_pic_name)

    if os.path.exists(full_path):
        os.remove(full_path)

    return profile_pic_name

class order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pickup_point_name = models.CharField(max_length=50)
    pickup_point_address = models.CharField(max_length=100)
    pickup_point_phone_number = models.CharField(max_length=10)
    delivery_point_name = models.CharField(max_length=50)
    delivery_point_address = models.CharField(max_length=100)
    delivery_point_phone_number = models.CharField(max_length=10)
    quantity = models.CharField(max_length=10)
    mode_of_payment = models.CharField(max_length=20,)
    amount = models.IntegerField()  
    order_id = models.CharField(max_length=20, unique=True)
    flag = models.CharField(max_length=2, choices=(('CM' , 'Completed'),
                                                    ('P', 'Pending'),
                                                    ('C', 'Canceled')))
    payment = models.CharField(max_length=10, choices=(('Pending' , 'Pending'),
                                                       ('Done' ,'Done'),
                                                       ('Cancel' ,'Cancel'),
                                                       ('Refund' ,'Refund'),))
    type = models.CharField(max_length=10)                                

class contactus(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    message = models.CharField(max_length=500)

class profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone_no = models.CharField(max_length=10, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(default='default.jpg', upload_to=pic, null=True, blank=True)
    phone_no_verification = models.CharField(max_length=2, choices=(('V', 'Verified'),
                                                                    ('NV', 'Not Verified')), default='NV')
    email_verification = models.CharField(max_length=2, choices=(('V', 'Verified'),
                                                                    ('NV', 'Not Verified')), default='NV')
    phone_no_otp = models.IntegerField(null=True, blank=True)
    email_otp = models.IntegerField(null=True, blank=True)
    verified_phone_no = models.CharField(max_length=10, null=True, blank=True)
    verified_email = models.EmailField(null=True, blank=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, *args, **kwargs):
	    if created:
	    	profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, *args, **kwargs):
	    instance.profile.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)

        if self.image:
            output_size = 200   , 200
            img.thumbnail(output_size)
            img.save(self.image.path)

class price(models.Model):
    document_price = models.FloatField()
    food_price = models.FloatField()
    package_price = models.FloatField()