from rest_framework import serializers
from ...models import Purchase,Product
from rest_framework.exceptions import ValidationError
import csv

from django.db.models import F
from django.core.exceptions import ValidationError

class PurchasetSerializer(serializers.ModelSerializer):
    class Meta:
        model =Purchase
        fields = '__all__'
    def save(self, **kwargs):
        data = self._kwargs['data']

        try:
            product_id = data['product']
            purchased_qty = data['purchased_qty']
            product = Product.objects.filter(id = product_id)
            if product and  product.first().available_stock-purchased_qty>0:
                product.update(available_stock=F('available_stock') - int(purchased_qty))
                return super().save(**kwargs)
            else:
    
                raise ValidationError("check available qauntity of product")
        except KeyError as e:
            # Handle the KeyError if 'product' or 'purchased_qty' is missing in 'data'
            raise ValidationError(f"Missing data: {e}") 




class PurchasetUploadCSVSerializer(serializers.Serializer):
    csvfile = serializers.FileField(required=True)
    csv_content = None  # Initialize as None
    def validate_csvfile(self, value):
        # Check if the uploaded file has the correct CSV format
        try:
            
           
            csv_content = value.read().decode('utf-8')
            self.csv_content = csv_content

           

            csv_reader = csv.reader(csv_content.splitlines())
            header = next(csv_reader)
            # expected_header = ['Product Id', 'Purchased Id', 'Product Name','Purchased Qty','Price Per Quantity'] 
            # if header != expected_header:
            #     raise ValidationError("Invalid CSV format: Header does not match expected format.")

        except Exception as e:
            raise ValidationError("Invalid CSV format: Unable to parse the CSV file.")

        return value