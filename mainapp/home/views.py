from rest_framework.response import Response
from rest_framework import status
from .models import User, LandingPage, Referral, Points
from rest_framework import generics
from .serializer import LandingSerializer, CompleteSignUpSerializer, ReferralLandingSerializer, SetNewPasswordSerializer, ResetPasswordSerializer,LogoutSerializer, LoginSerializer, ContactUsSerializer
from .utils import generate, Error, send_activation_email, TokenGenerator,add_points,refer, contactus_email
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework.permissions import IsAuthenticated
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import ast






#landing page view
class LandingPageView(generics.GenericAPIView):
    serializer_class = LandingSerializer
    def post(self,request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():

            email= serializer.data['landing_email']
            if User.objects.filter(email=email).exists():
                error = Error().error({'error':'Email has already registered'})
                return Response(error, status=status.HTTP_400_BAD_REQUEST)

            ref_code = generate()
            LandingPage.objects.create(landing_email=email,ref_code=ref_code)
            user = LandingPage.objects.get(landing_email=email)
            send_activation_email(user,request)
            return Response(
                {
                    'email':email,
                    'ref_code':ref_code
                },
                status=status.HTTP_201_CREATED
            )
        error = Error().error(serializer.errors)

        return Response({"errors":error['errors'][0]}, status= status.HTTP_400_BAD_REQUEST)




#complete sign up view
class CompleteSignUpView(generics.GenericAPIView):

    serializer_class = CompleteSignUpSerializer
    def post(self, request):
        data = request.data

        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            email = serializer.data['email']
            token = serializer.data['tokens']

            user = User.objects.get(email=email)
            if not LandingPage.objects.filter(landing_email=email).exists():
                user.ref_code = generate()
                user.save()
                LandingPage.objects.create(landing_email=email, ref_code=user.ref_code)
            else:
                user_land = LandingPage.objects.get(landing_email=email)
                user.ref_code = user_land.ref_code
                user.save()
            add_points(email)
            k = ast.literal_eval(token)
            return Response(
                {
                    'msg':'sign up is complete',
                    'token':{"refresh":k['refresh'], "access":k['access']},
                    'ref_code':user.ref_code
                },
                status=status.HTTP_200_OK
            )
        error = Error().error(serializer.errors)
        return Response({"errors":error['errors'][0]}, status=status.HTTP_400_BAD_REQUEST)




# verification of email sent when user signup to waitlist
class VerifyEmail(generics.GenericAPIView):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))

            user = LandingPage.objects.get(pk=uid)

        except Exception as e:
            user = None

        if user and TokenGenerator().check_token(user, token):
            user.verified = True
            user.save()
            return Response({'msg': 'email verified', 'email': user.landing_email}, status=status.HTTP_200_OK)

        return Response({'errors': 'verification failed'}, status=status.HTTP_400_BAD_REQUEST)



#referral
class ReferralLandingView(generics.GenericAPIView):
    serializer_class = ReferralLandingSerializer


    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            email = serializer.data['landing_email']
            referred_code = serializer.data['referred_code']
            ref_code = generate()
            if not LandingPage.objects.filter(ref_code=referred_code).exists():
                error = Error().error({'error': 'something might be wrong with your referral link'})
                return Response(error, status=status.HTTP_400_BAD_REQUEST)
            LandingPage.objects.create(landing_email=email, ref_code=ref_code, referred_code=referred_code)
            user = LandingPage.objects.get(landing_email=email)
            author = LandingPage.objects.get(ref_code=referred_code)

            add_points(author.landing_email)
            send_activation_email(user, request)
            refer(user)
            add_points(email)
            return Response(
                {
                    'email': email,
                    'ref_code': ref_code
                },
                status=status.HTTP_201_CREATED
            )
        error = Error().error(serializer.errors)
        return Response({"errors":error['errors'][0]}, status=status.HTTP_400_BAD_REQUEST)


class Customerdetails(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request):
        if LandingPage.objects.filter(landing_email=request.user.email).exists():

            try:

                author =LandingPage.objects.get(landing_email=request.user.email)
                points = Points.objects.filter(user=author).count()
                referrals = Referral.objects.filter(author=author)
                referral = [i.referral.landing_email for i in referrals]
            except Exception as e:
                return Response({'errors':'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)
            if points:
                return Response({'points':points, 'referrals':referral,'name':request.user.first_name,'ref_code':request.user.ref_code}, status=status.HTTP_200_OK)
            else:
                return Response({'errors':'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)
        elif Points.objects.filter(user=request.user).exists():

            points = Points.objects.filter(user=request.user).count()
            return Response({'points':points, 'referrals':[], 'name':request.user.first_name, 'ref_code':request.user.ref_code}, status=status.HTTP_200_OK)
        else:
            return Response({'errors':'User does not exist'},status.HTTP_400_BAD_REQUEST)




#Password token check view
class PasswordTokenCheckView(generics.GenericAPIView):
    def get(self,request,uidb64,token):
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user,token):
                return Response(
                    {
                        'errors':'Token is not valid, Please request a new one'
                    },
                    status=status.HTTP_401_UNAUTHORIZED
                )
            return Response({
                'success':True,
                'msg':'Valid Credentials',
                'uid64':uidb64,
                'token':token
            })
        except DjangoUnicodeDecodeError as e:
            return Response(
                {
                    'errors': 'Token is not valid, Please request a new one'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )



#set new password view
class SetNewPasswordView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self,request):

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return Response(
                {
                    'success':True,
                    'msg':'Password reset was successful'
                },
                status=status.HTTP_201_CREATED
            )
        else:
            error = Error().error(serializer.errors)
            return Response({"errors": error['errors'][0]}, status=status.HTTP_400_BAD_REQUEST)




#Reset Password View
class ResetPasswordView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        data = request.data
        serializers = self.serializer_class(data=data, context={'request':request})
        if serializers.is_valid():

            return Response(
                {
                    'msg':'We just sent you a link to reset your password'
                },
                status=status.HTTP_200_OK
            )
        else:
            error = Error().error(serializers.errors)
            return Response({"errors": error['errors'][0]}, status=status.HTTP_400_BAD_REQUEST)


#logout View
class LogoutView(generics.GenericAPIView):

    serializer_class = LogoutSerializer

    permission_classes = (IsAuthenticated,)

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            error = Error().error(serializer.errors)
            return Response({"errors": error['errors'][0]}, status=status.HTTP_400_BAD_REQUEST)




#Login View
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data, context={'request':request})
        if serializer.is_valid():

            email = serializer.data['email']
            token = serializer.data['tokens']
            user = User.objects.get(email=email)
            k = ast.literal_eval(token)
            return Response({
                'email':email,
                'first_name':user.first_name,
                'token':{"refresh":k['refresh'], "access":k['access']}
            }, status=status.HTTP_200_OK)
        else:
            error = Error().error(serializer.errors)
            return Response({"errors": error['errors'][0]}, status=status.HTTP_400_BAD_REQUEST)



class ContactUsView(generics.GenericAPIView):
    serializer_class = ContactUsSerializer

    def post(self,request):
        data = request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            email_n = serializer.data["email"]
            name = serializer.data["name"]
            message = serializer.data["message"]
            contactus_email(request,email_n,name,message)
            return Response({"msg":"Message has been recieved, we would get back to you"}, status= status.HTTP_200_OK)
        else:
            error = Error().error(serializer.errors)
            return Response({"errors": error['errors'][0]}, status=status.HTTP_400_BAD_REQUEST)
