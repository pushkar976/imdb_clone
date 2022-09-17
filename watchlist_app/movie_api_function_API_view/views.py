from watchlist_app.models import Movie
from rest_framework.response import Response
from django.http import JsonResponse
from watchlist_app.movie_api_function_API_view.serializers import MovieSerializer
from rest_framework.decorators import api_view
from rest_framework import status

# Create your views here.

@api_view(['GET','POST'])
def movie_list(request):
    # Getting the Query set
    if request.method == 'GET':
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = MovieSerializer(data = request.data)     # This returns the serialized data
        if serializer.is_valid():
            serializer.save()                      # This line calls the create method of MovieSerializer class
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

@api_view(['GET','PUT','DELETE'])
def movie_details(request,pk):
    if request.method == 'GET':
        try:
            movie_1 = Movie.objects.get(pk=pk)
        except Exception:
            return Response(data={'error':'Movie not found'},status=status.HTTP_404_NOT_FOUND)
            
        serializer = MovieSerializer(movie_1)
        return Response(serializer.data)
    if request.method == 'PUT':
        movie_1 = Movie.objects.get(pk=pk)
        serializer = MovieSerializer(movie_1,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    
    if request.method == 'DELETE':
        movie_1 = Movie.objects.get(pk=pk)
        movie_1.delete()
        return Response({'message':'The movie id '+str(pk)+' is deleted.'},status=status.HTTP_201_CREATED) 
            