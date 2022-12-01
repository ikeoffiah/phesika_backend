from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, JSONParser
from .serializers import PropertySerializer, OwnedPropSerializer,DetailPropSerializer, IndicateSerializer
import cloudinary.uploader
from rest_framework import status
from django.core import serializers
from rest_framework import generics
from .models import Property, OwnedProp
from rest_framework.permissions import IsAuthenticated



class PropertyView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        properties = Property.objects.all()
        props = [{"id":property.id,"name":property.name,"image":property.property_pics.url,"price":property.price,"deposits":property.deposits,"project_return":property.project_return,"location":property.location,"time_left":property.time_left,"roi":property.roi} for property in properties]

        return Response({
            'msg':props
        })

class InterestsView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        properties = Property.objects.all()
        props = [
            {"interest":OwnedProp.objects.filter(owner=request.user,property=Property.objects.get(pk=property.id)).exists(),"id": property.id, "name": property.name, "image": property.property_pics.url, "price": property.price,
             "deposits": property.deposits, "project_return": property.project_return,
             "location": property.location, "time_left": property.time_left, "roi": property.roi} for property in
            properties if property.stage == "Interest"]

        return Response({
            'msg': props
        })



class FundedView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        properties = Property.objects.all()
        props = [
            {"interest":OwnedProp.objects.filter(owner=request.user,property=Property.objects.get(pk=property.id)).exists(),"id": property.id, "name": property.name, "image": property.property_pics.url, "price": property.price,
             "deposits": property.deposits, "project_return": property.project_return,
             "location": property.location, "time_left": property.time_left, "roi": property.roi} for property in
            properties if property.stage == "Funded"]

        return Response({
            'msg': props
        })


class ContractView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        properties = Property.objects.all()
        props = [
            {"interest":OwnedProp.objects.filter(owner=request.user,property=Property.objects.get(pk=property.id)).exists(),"id": property.id, "name": property.name, "image": property.property_pics.url, "price": property.price,
             "deposits": property.deposits, "project_return": property.project_return,
             "location": property.location, "time_left": property.time_left, "roi": property.roi} for property in
            properties if property.stage == "Contract"]

        return Response({
            'msg': props
        })



class ClosedView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        properties = Property.objects.all()
        props = [
            {"interest":OwnedProp.objects.filter(owner=request.user,property=Property.objects.get(pk=property.id)).exists(),"id": property.id, "name": property.name, "image": property.property_pics.url, "price": property.price,
             "deposits": property.deposits, "project_return": property.project_return,
             "location": property.location, "time_left": property.time_left, "roi": property.roi} for property in
            properties if property.stage == "Closed"]

        return Response({
            'msg': props
        })


class TrendingProp(generics.GenericAPIView):
    def get(self,request):
        propert = []
        properties = Property.objects.all()
        for property in properties:
            if property.deposits > 20000:
                propert.append({"id":property.id,"name":property.name,"image":property.property_pics.url,"price":property.price,"deposits":property.deposits,"project_return":property.project_return,"location":property.location,"time_left":property.time_left,"roi":property.roi})

        return Response({
            'msg':propert
        })


