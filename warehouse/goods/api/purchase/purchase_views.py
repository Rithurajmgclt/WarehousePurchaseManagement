import csv
import threading

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework .decorators import action
from rest_framework .response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from django.db.models import F


from ...models import Purchase,Product
from .purchase_serializers import PurchasetSerializer,PurchasetUploadCSVSerializer



class PurchaseViewset(viewsets.ModelViewSet):
    """
    model viewset to create,edit,delete puchse details online
    
    """
   
    serializer_class=PurchasetSerializer
    queryset=Purchase.objects.all()
    http_method_names=['get','post','put']
    # permission_classes = [IsAuthenticated]


    def check_dupicate_entry(self,data):
        try:
            if data[1] not in self.queryset.values_list('purchase_id',flat=True):
                return True
            else:
                return False
        except:
            return False

    def unique_data_list(self,csv_reader):
        bulk_create_purchase = []
        unique=list(filter(self.check_dupicate_entry,csv_reader))
        count=0
        for purchase_obj in unique[1:]:
            count=count+1
            if purchase_obj[0] and purchase_obj[3]:
                product = Product.objects.filter(id=purchase_obj[0])
                if product:    #logic to check product id mentioned in purchase order exists in our database or not
                    if product.first().available_stock-int(purchase_obj[3])>0: # available quantity should not be less than zero
                        product.update(available_stock=F('available_stock') - int(purchase_obj[3]))
                        puchase=Purchase(product=product.first(),purchase_id=purchase_obj[1],purchased_qty=purchase_obj[3])
                        bulk_create_purchase.append(puchase) # used bulk upload to avoid server crash during huge data uploas  
        Purchase.objects.bulk_create(bulk_create_purchase)         
        return unique         

    @action(detail=False,methods=['post'],serializer_class=PurchasetUploadCSVSerializer, parser_classes = [MultiPartParser])
    def post_puchase_order_from_csv(self,request):
        """
        end point to upload offline puchase order
        
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                csv_content = serializer.csv_content
                csv_reader = csv.reader(csv_content.splitlines())
                csv_reader = list(csv_reader)
                thread1 = threading.Thread(target=self.unique_data_list, args=(csv_reader))
                thread1.start()
                return Response({'msg':"succussful upload"}, status= status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


