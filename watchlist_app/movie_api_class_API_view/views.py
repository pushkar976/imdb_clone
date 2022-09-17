from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.exceptions import ValidationError 
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle, ScopedRateThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from user_app.login_api.pagination import MovieListPagination,MovieLOpagination
from user_app.login_api.throtlling import MovieDetailsThrottle,CreateReviewThrottle
from watchlist_app.movie_api_class_API_view.permissions import AdminorReadOnly, IsOwnerOrReadOnly
from watchlist_app.models import Movie, Review,Watchlist,StreamPlatform
from watchlist_app.movie_api_class_API_view.serializers import (MovieSerializer
                                                                ,MovieSerializerModel,
                                                                WatchlistSerializer, 
                                                                StreamPlatformSerializer,
                                                                ReviewSerializer,
                                                                )


# Create your views here.

'''Creating views which will use Normal serializer'''
class MovieListAPIView(APIView):
    

    def get(self,request):
        
        # Getting the Query set
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)
        
    def post(self,request):

        serializer = MovieSerializer(data = request.data)     # This returns the serialized data
        if serializer.is_valid():
            serializer.save()                      # This line calls the create method of MovieSerializer class
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)


class MovieDetailsAPIView(APIView):

    def get(self,request,pk):
        try:
            movie_1 = Movie.objects.get(pk=pk)
            print('DATA TYPE---------------',type(movie_1)) # Returns complex data in form of model
        except Exception:
            return Response(data={'error':'Movie not found'},status=status.HTTP_404_NOT_FOUND)
            
        serializer = MovieSerializer(movie_1)
        print('DATA TYPE---------------',type(serializer)) # Returns serialized data in form of model
        print('DATA TYPE---------------',type(serializer.data))  # Returns dictonary
        print('DATA TYPE---------------',type(Response(serializer.data))) # Returns Response in Json format
        return Response(serializer.data)
        
    def put(self,request,pk):
        
            movie_1 = Movie.objects.get(pk=pk)
            serializer = MovieSerializer(movie_1,data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        
    def delete(self,request,pk):
        
        movie_1 = Movie.objects.get(pk=pk)
        movie_1.delete()
        return Response({'message':'The movie id '+str(pk)+' is deleted.'},status=status.HTTP_201_CREATED) 
    
    
'''Creating views which will use model serializer'''
class MovieListAPIView_ModelSerializer(APIView):

    def get(self,request):
        
        # Getting the Query set
        movies = Movie.objects.all()
        serializer = MovieSerializerModel(movies, many=True)
        return Response(serializer.data)
        
    def post(self,request):

        serializer = MovieSerializerModel(data = request.data)     # This returns the serialized data
        if serializer.is_valid():
            serializer.save()                      # This line calls the create method of MovieSerializer class
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)    
        
class MovieDetailsAPIView_ModelSerializer(APIView):
    
    # permission_classes = [IsAuthenticated]
    
    throttle_classes = [AnonRateThrottle,MovieDetailsThrottle] #Restricts the ananymous user and the registered user based
                                                           #on configuration in settings.py under REST_FRAMEWORK

    def get(self,request,pk):
        try:
            movie_1 = Movie.objects.get(pk=pk)
            print('DATA TYPE---------------',type(movie_1)) # Returns complex data in form of model
        except Exception:
            return Response(data={'error':'Movie not found'},status=status.HTTP_404_NOT_FOUND)
            
        serializer = MovieSerializerModel(movie_1)
        print('DATA TYPE---------------',type(serializer)) # Returns serialized data in form of model
        print('DATA TYPE---------------',type(serializer.data))  # Returns dictonary
        print('DATA TYPE---------------',type(Response(serializer.data))) # Returns Response in Json format
        return Response(serializer.data)
        
    def put(self,request,pk):
        
            movie_1 = Movie.objects.get(pk=pk)
            serializer = MovieSerializerModel(movie_1,data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        
    def delete(self,request,pk):
        
        movie_1 = Movie.objects.get(pk=pk)
        movie_1.delete()
        return Response({'message':'The movie id '+str(pk)+' is deleted.'},status=status.HTTP_201_CREATED)
    
class AddMovie_APIview(APIView):
    # import pdb; pdb.set_trace()
    permission_classes = [permissions.IsAdminUser]
    
    def post(self,request):
        print('Request=================',request.data)
        serializer = MovieSerializerModel(data = request.data)
        movie_obj = Movie.objects.filter(name = request.data['name'])
        if movie_obj.exists():
            return Response({'error':'Movie already exist'},status=status.HTTP_406_NOT_ACCEPTABLE)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)

