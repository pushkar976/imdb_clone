"""watchmate URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from watchlist_app.movie_api_class_API_view.views import MovieDetailsAPIView_ModelSerializer

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user_app.login_api.urls')),
    path('movie/', include('watchlist_app.movie_api_class_API_view.urls')),
    # path('movie/', include('watchlist_app.movie_api_function_API_view.urls')),
    path('watchlist/', include('watchlist_app.movie_api_class_API_view.urls')),
    path('otts/', include('watchlist_app.movie_api_class_API_view.urls')),
    
    # This line is added to let the active users(other than Admin) login and access the API's'''
    path('api-auth/', include('rest_framework.urls')),
]
