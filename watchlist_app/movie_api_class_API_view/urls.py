from django.urls import path,include
from rest_framework.routers import DefaultRouter
from watchlist_app.movie_api_class_API_view.views import MovieListAPIView, MovieDetailsAPIView, MovieListAPIView_ModelSerializer, MovieDetailsAPIView_ModelSerializer
from watchlist_app.movie_api_class_API_view.views import (Watchlist_Detail_APIView, 
                                                          Watchlist_APIView, 
                                                          StreamPlatform_APIView, 
                                                          StreamPlatformDetail_APIView,
                                                          Review_APIview,
                                                          Review_GenericView,
                                                          ReviewDetails_GenericView,
                                                          Review_ConcreteView,
                                                          ReviewDetails_ConcreteView,
                                                          Reviews_ConcreteView_overight,
                                                          ReviewCreate_ConcreteView_overight,
                                                          StreamPlatform_VS,
                                                          StreamPlatform_MVS,
                                                          ReviewDelete_AV,
                                                          ReviewsFilter_ConcreteView_overight,
                                                          ReviewsWithQueryParameter,
                                                          ReviewsWithDjangoFilter,
                                                          MovieListDjangoFilter,
                                                          AddMovie_APIview,
                                                          UpdateMovie_APIview,
                                                          MovieListDjangoSearch,
                                                          MovieListInOrder)

router = DefaultRouter()
router.register('ott',StreamPlatform_VS, basename='streamplatform')
router.register('mvs_ott',StreamPlatform_MVS, basename='mvs_streamplatform')


urlpatterns = [
    
    # For class based API view
    path('all/', MovieListAPIView.as_view(), name = 'movie-list'),
    path('add_movie/', AddMovie_APIview.as_view(), name = 'add-movie'),
    path('update_movie/<int:pk>/', UpdateMovie_APIview.as_view(), name = 'update-movie'),
    path('all_movie/', MovieListAPIView_ModelSerializer.as_view(), name = 'movie-list'),
    path('details/<int:pk>/', MovieDetailsAPIView_ModelSerializer.as_view(), name = 'movie_details'),
    path('item/<int:pk>/', MovieDetailsAPIView.as_view(), name='movie_details'),  
    path('all_watchlist/', Watchlist_APIView.as_view(), name = 'watch-list'),
    path('num/<int:pk>/', Watchlist_Detail_APIView.as_view(), name = 'watchlist-details'),
    path('all_ott/', StreamPlatform_APIView.as_view(), name = 'ott-list'),
    path('',include(router.urls)),
    
    path('id/<int:pk>/', StreamPlatformDetail_APIView.as_view(), name = 'ott-details'),
    path('reviews/', Review_APIview.as_view(), name = 'movie-review'),
    path('generic_reviews/', Review_GenericView.as_view(), name = 'movie-generic-review'),
    path('generic_review_details/<int:pk>/', ReviewDetails_GenericView.as_view(), name = 'movie-generic-review-details'),
    path('concrete_reviews/', Review_ConcreteView.as_view(), name = 'movie-concrete-review'),
    path('concrete_review_details/<int:pk>/', ReviewDetails_ConcreteView.as_view(), name = 'movie-concrete-review-details'),
    path('<int:pk>/review/', Reviews_ConcreteView_overight.as_view(), name = 'Reviews_ConcreteView_overight'),
    path('<int:pk>/create_review/', ReviewCreate_ConcreteView_overight.as_view(), name = 'Reviews_create_ConcreteView_overight'),
    path('<int:pk>/delete_review/', ReviewDelete_AV.as_view(), name = 'Reviews_delete'),
    path('user_review_details/<str:username>/', ReviewsFilter_ConcreteView_overight.as_view(), name = 'user-review-details'),
    path('user_review_details/', ReviewsWithQueryParameter.as_view(), name = 'user-review-details-params'),
    path('<int:pk>/user_review_filter/', ReviewsWithDjangoFilter.as_view(), name = 'user-review-details-djfilter'),
    path('list/', MovieListDjangoFilter.as_view(), name = 'movie-list-djfilter'),
    path('find/', MovieListDjangoSearch.as_view(), name = 'movie-search'),
    path('order/', MovieListInOrder.as_view(), name = 'movie-order'),
    
]