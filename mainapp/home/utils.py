import uuid
import six
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.conf import settings
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.core import mail
import threading
from .models import Points, User, LandingPage,Referral



class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (six.text_type(user.pk)+six.text_type(timestamp)+six.text_type(user.verified))





def generate():
    code = uuid.uuid4()
    final = str(code).replace('-', '')[:12]
    return final


class Error:
    def error(self,error):
        erro = {}
        for key, value in error.items():
            erro["errors"] = value
        return erro


class EmailThread(threading.Thread):
    def __init__(self,email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        return self.email.send()





def send_activation_email(user,request):
    current_site = get_current_site(request)
    subject = 'Thank you for joining our waitlist'
    body = render_to_string(
        'home/email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': TokenGenerator().make_token(user)
        }
    )

    email = EmailMultiAlternatives(subject=subject,from_email='Phesika <support@phesika.com>', to=[user.landing_email])
    email.attach_alternative(body,'text/html')
    EmailThread(email).start()


class PointThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        try:

            user = LandingPage.objects.get(landing_email=self.email)
            point =Points.objects.create(user=user, points=1)
            return point
        except:
            return None


def add_points(email):
    PointThread(email).start()


class ReferralThread(threading.Thread):
    def __init__(self ,user):

        self.user = user
        threading.Thread.__init__(self)

    def run(self):
        try:
            author = LandingPage.objects.get(ref_code=self.user.referred_code)

            refer = Referral.objects.create(author=author, referral=self.user)
            return refer
        except:
            return None




def refer(user):
    ReferralThread(user).start()




def send_email(user,request):
    current_site = get_current_site(request)
    subject = 'Reset Password'
    body = render_to_string(
        'home/reset_password.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': PasswordResetTokenGenerator().make_token(user)
        }
    )

    email = EmailMultiAlternatives(subject=subject,from_email='Reset Password <support@phesika.com>', to=[user.email])
    email.attach_alternative(body,'text/html')
    EmailThread(email).start()




def contactus_email(request,email_n, name, message):
    subject = 'New Customer Message'
    body = render_to_string('home/contactus.html', {
        'email': email_n,
        'name': name,
        'message': message
    })

    email = EmailMessage(subject=subject, body=body, from_email=email_n,
                         to=['support@phesika.com']
                         )

    EmailThread(email).start()

