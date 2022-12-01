from django.db import models
from django.conf import settings
from cloudinary.models import CloudinaryField


class Property(models.Model):
    name = models.CharField(max_length=200)
    property_pics = CloudinaryField('image', blank=True)
    price = models.IntegerField()
    deposits = models.IntegerField()
    stage = models.CharField(default="Interest", max_length=100)
    project_return = models.IntegerField()
    location = models.CharField(max_length=200)
    time_left = models.IntegerField()
    roi = models.IntegerField()

    def __str__(self):
        return self.name


class OwnedProp(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    shares = models.IntegerField(default=0)
    deposit = models.IntegerField(default=0)
    funded_stage = models.BooleanField(default=False)


    def __str__(self):
        return self.property.name






class MoneySpent(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    amount = models.IntegerField()

    def __str__(self):
        return self.user


class Returns(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    amount = models.IntegerField()

    def __str__(self):
        return self.user
