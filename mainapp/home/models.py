from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken



class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, first_name,password, **other_fields):
        other_fields.setdefault('is_staff',True)
        other_fields.setdefault('is_superuser',True)
        other_fields.setdefault('is_active',True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Super User must be Staff')

        if other_fields.get('is_superuser') is not True:
            raise ValueError('Super User must be true')

        if other_fields.get('is_active') is not True:
            raise ValueError('Super User must be active')

        return self.creat_user(email,first_name,password, **other_fields)

    def creat_user(self,email, first_name,password, **other_fields):

        if not email:
            raise ValueError('Email must be provided')

        if not first_name:
            raise ValueError('First name must be provided')

        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, **other_fields)
        user.set_password(password)
        user.save()
        return user






class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    ref_code = models.CharField(max_length=20, default='')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)


    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']


    def __str__(self):
        return self.email

    def tokens(self):
        refresh_token = RefreshToken.for_user(self)
        return {
            'refresh':str(refresh_token),
            'access':str(refresh_token.access_token)
        }






class LandingPage(models.Model):
    landing_email = models.EmailField(unique=True)
    ref_code = models.CharField(max_length=20, default='')
    verified = models.BooleanField(default=False)
    referred_code = models.CharField(max_length=20,default='')

    def __str__(self):
        return self.landing_email




class Points(models.Model):
    user = models.ForeignKey(LandingPage,on_delete=models.CASCADE)
    points = models.IntegerField()


    def __str__(self):
        return self.user.landing_email




class Referral(models.Model):
    referral = models.ForeignKey(LandingPage,on_delete=models.CASCADE, related_name='referral')
    author = models.ForeignKey(LandingPage, on_delete=models.CASCADE, related_name='author')

    def __str__(self):
        return self.author.landing_email

class  ContactUs(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name