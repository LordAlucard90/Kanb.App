from rest_framework import routers
from . import views
from django.urls import path

router = routers.DefaultRouter()

app_name = 'example'

urlpatterns = [
    path('task/', views.TaskViewSet.as_view(), name='task-list')
]
