from rest_framework import routers
from . import views
from django.urls import path


# To know more about routers urls
# https://www.django-rest-framework.org/api-guide/routers/#defaultrouter
router = routers.DefaultRouter(trailing_slash=True)
router.register('task', views.TaskViewSet)

app_name = 'example'

urlpatterns = [
    # Additional personalized urls
] + router.urls
