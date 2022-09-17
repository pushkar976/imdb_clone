import email
from pyexpat import model
from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

class RegisterTestCase(APITestCase):
    
    def test_register(self):
        data = {
            'username' : 'testcaseuser1',
            'email' : 'test@user1.com',
            'password' : 'Testuser@123',
            'password2' : 'Testuser@123', 
        }
        response = self.client.post(reverse('register'), data)
        print(response.status_code)
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
class LoginLogoutTestCase(APITestCase):
    
    def setUp(self):

        data = {
            'username' : 'testcaseuser1',
            'email' : 'test@user1.com',
            'password' : 'Testuser@123',
            'password2' : 'Testuser@123', 
        }
        self.response = self.client.post(reverse('register'), data)
        print(self.response.status_code)
        self.token = self.response.json()['data']['token']
        
        
    def test_login(self):
        
        data = {
            'username':'testcaseuser1',
            'password':'Testuser@123'
        }
        
        response = self.client.post(reverse('login'),data)
        print(response.status_code)
        print(response.json())
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
    def test_logout(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token '+self.token)
        response=self.client.post(reverse('logout'))
        print(response.json())
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
