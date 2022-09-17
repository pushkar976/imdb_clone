import imp
from django.shortcuts import render
from watchlist_app.models import Movie
from django.http import JsonResponse
# Create your views here.

def movie_list(request):
    # Getting the Query set
    movies = Movie.objects.all()
    
    # Converting the queryset into dictonaries
    data = {
        'movies' : list(movies.values())
    }
    
    # Returning the dictonaries as Json Response
    return JsonResponse(data)

'''Below method returns the data for specific movie, however the problem is that 
the coder has to explictly create the dictonary which can be tedious and faulty

Hence the solution to this is Django Rest Framework

'''

def movie_details(request,pk):
    movie_1 = Movie.objects.get(pk=pk)
    data = {
        'name' : movie_1.name,
        'description' : movie_1.description,
        'active' : movie_1.active       
    }
    return JsonResponse(data)
    
    
