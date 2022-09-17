from rest_framework.throttling import UserRateThrottle

class MovieDetailsThrottle(UserRateThrottle):
    scope = 'movie-details'

class CreateReviewThrottle(UserRateThrottle):
    scope = 'create-review'