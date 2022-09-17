from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

# Create your models here. 

# The field created here are stored in the database.
'''If we make any changes in the model then we would need to make migrations and migrate inorder to get the changes 
stored in the database.'''

    
class StreamPlatform(models.Model):
    name = models.CharField(max_length=50)
    about = models.CharField(max_length=200)
    website = models.URLField(max_length=200)

    def __str__(self):
        return self.name
    
class Watchlist(models.Model):
    title = models.CharField(max_length=50)
    storyline = models.CharField(max_length=200)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    '''Adding relationship with Stream Platform Model'''
    platform = models.ForeignKey(StreamPlatform, on_delete=models.CASCADE, related_name='watchlist')

    def __str__(self):
        return self.title
    
class Movie(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    release_date = models.DateField(blank=True,null=True)
    active = models.BooleanField(default=True)
    average_rating = models.FloatField(default=0.0)
    total_rating = models.IntegerField(default=0)
    number_of_reviews = models.IntegerField(default=0)
    '''Adding relationship with Watchlist Model'''
    watchlist = models.ForeignKey(Watchlist, on_delete=models.CASCADE, related_name="movie")

    def __str__(self):
        return self.name
    
class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    description = models.CharField(max_length=200)
    '''Adding relationship with Movie Model'''
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='review')
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.movie.name +" | rating : "+ str(self.rating)   #Here self.movie.name is coming from the added Foreign key
