from rest_framework import viewsets
from rest_framework. response import Response
from rest_framework import status
from rest_framework .decorators import action

from django.shortcuts import get_object_or_404
from goods.models import Product

from .produt_serializres import ProductSerializer,ProductEditSerializer,ProductRefillSerializer

class ProductViewset(viewsets.ModelViewSet):
    """
    model viewset to create,edit,delete products
    
    """
    queryset=Product.objects.all()
    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve' or self.action == 'create' :
            return ProductSerializer
        if self.action == 'update' or self.action == 'partial_update':
            return ProductEditSerializer
        return ProductRefillSerializer
        
    def create(self, request, *args, **kwargs):
        if int(request.data['available_stock'])!=25000:# checking entered value is 25000 or not
            return Response({'msg':'availabel stock will be 25000 initialy '},status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)
    @action(detail=True,methods=['post'],serializer_class=ProductRefillSerializer)
    def refill_product(sellf,request,pk):
        """
        end pint to refill the stock of product input id will be primary key of product
        """
        product_obj = get_object_or_404(Product, pk=pk)
        new_stock=product_obj.available_stock + int(request.data['refill_stock'])
        product_obj.available_stock=new_stock
        product_obj.save()
        return Response({'msg':f'{product_obj.name}  vailabe stock updated to {new_stock}'},status=status.HTTP_200_OK)

