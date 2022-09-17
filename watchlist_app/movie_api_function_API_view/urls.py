from django.urls import path,include
from watchlist_app.movie_api_function_API_view.views import movie_list, movie_details

urlpatterns = [
    # For function based API view
    path('list/', movie_list, name = 'movie-list'),
    path('<int:pk>', movie_details, name='movie_details')
    
]