class UpdateMovie_APIview(APIView):
   
    permission_classes = [permissions.IsAdminUser]        
    def put(self,request,pk):
        movie = Movie.objects.get(pk=pk)
        serializer = MovieSerializerModel(movie,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    

'''Watchlist'''
class Watchlist_APIView(APIView):

    def get(self,request):
        
        # Getting the Query set
        watchlist = Watchlist.objects.all()
        serializer = WatchlistSerializer(watchlist, many=True)
        return Response(serializer.data)
        
    def post(self,request):

        serializer = WatchlistSerializer(data = request.data)     # This returns the serialized data
        if serializer.is_valid():
            serializer.save()                      # This line calls the create method of MovieSerializer class
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)    
        
class Watchlist_Detail_APIView(APIView):

    def get(self,request,pk):
        # import pdb; pdb.set_trace()
        try:
            show = Watchlist.objects.get(pk=pk)
            print('DATA TYPE---------------',type(show)) # Returns complex data in form of model
        except Exception:
            return Response(data={'error':'Movie not found'},status=status.HTTP_404_NOT_FOUND)
            
        serializer = WatchlistSerializer(show)
        print('DATA TYPE---------------',type(serializer)) # Returns serialized data in form of model
        print('DATA TYPE---------------',type(serializer.data))  # Returns dictonary
        print('DATA TYPE---------------',type(Response(serializer.data))) # Returns Response in Json format
        return Response(serializer.data)
        
    def put(self,request,pk):
        
            show = Watchlist.objects.get(pk=pk)
            serializer = WatchlistSerializer(show,data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        
    def delete(self,request,pk):
        
        show = Watchlist.objects.get(pk=pk)
        show.delete()
        return Response({'message':'The show id '+str(pk)+' is deleted.'},status=status.HTTP_201_CREATED)
                
                
'''Stream Platform'''
class StreamPlatform_APIView(APIView):

    def get(self,request):
        
        # Getting the Query set
        platforms = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(platforms, many=True)
        return Response(serializer.data)
        
    def post(self,request):

        serializer = StreamPlatformSerializer(data = request.data)     # This returns the serialized data
        if serializer.is_valid():
            serializer.save()                      # This line calls the create method of MovieSerializer class
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)    
        
