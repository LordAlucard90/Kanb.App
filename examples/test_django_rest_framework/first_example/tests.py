from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Task


class TaskUrlTesting(APITestCase):

    def setUp(self):
        self.task_list_url = reverse('example:task-list')

    def test_given_task_url_when_get_than_status_code_eq_200(self):
        response = self.client.get(self.task_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_given_task_data_when_post_than_create_task(self):
    #     response = self.client.post(self.task_list_url, {'name': 'First task'}, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(Task.objects.count(), 1)
    #     self.assertEqual(Task.objects.get().name, 'First task')
