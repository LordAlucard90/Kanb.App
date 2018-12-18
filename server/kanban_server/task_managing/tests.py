from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Task


class TaskUrlTesting(APITestCase):
    def setUp(self):
        self.task_list_url = reverse('task_managing:task-list')
        self.task_detail_url = reverse('task_managing:task-detail', kwargs={'pk': 1})

    def test_given_task_url_when_get_than_status_code_eq_200(self):
        response = self.client.get(self.task_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_given_task_data_when_post_than_create_task(self):
        response = self.client.post(self.task_list_url, {'title': 'First task'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get().title, 'First task')

    def test_given_task_when_delete_than_delete_it(self):
        self.client.post(self.task_list_url, {'title': 'First task'}, format='json')
        self.assertEqual(Task.objects.count(), 1)
        response = self.client.delete(self.task_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)

    def test_given_task_when_get_details_than_return_task_data(self):
        self.client.post(self.task_list_url, {'title': 'First task'}, format='json')
        response = self.client.get(self.task_detail_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'title': 'First task', 'description': ''})

    def test_given_task_when_update_description_than_check_description(self):
        self.client.post(self.task_list_url, {'title': 'First task'}, format='json')
        response = self.client.patch(self.task_detail_url, {'description': 'This is a description'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Task.objects.get().description, 'This is a description')
        self.assertEqual(response.data, {'title': 'First task', 'description': 'This is a description'})
