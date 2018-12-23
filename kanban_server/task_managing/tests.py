from django.test import TestCase
from django.urls import reverse
from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.test import APITestCase

from .views import BoardView
from .models import Task


class TaskCreationTesting(APITestCase):
    task_list_url = reverse('task_managing:task-list')

    def test_given_task_data_when_post_than_create_task(self):
        data = {"title": "First task", "status": "BACKLOG"}
        response = self.client.post(self.task_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get().title, 'First task')
        self.assertEqual(Task.objects.get().status, 'BACKLOG')
        self.assertEqual(response.data['status'], 'BACKLOG')

    def test_given_status_when_post_than_create_task(self):
        data = {"title": "aTask", "status": "TODO"}
        response = self.client.post(self.task_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_given_bad_status_when_post_than_not_create_task(self):
        data = {"title": "aTask", "status": "BAD STATUS"}
        response = self.client.post(self.task_list_url, data, format='json')
        self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)

    def test_given_aTask_when_post_than_default_status_is_backlog(self):
        data = {"title": "aTask", }
        response = self.client.post(self.task_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'BACKLOG')


class TaskRUDTesting(APITestCase):
    task_list_url = reverse('task_managing:task-list')
    task_detail_url = reverse('task_managing:task-detail', kwargs={'pk': 1})

    def setUp(self):
        x = Task(title='First task')
        x.save()
        self.saved_task = x

    def test_given_task_url_when_get_than_status_code_eq_200(self):
        response = self.client.get(self.task_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_given_task_when_delete_than_delete_it(self):
        response = self.client.delete(self.task_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)

    def test_given_task_when_get_details_than_return_task_data(self):
        response = self.client.get(self.task_detail_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.saved_task.title)
        self.assertEqual(response.data['description'], self.saved_task.description)

    def test_given_task_when_update_description_than_check_description(self):
        response = self.client.patch(self.task_detail_url, {'description': 'This is a description'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Task.objects.get().description, 'This is a description')

        data = {'title': 'First task', 'description': 'This is a description', "status": "BACKLOG"}
        self.assertEqual(response.data, data)


class TaskViewTesting(APITestCase):
    board_url = reverse('task_managing:board')

    def setUp(self):
        x = Task(title='First task')
        x.save()
        self.saved_task = x

    def test_given_board_view_when_called_than_correct_context(self):
        response = self.client.get(self.board_url)
        keys = ('tasks', 'title', 'columns',)

        for k in keys:
            self.assertIn(k, response.context)

        self.assertEqual(self.saved_task.title, response.context['tasks'][0].title)
