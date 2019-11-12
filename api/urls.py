from rest_framework.routers import DefaultRouter

from api.views import CategoryViewSet

app_name = 'api'

router = DefaultRouter(trailing_slash=True)
router.register('', CategoryViewSet, basename='category')
urlpatterns = router.urls
