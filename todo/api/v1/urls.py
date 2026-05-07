from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r"task", TaskModelViewSet, basename="Task")
urlpatterns = router.urls
