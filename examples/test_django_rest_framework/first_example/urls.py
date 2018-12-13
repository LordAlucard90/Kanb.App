from rest_framework import routers
from . import views
from django.urls import path


router = routers.DefaultRouter(trailing_slash=True)
router.register('task', views.TaskViewSet)

app_name = 'example'

urlpatterns = [
    # Additional personalized urls
] + router.urls