class StreamPlatformDetail_APIView(APIView):

    def get(self,request,pk):
        # import pdb; pdb.set_trace()
        try:
            platform = StreamPlatform.objects.get(pk=pk)
            print('DATA TYPE---------------',type(platform)) # Returns complex data in form of model
        except Exception:
            return Response(data={'error':'Movie not found'},status=status.HTTP_404_NOT_FOUND)
            
        serializer = StreamPlatformSerializer(platform)
        print('DATA TYPE---------------',type(serializer)) # Returns serialized data in form of model
        print('DATA TYPE---------------',type(serializer.data))  # Returns dictonary
        print('DATA TYPE---------------',type(Response(serializer.data))) # Returns Response in Json format
        return Response(serializer.data)
        
    def put(self,request,pk):
        
            platform = StreamPlatform.objects.get(pk=pk)
            serializer = StreamPlatformSerializer(platform,data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        
    def delete(self,request,pk):
        
        platform = StreamPlatform.objects.get(pk=pk)
        platform.delete()
        return Response({'message':'The show id '+str(pk)+' is deleted.'},status=status.HTTP_201_CREATED)
    

class Review_APIview(APIView):
    # import pdb; pdb.set_trace()
    permission_classes = [IsOwnerOrReadOnly]
    
    def get(self,request):
        user = self.request.user
        review = Review.objects.filter(reviewer = user)    #get review specific to user
        serializer = ReviewSerializer(review, many = True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = ReviewSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.data)        
        
        
'''GENERIC VIEWS'''
'''We use generic view with mixins, which has pre defined functions to perform crud operations'''

class Review_GenericView(mixins.ListModelMixin,generics.GenericAPIView):
    
    # permission_classes = [IsOwnerOrReadOnly]   # For list view "has_object_permission" method do not work
    queryset = Review.objects.all()              #The attribute names should always be same, as defined by drf
    serializer_class = ReviewSerializer
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
class ReviewDetails_GenericView(mixins.CreateModelMixin, mixins.RetrieveModelMixin, generics.GenericAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    

'''CONCRETE VIEW CLASS'''
'''It also has the predefined methods, which internally perform all the task using mixins'''

class Review_ConcreteView(generics.ListCreateAPIView):
    queryset = Review.objects.all()    #The attribute names should always be same, as defined by drf
    serializer_class = ReviewSerializer
    
    
class ReviewDetails_ConcreteView(generics.RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
    
'''OVERIGHT QUERYSET in CONCRETE VIEW'''
'''Here we are overighting in order to create URL's specific to our needs '''

class Reviews_ConcreteView_overight(generics.ListAPIView):
    # queryset = Review.objects.all()              
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(movie = pk)   # here "movie" is defined and added as foreign in review model
    
'''Basic Filtering'''
class ReviewsFilter_ConcreteView_overight(generics.ListAPIView):
    # queryset = Review.objects.all()              
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        username = self.kwargs['username']
        review_queryset = Review.objects.filter(reviewer__username = username)
        if review_queryset.exists():
            return review_queryset #Filter the review specific to username
        else:
            return Response(data={'error':'error'})  #Throws error since get_queryset() method only returns queryset
        
        
'''Basic Filtering using APIView'''
class ReviewsFilter_ConcreteView_overight(APIView):
    
    def get(self,request,username):
        # import pdb; pdb.set_trace()
        try:
            review = Review.objects.get(reviewer__username = username)
            print('DATA TYPE---------------',review) # Returns complex data in form of model
        except Exception:
            return Response(data={'error':'Review for user {} not found'.format(username)},status=status.HTTP_404_NOT_FOUND)
            
        serializer = ReviewSerializer(review)
        return Response(serializer.data)
    
'''Filtering against query parameters'''

class ReviewsWithQueryParameter(generics.ListAPIView):
    # queryset = Review.objects.all()              
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        username = self.request.query_params.get('username')
        review_queryset = Review.objects.filter(reviewer__username = username)
        return review_queryset #Filter the review specific to username

'''Filtering using Django-filter package'''
'''It only Supports GENERIC VIEWS'''
    
class ReviewsWithDjangoFilter(generics.ListAPIView):
    # queryset = Review.objects.all()              
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend]
    
    filterset_fields = ['reviewer__username', 'rating']
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(movie = pk)
    
'''PAGINATION   --  It works with Viewset and the generic view classes''' 
class MovieListDjangoFilter(generics.ListAPIView):

    queryset = Movie.objects.all()
    serializer_class = MovieSerializerModel
    filter_backends = [DjangoFilterBackend]
    # pagination_class = MovieListPagination        #page number pagination
    pagination_class = MovieLOpagination            #Limit Offset(Start) pagination
    
    filterset_fields = ['name', 'number_of_reviews']
    
    
'''SEARCH'''
class MovieListDjangoSearch(generics.ListAPIView):

    queryset = Movie.objects.all()
    serializer_class = MovieSerializerModel
    filter_backends = [filters.SearchFilter]
    
    search_fields = ['name', 'watchlist__title']
    
class MovieListInOrder(generics.ListAPIView):

    queryset = Movie.objects.all()
    serializer_class = MovieSerializerModel
    filter_backends = [filters.OrderingFilter]
    
    search_fields = ['name', 'average_rating']
    
        

class ReviewCreate_ConcreteView_overight(generics.CreateAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [CreateReviewThrottle]
    
    def get_queryset(self):
        return Review.objects.all()
    
    def perform_create(self, serializer):
        pk = self.kwargs['pk']
        movie_obj = Movie.objects.get(pk = pk)
        
        
        '''Checks for already exsitig review from the user '''
        user = self.request.user
        review_queryset = Review.objects.filter(movie = movie_obj,reviewer = user)
        
        if review_queryset.exists():
            raise ValidationError("Your review is already present")
        
        if movie_obj.number_of_reviews == 0:
            movie_obj.average_rating = serializer.validated_data['rating']
            movie_obj.total_rating = serializer.validated_data['rating']
            movie_obj.number_of_reviews = movie_obj.number_of_reviews + 1
        else:
            movie_obj.number_of_reviews = movie_obj.number_of_reviews + 1
            movie_obj.total_rating = movie_obj.total_rating + serializer.validated_data['rating']
            movie_obj.average_rating = movie_obj.total_rating/movie_obj.number_of_reviews
        movie_obj.save()
        serializer.save(movie=movie_obj, reviewer = user) 
        
        '''After hitting the URL, it will give an error "Movie field is required"
            Hence we need to exclude the movie field from the serializer, as we are already passing the 
            movie id in our URL
        '''
    
class ReviewDelete_AV(APIView):
    
    permission_classes = [IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review-delete'        #Throtteling directly for the specific view class
    
    
    def post(self,request,pk):
        serializer = ReviewSerializer(data=request.data)
        movie_obj = Movie.objects.get(pk = pk)
               
        '''Checks for already exsitig review from the user '''
        user = self.request.user
        review_queryset = Review.objects.filter(movie = movie_obj,reviewer = user)
        
        if review_queryset.exists():
            rating = review_queryset[0].rating
            
            if movie_obj.number_of_reviews > 1:
                movie_obj.number_of_reviews = movie_obj.number_of_reviews - 1
                movie_obj.average_rating = (movie_obj.total_rating - rating)/movie_obj.number_of_reviews
            else:
                movie_obj.average_rating = (movie_obj.total_rating - rating)/movie_obj.number_of_reviews
                movie_obj.number_of_reviews = movie_obj.number_of_reviews - 1
            movie_obj.total_rating = movie_obj.total_rating - rating
            review_queryset[0].delete() 
            movie_obj.save()
        else:
            return Response({'message':'No review for {} available for movie {}.'.format(user,movie_obj.name)},status=status.HTTP_404_NOT_FOUND)
        if serializer.is_valid():
            serializer.save()
        # serializer.save(movie=movie_obj,reviewer = user)
        
        return Response({'message':'{} user review for movie {} is deleted.'.format(user,movie_obj.name)    },status=status.HTTP_204_NO_CONTENT)
            
            
        
    


'''VIEWSET
    - Using Viewset we can handle multiple type of request without creating multiple URL's
    - In the below code we will handle both list and retrieve request in the same URL

'''         
class StreamPlatform_VS(viewsets.ViewSet):
    
    def list(self, request):
        queryset = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        queryset = StreamPlatform.objects.all()
        ott = get_object_or_404(queryset,pk=pk)
        serializer = StreamPlatformSerializer(ott)
        return Response(serializer.data)
    

'''MODEL VIEWSET'''
class StreamPlatform_MVS(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer

    
    
    