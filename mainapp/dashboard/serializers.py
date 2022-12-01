from rest_framework import serializers
from .models import Property, OwnedProp



class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'


class OwnedPropSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    shares = serializers.IntegerField()
    deposit = serializers.IntegerField()



class IndicateSerializer(serializers.Serializer):
    id = serializers.IntegerField()





class UpdateProp(serializers.Serializer):
    id = serializers.IntegerField()





class DetailPropSerializer(serializers.Serializer):
    id = serializers.CharField()





