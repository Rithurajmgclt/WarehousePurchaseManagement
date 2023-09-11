from rest_framework import serializers
from goods.models import Product

class ProductSerializer(serializers.ModelSerializer):
    available_stock=serializers.IntegerField(min_value=0, default=25000)
 
    class Meta:
        model = Product
        fields = ['id','name','price','available_stock']

class ProductEditSerializer(serializers.ModelSerializer):

 
    class Meta:
        model = Product
        fields = ['id','name','price']        


class ProductRefillSerializer(serializers.Serializer):
    refill_stock=serializers.IntegerField(min_value=0)
   
