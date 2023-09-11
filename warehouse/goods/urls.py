from django.urls import path,include

from rest_framework import routers

from .api.purchase.purchase_views import PurchaseViewset
from .api.product.product_views import ProductViewset


router =routers.DefaultRouter()
router.register('purchase',PurchaseViewset)
router.register('product',ProductViewset)


urlpatterns = [
    path('', include(router.urls)),
]