class DetailView(generics.GenericAPIView):
    serializer_class = DetailPropSerializer

    def post(self,request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            id = serializer.data["id"]
            property = Property.objects.get(pk=id)
            prop = {"id":property.id,"name":property.name,"image":property.property_pics.url,"price":property.price,"deposits":property.deposits,"project_return":property.project_return,"location":property.location,"time_left":property.time_left,"roi":property.roi}
            return Response({
                'msg':prop
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'errors':'Something went wrong'
            }, status=status.HTTP_400_BAD_REQUEST)





class PayPropView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = OwnedPropSerializer

    def post(self,request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            id = serializer.data['id']
            shares =serializer.data['shares']
            deposit = serializer.data['deposit']

            try:
                prop =Property.objects.get(pk=id)
            except:
                return Response({
                    "errors":"something went wrong"
                })
            if prop.deposits == prop.price:
                return Response({
                    "error":"This property has been purchased"
                }, status=status.HTTP_400_BAD_REQUEST)
            own_prop =OwnedProp.objects.get(owner=request.user,property=prop)
            own_prop.shares = shares + own_prop.shares
            own_prop.deposit = deposit + own_prop.deposit
            prop.deposits = prop.deposits + deposit
            prop.save()
            own_prop.save()

            return Response({
                'msg':'success'
            }, status=status.HTTP_200_OK)




class OwnedPropView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = IndicateSerializer

    def post(self,request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            id = serializer.data['id']
            try:
                prop =Property.objects.get(pk=id)
            except:
                return Response({
                    "errors":"something went wrong"
                })
            if not OwnedProp.objects.filter(owner=request.user,property=prop).exists():
                OwnedProp.objects.create(owner=request.user,property=prop)

                return Response({
                'msg':'success'
            }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "errors": "You have added this property"
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "errors": "something went wrong"
            },status=status.HTTP_400_BAD_REQUEST)





class InterestProp(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):

        try:
            prop = OwnedProp.objects.filter(owner=request.user)
            properties = [i.property for i in prop]
        except:
            return Response({
                'errors':"You have no properties"
            },status=status.HTTP_404_NOT_FOUND)

        props = [
            {"id": property.id, "name": property.name, "image": property.property_pics.url, "price": property.price,
             "deposits": property.deposits, "project_return": property.project_return,
             "location": property.location, "time_left": property.time_left, "roi": property.roi} for property in
            properties if property.stage == "Interest"]

        if props == []:
            return Response({
                'errors':'No property exist'
            }, status=status.HTTP_404_NOT_FOUND)
        return Response({
            'msg': props
        }, status=status.HTTP_200_OK)



class FundedProp(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        try:
            prop = OwnedProp.objects.filter(owner=request.user)
            properties = [i.property for i in prop]
        except:
            return Response({
                'errors':"You have no properties"
            },status=status.HTTP_404_NOT_FOUND)

        props = [
            {"funded":OwnedProp.objects.get(owner=request.user, property=property).deposit > 0,"completed":property.deposits==property.price,"id": property.id, "name": property.name, "image": property.property_pics.url, "price": property.price,
             "deposits": property.deposits, "project_return": property.project_return,
             "location": property.location, "time_left": property.time_left, "roi": property.roi} for property in
            properties if property.stage == "Funded" or property.stage =="Interest"]

        if props == []:
            return Response({
                'errors': 'No property exist'
            }, status=status.HTTP_404_NOT_FOUND)
        return Response({
            'msg': props
        }, status=status.HTTP_200_OK)


class ContractProp(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            prop = OwnedProp.objects.filter(owner=request.user)
            properties = [i.property for i in prop]
        except:
            return Response({
                'errors':"You have no properties"
            },status=status.HTTP_404_NOT_FOUND)

        props = [
            {"id": property.id, "name": property.name, "image": property.property_pics.url, "price": property.price,
             "deposits": property.deposits, "project_return": property.project_return,
             "location": property.location, "time_left": property.time_left, "roi": property.roi} for property in
            properties if property.stage == "Contract"]

        if props == []:
            return Response({
                'errors': 'No property exist'
            }, status=status.HTTP_404_NOT_FOUND)
        return Response({
            'msg': props
        }, status=status.HTTP_200_OK)


class ClosedProp(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            prop = OwnedProp.objects.filter(owner=request.user)
            properties = [i.property for i in prop]
        except:
            return Response({
                'errors':"You have no properties"
            },status=status.HTTP_404_NOT_FOUND)

        props = [
            {"id": property.id, "name": property.name, "image": property.property_pics.url, "price": property.price,
             "deposits": property.deposits, "project_return": property.project_return,
             "location": property.location, "time_left": property.time_left, "roi": property.roi} for property in
            properties if property.stage == "Closed"]

        if props == []:
            return Response({
                'errors': 'No property exist'
            }, status=status.HTTP_404_NOT_FOUND)
        return Response({
            'msg': props
        }, status=status.HTTP_200_OK)










class GetProps(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        try:
            prop = OwnedProp.objects.filter(owner=request.user)
            properties =[Property.objects.get(pk=i.property.id) for i in prop]
            props = [
                {"id": property.id, "name": property.name, "image": property.property_pics.url, "price": property.price,
                 "deposits": property.deposits, "project_return": property.project_return, "location": property.location,
                 "time_left": property.time_left, "roi": property.roi} for property in properties]


        except:
            return Response({
                'errors':'Nothing'
            }, status=status.HTTP_404_NOT_FOUND)
        return Response({
            'msg':props
        }, status=status.HTTP_200_OK)


class ProposedView(generics.GenericAPIView):
    def get(self, request):
        propert = []
        properties = Property.objects.all()
        for property in properties:
            if property.interest_sec:
                propert.append({"id": property.id, "name": property.name, "image": property.property_pics.url,
                                "price": property.price, "deposits": property.deposits,
                                "project_return": property.project_return, "location": property.location,
                                "time_left": property.time_left, "roi": property.roi})

        return Response({
            'msg': propert
        })















