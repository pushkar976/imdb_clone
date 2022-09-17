from dataclasses import fields
from platform import platform
from wsgiref.validate import validator
from rest_framework import serializers
from watchlist_app.models import Movie, Review,Watchlist,StreamPlatform
from datetime import datetime
from dateutil import relativedelta


# Custom Validators
def field_length(value):   # This function is passed as Validators.
    if len(value) < 5:
        raise serializers.ValidationError("Field should have atleat 5 char")
    return value

'''Normal Serializer'''
class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    name = serializers.CharField(validators=[field_length])
    description = serializers.CharField()
    release_date = serializers.DateField()
    active = serializers.BooleanField()
    
    def create(self, validated_data):
        return Movie.objects.create(**validated_data)
    
    # Here Instance is the old data and validated_data is the update request data
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name',instance.name)
        instance.description = validated_data.get('description',instance.description)
        instance.release_date = validated_data.get('release_date',instance.release_date)
        instance.active = validated_data.get('active',instance.active)
        instance.save()
        return instance
      
    '''Field level Validation'''
    
    # def validate_name(self, value):   # Here the "name" checks for the name defined in Model
    #     if len(value) < 5:
    #         raise serializers.ValidationError("Please provide name more than 5 characters")
    #     else:
    #         return value
        
    '''Object level Validation'''
    
    def validate(self, data): # The data here is the requested data from the user.
        if data['name'] == data['description']:
            raise serializers.ValidationError('name and description should not be same')
        return data


'''Model Serializer'''


class ReviewSerializer(serializers.ModelSerializer):
    
    reviewer = serializers.StringRelatedField(read_only = True)
    # movie = serializers.CharField()   #This will display the movie name on UI instead of id

    class Meta:
        model = Review
        # fields = '__all__'
        exclude = ('movie',)

class MovieSerializerModel(serializers.ModelSerializer):
    
    #Nested Serializer relations
    review = ReviewSerializer(many=True, read_only = True)
    # watchlist = serializers.CharField(source='watchlist.title')   #This line overwrites the watchlist field
                                                                # and gets the name instead of id
    
    class Meta:
        model = Movie
        # fields = "__all__"
        # fields = ['id','name','release_date']
        exclude = ['total_rating']
        
    '''Field level validation'''
    def validate_name(self, value):   # Here the "name" checks for the name defined in the Model.
        if len(value) < 5:
            raise serializers.ValidationError("Please provide name more than 5 characters")
        else:
            return value
        
    '''Object level Validation'''
    
    def validate(self, data):
        if data['name'] == data['description']:
            raise serializers.ValidationError('name and description should not be same')
        return data
    
    '''Calculate num of years here'''
    '''Adding more custom fields at runtime which are not present in models'''
    num_of_years = serializers.SerializerMethodField()
    
    def get_num_of_years(self, object):
        today = datetime.today()
        print('TODAY : ',today)
        release_date = object.release_date
        print('release_date : ',release_date)
        delta = relativedelta.relativedelta(today, release_date)
        print('Years, Months, Days between two dates is')
        print(delta.years, 'Years,', delta.months, 'months,', delta.days, 'days')
        return delta.years


class WatchlistSerializer(serializers.ModelSerializer):
    
    '''Here the object name "movie" has to be same as "related_name" defined in the model'''
    '''Nested Serializer Relationship'''
    movie = MovieSerializerModel(many = True, read_only = True)  # Movie Model Serializer
    # movie = serializers.StringRelatedField(many=True)      #This will only return the string specified in the model
    
    # platform = serializers.CharField(source='platform.name') #This line overwrites the watchlist field
                                                                # and gets the name instead of id
    
    class Meta:
        model = Watchlist
        fields = "__all__"
        
    
class StreamPlatformSerializer(serializers.ModelSerializer):
    
    '''Here the object name has to be same as "related_name" defined in the model'''
    '''Nested Serializer Relationship'''
    watchlist = WatchlistSerializer(many = True, read_only = True)
    
    class Meta:
        model = StreamPlatform
        fields = "__all__"
        

        