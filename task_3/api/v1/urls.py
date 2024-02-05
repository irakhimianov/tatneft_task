from rest_framework.routers import DefaultRouter

from api.v1 import views

app_name = 'v1'
router = DefaultRouter()

urlpatterns = []

router.register('stations', views.Station, basename='stations')

urlpatterns += router.urls
