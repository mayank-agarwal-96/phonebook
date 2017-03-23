from __future__ import unicode_literals

from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User


class Contact(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=50)
    phone = PhoneNumberField()
    email = models.EmailField(max_length=100)

    def __str__(self):
    	return self.name