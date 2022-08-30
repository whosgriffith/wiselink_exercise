import json

from rest_framework import status
from rest_framework.test import APITestCase

from users.models import Account
from events.models import Event


class WiselinkExerciseTests(APITestCase):
    def test_create_account(self):
        url = '/users/signup/'
        data = {
            "username": "User2",
            "email": "user2@email.com",
            "password": "abcd123123",
            "password_confirmation": "abcd123123",
            "first_name": "FirstName",
            "last_name": "LastName",
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_account_with_organization_name(self):
        url = '/users/signup/'
        data = {
            "username": "User1",
            "email": "user1@email.com",
            "password": "abcd123123",
            "password_confirmation": "abcd123123",
            "first_name": "FirstName",
            "last_name": "LastName",
            "organization_name": "Org",
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Account.objects.count(), 1)
        self.assertEqual(Account.objects.get(id=2).organization_name, "Org")

    def test_create_account_without_required_fields(self):
        url = '/users/signup/'
        response = self.client.post(url, {}, format='json')
        content = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(content.get('username'), ['This field is required.'])
        self.assertEqual(content.get('email'), ['This field is required.'])
        self.assertEqual(content.get('password'), ['This field is required.'])
        self.assertEqual(content.get('password_confirmation'), ['This field is required.'])
        self.assertEqual(content.get('first_name'), ['This field is required.'])
        self.assertEqual(content.get('last_name'), ['This field is required.'])

    def test_create_event(self):
        account = Account.objects.create_user('root', 'root', is_staff=True)
        self.client.force_authenticate(account)
        url = '/events/'
        data = {
            "title": "Super Event",
            "short_description": "This is a super short description",
            "date_time": "2025-3-19T23:48"
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = {
            "title": "Super Super Event",
            "date_time": "2010-3-19T23:48"
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Event.objects.count(), 1)
        self.assertEqual(Event.objects.get(id=1).title, "Super Event")
        self.assertEqual(Event.objects.get(id=1).short_description, "This is a super short description")

        response = self.client.post(url, {}, format='json')
        content = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(content.get('title'), ['This field is required.'])

    def test_retrieve_event(self):
        account = Account.objects.create_user('user', 'user')
        self.client.force_authenticate(account)
        Event.objects.create(title="Super Event", date_time="2025-3-19T23:48", status="active")

        url = '/events/3/'
        response = self.client.get(url)
        content = json.loads(response.content)
        self.assertEqual(content['event']['title'], "Super Event")

    def test_retrieve_event_forbidden(self):
        account = Account.objects.create_user('user', 'user')
        self.client.force_authenticate(account)
        Event.objects.create(title="Forbidden Event", date_time="2025-3-19T23:48")

        url = '/events/3/'
        response = self.client.get(url)
        content = json.loads(response.content)
        self.assertEqual(content['detail'], "Not found.")

    def test_event_inscription(self):
        account = Account.objects.create_user('user', 'user')
        self.client.force_authenticate(account)
        Event.objects.create(title="Super Event", date_time="2025-3-19T23:48", status='active')

        url = '/events/2/register/'
        response = self.client.get(url)
        content = json.loads(response.content)
        self.assertEqual(content['detail'], "Inscription completed for Super Event")
