from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Task

class TaskModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.task = Task.objects.create(name='Test Task', user=self.user)

    def test_task_creation(self):
        self.assertEqual(self.task.name, 'Test Task')
        self.assertEqual(self.task.status, 'pending')
        self.assertEqual(str(self.task), 'Test Task')

class ViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.task = Task.objects.create(name='Test Task', user=self.user)

    def test_dashboard_view(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Task')

    def test_create_task_view(self):
        response = self.client.post(reverse('create_task'), {
            'name': 'New Task',
            'description': 'Description',
            'status': 'pending'
        })
        self.assertEqual(response.status_code, 302) # Redirects after success
        self.assertEqual(Task.objects.count(), 2)

    def test_run_task_view(self):
        response = self.client.post(reverse('run_task', args=[self.task.pk]))
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.status, 'completed')
