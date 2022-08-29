import json

from rest_framework import status
from rest_framework.test import APITestCase

from users.models import Account


class AccountTests(APITestCase):
    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """
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
        self.assertEqual(Account.objects.count(), 2)
        self.assertEqual(Account.objects.get(id=1).organization_name, "FirstName LastName")
        self.assertEqual(Account.objects.get(id=2).organization_name, "Org")

        response = self.client.post(url, {}, format='json')
        content = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(content.get('username'), ['This field is required.'])
        self.assertEqual(content.get('email'), ['This field is required.'])
        self.assertEqual(content.get('password'), ['This field is required.'])
        self.assertEqual(content.get('password_confirmation'), ['This field is required.'])
        self.assertEqual(content.get('first_name'), ['This field is required.'])
        self.assertEqual(content.get('last_name'), ['This field is required.'])
