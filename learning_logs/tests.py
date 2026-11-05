from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Topic, Entry


class LearningLogTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password123')

        self.topic1 = Topic.objects.create(text='Python Programming', owner=self.user1)
        self.topic2 = Topic.objects.create(text='Django Framework', owner=self.user2)

        self.entry1 = Entry.objects.create(topic=self.topic1, text='Learning Django models and views')

    def test_index_page(self):
        response = self.client.get(reverse('learning_logs:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Learning Log')

    def test_topics_login_required(self):
        response = self.client.get(reverse('learning_logs:topics'))
        self.assertEqual(response.status_code, 302)

    def test_topics_list_for_user(self):
        self.client.login(username='user1', password='password123')
        response = self.client.get(reverse('learning_logs:topics'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Python Programming')
        self.assertNotContains(response, 'Django Framework')

    def test_topic_owner_access(self):
        self.client.login(username='user1', password='password123')
        response = self.client.get(reverse('learning_logs:topic', args=[self.topic1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Learning Django models and views')

    def test_topic_non_owner_access_404(self):
        self.client.login(username='user1', password='password123')
        response = self.client.get(reverse('learning_logs:topic', args=[self.topic2.id]))
        self.assertEqual(response.status_code, 404)

    def test_new_topic_post(self):
        self.client.login(username='user1', password='password123')
        response = self.client.post(reverse('learning_logs:new_topic'), {'text': 'Machine Learning'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Topic.objects.filter(text='Machine Learning', owner=self.user1).exists())

    def test_new_entry_post(self):
        self.client.login(username='user1', password='password123')
        response = self.client.post(
            reverse('learning_logs:new_entry', args=[self.topic1.id]),
            {'text': 'Another entry for python'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Entry.objects.filter(text='Another entry for python', topic=self.topic1).exists())

    def test_edit_entry_owner(self):
        self.client.login(username='user1', password='password123')
        response = self.client.post(
            reverse('learning_logs:edit_entry', args=[self.entry1.id]),
            {'text': 'Updated text for entry'}
        )
        self.assertEqual(response.status_code, 302)
        self.entry1.refresh_from_db()
        self.assertEqual(self.entry1.text, 'Updated text for entry')

    def test_edit_entry_non_owner_404(self):
        self.client.login(username='user2', password='password123')
        response = self.client.post(
            reverse('learning_logs:edit_entry', args=[self.entry1.id]),
            {'text': 'Hacker update'}
        )
        self.assertEqual(response.status_code, 404)
        self.entry1.refresh_from_db()
        self.assertNotEqual(self.entry1.text, 'Hacker update')
