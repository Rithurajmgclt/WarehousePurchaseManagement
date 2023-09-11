# WarehousePurchaseManagement
#deatils
this is a projrect to manage products in a warehouse u can create product in backend list and  edit the same, 
purchase order can create online for each product, offile puchase can aslo do and csv of the purchase can be uploaded to back end.
proct stock will be reduced on each purchse
we can refill the stock of each product if needed

#basic
create virtual enviornment  active it .
run "pip install requirements.txt" from the root of directory where manage.py file locates
use  "python manage.py migrate" command to create tables
to run the server use "python manage.py runserver"


#api
1.swagger is added no need of postman to test
localhost/swagger url will lead you to api page

note.
use correct format of csv that is given by you headings('Product Id', 'Purchased Id', 'Product Name','Purchased Qty','Price Per Quantity')

