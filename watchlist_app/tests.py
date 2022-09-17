from platform import platform
from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from watchlist_app import models


class MovieTestWithNormalUser(APITestCase):
    def setUp(self):
        # self.user= User.objects.create_user(username='example',password='Password@123')
    
        data = {
            'username' : 'testcaseuser1',
            'email' : 'test@user1.com',
            'password' : 'Testuser@123',
            'password2' : 'Testuser@123', 
        }
        self.response = self.client.post(reverse('register'), data)
        self.token = self.response.json()['data']['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token '+self.token)
        
        self.platform = models.StreamPlatform.objects.create(name='Prime',about='#1 OTT platform',
                                                             website='https//www.primevideo.com')
        self.watchlist = models.Watchlist.objects.create(title = 'Romance', storyline = 'All about romance', 
                                                         active = True, platform=self.platform)
        self.movie = models.Movie.objects.create(name='The Movie',description='Once for all',
                                                 release_date='2020-09-01', active=True,
                                                 watchlist=self.watchlist)
        
                
    def test_add_movie(self):
        
        data = {
            'name': 'Romance11',
            'description' : 'Let me romance',
            'release_date' : '2022-09-01',
            'active' : True,
            'watchlist' : self.watchlist
        }
        
        response = self.client.post(reverse('add-movie'), data)
        print(response.json())
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
    
    def test_movie_list(self):
    
        response = self.client.get(reverse('movie-list'))
        print(response.json())
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
    def test_movie_details(self):
        movie_details_response = self.client.get(reverse('movie_details', args=(self.movie.id,)))
        print(movie_details_response.json())
        self.assertEqual(movie_details_response.status_code,status.HTTP_200_OK)
        
    
        
        
class MovieTestWithAdminUser(APITestCase):
    
    def setUp(self):
        self.admin_user = User.objects.get_or_create(username='shubhi',password='Password@123',is_superuser=True, is_staff=True)[0].username
        self.admin_token = Token.objects.get_or_create(user_id=User.objects.get(username=self.admin_user).id)[0].key
        self.client.credentials(HTTP_AUTHORIZATION='Token '+self.admin_token)
        self.platform = models.StreamPlatform.objects.create(name='Prime',about='#1 OTT platform',
                                                             website='https//www.primevideo.com')
        self.watchlist = models.Watchlist.objects.create(title = 'Romance', storyline = 'All about romance', 
                                                         active = True, platform=self.platform)
        
    def test_admin_adds_movie(self):
        
        data = {
            'name': 'Romance11',
            'description' : 'Let me romance',
            'release_date' : '2022-09-01',
            'active' : True,
            'watchlist' : self.watchlist.id
        }
        
        response = self.client.post(reverse('add-movie'), data)
        print(response.json())
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)