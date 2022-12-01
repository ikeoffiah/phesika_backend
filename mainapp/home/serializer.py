from rest_framework import serializers
from .models import User, LandingPage, User, ContactUs
from django.contrib.auth.password_validation import validate_password
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import generate, Error, send_email,TokenGenerator
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator




#landing page serializer
class LandingSerializer(serializers.ModelSerializer):
    landing_email = serializers.EmailField()

    class Meta:
        model = LandingPage
        fields = ('landing_email',)

    def validate(self, attrs):
        email = attrs.get('landing_email',None)
        if LandingPage.objects.filter(landing_email=email).exists():
            raise serializers.ValidationError("Email has already joined waitlist")

        return attrs



#referral serializer
class ReferralLandingSerializer(serializers.ModelSerializer):
    landing_email = serializers.EmailField()

    class Meta:
        model = LandingPage
        fields = ('landing_email','referred_code',)

    def validate(self, attrs):
        email = attrs.get('landing_email',None)
        if LandingPage.objects.filter(landing_email=email).exists():
            raise serializers.ValidationError("Email has already joined waitlist")

        return attrs



#complete signup serializer
class CompleteSignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    tokens = serializers.CharField(max_length=100, min_length=6, read_only=True)
    password = serializers.CharField(write_only=True, max_length=100, min_length=4, required=True)

    class Meta:
        model = User
        fields = ['email','first_name','password','tokens']

    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email already exists')
        return attrs

    def create(self, validated_data):
        user = User.objects.creat_user(
            email= validated_data['email'],

            first_name = validated_data['first_name'],
            password=validated_data['password']
        )
        user.save()

        return user



class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    tokens = serializers.CharField(max_length=100, min_length=6, read_only=True)
    password = serializers.CharField(write_only=True, max_length=100, min_length=4, required=True)

    class Meta:
        model = User
        fields = ['email','tokens','password']


    def validate(self, attrs):
        email = attrs.get('email',None)
        password = attrs.get('password',None)

        if not authenticate(email=email,password=password):
            raise serializers.ValidationError('Email or password is invalid')

        user = User.objects.filter(email=email).first()

        return {
            'email':user.email,
            'tokens':user.tokens()
        }



#logout serializer
class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(min_length=2)

    default_error_messages = {
        'bad_token':'token is expired or invalid'
    }

    def validate(self, attrs):

        self.token = attrs['refresh_token']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()

        except Exception:
            self.fail('bad_token')



#Reset Password Serializer
class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        req = self.context['request']
        email = attrs.get('email',None)
        user_exists = User.objects.filter(email=email).exists()

        if user_exists:
            user = User.objects.get(email=email)
            send_email(user,req)
            return attrs
        return attrs






#set new password serializer
class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=4, max_length=100, write_only=True)
    uidb64 = serializers.CharField(min_length=1, max_length=100, write_only=True)
    token = serializers.CharField(min_length=1, max_length=100, write_only=True)

    class Meta:
        fields = ['password','uidb64','token']


    def validate(self, attrs):
        try:
            password =attrs.get('password',None)
            uidb64 = attrs.get('uidb64',None)
            token = attrs.get('token',None)
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user,token):
                raise serializers.ValidationError('The reset link is invalid', 401)

            user.set_password(password)
            user.save()
            return user

        except Exception as e:
            raise serializers.ValidationError('The reset link is invalid', 401)


#logout serializer
class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(min_length=2)

    default_error_messages = {
        'bad_token':'token is expired or invalid'
    }

    def validate(self, attrs):

        self.token = attrs['refresh_token']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()

        except Exception:
            self.fail('bad_token')



class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = '__all__'


