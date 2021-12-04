from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
#  Name, Phone Number, Email Address.
# Create your models here.

class Contact(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    email = models.EmailField(max_length = 255)
    spam = 