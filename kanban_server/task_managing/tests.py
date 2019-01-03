from django.test import TestCase
from django.urls import reverse
from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.utils import json

from .serializers import TaskSerializer
from .views import BoardView
from .models import Task, Event


class TaskCreationTesting(APITestCase):
    task_list_url = reverse('task_managing:task-list')

    def test_given_task_data_when_post_than_create_task(self):
        data = {"title": "First task", "status": "BACKLOG", 'owner': 'Ayeye Brazorf'}
        response = self.client.post(self.task_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get().title, 'First task')
        self.assertEqual(Task.objects.get().status, 'BACKLOG')
        self.assertEqual(Task.objects.get().owner, 'Ayeye Brazorf')
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
        self.assertEqual(response.data['owner'], self.saved_task.description)

    def test_given_task_when_update_description_than_check_description(self):
        response = self.client.patch(self.task_detail_url, {'description': 'This is a description'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Task.objects.get().description, 'This is a description')

        data = {'title': 'First task', 'description': 'This is a description', "status": "BACKLOG", 'owner': ''}
        self.assertEqual(response.data['description'], data['description'])


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


class EventDrivenTaskChange(TestCase):
    """
    post_save¶ - django.db.models.signals.post_save¶
    Like pre_save, but sent at the end of the save() method.

    Arguments sent with this signal:
        sender - The model class.
        instance - The actual instance being saved.
        created - A boolean; True if a new record was created.
        raw - A boolean; True if the model is saved exactly as presented
        using - The database alias being used.
        update_fields - The set of fields to update as passed to Model.save(), or None
    """

    def setUp(self):
        self.data = {"title": "First task", "status": "BACKLOG", 'owner': 'Ayeye Brazorf'}
        self.x = Task(**self.data)
        self.x.save()

    def test_given_task_when_created_than_write_event_for_creation(self):
        event = Event.objects.all().first()
        self.assertEqual("CREATED", event.name)
        self.assertNotEqual("UPDATED", event.name)

    def test_given_task_when_changed_than_write_event(self):
        x = Task.objects.get()
        self.assertEqual('BACKLOG', x.status)
        self.x.status = 'TODO'
        self.x.save()

        event = Event.objects.get(id=2)
        self.assertEqual("UPDATED", event.name)
        self.assertNotEqual("CREATED", event.name)
        self.assertEqual(x.id, event.object_id)

        print(event.JSON)
        loaded_json = json.loads(event.JSON)
        self.assertEqual(loaded_json['status'], ('BACKLOG', 'TODO',))
