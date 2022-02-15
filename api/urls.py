from rest_framework.routers import DefaultRouter

from api.views.trades import TradeViewSet

router = DefaultRouter()
router.register(r'trades', TradeViewSet, basename='trades')

urlpatterns = router.urls
