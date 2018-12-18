from rest_framework import routers
from . import views
from django.urls import path


router = routers.DefaultRouter(trailing_slash=True)
router.register('task', views.TaskViewSet)

app_name = 'task_managing'

urlpatterns = [
    path('board', views.BoardView.as_view(), name='board')
] + router.urls
