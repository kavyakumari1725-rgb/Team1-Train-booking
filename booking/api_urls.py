from rest_framework.routers import DefaultRouter
from .api import TrainViewSet, TicketViewSet

router = DefaultRouter()
router.register('trains', TrainViewSet, basename='api-trains')
router.register('tickets', TicketViewSet, basename='api-tickets')

urlpatterns = router.urls
