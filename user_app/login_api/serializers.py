from email.policy import default
from django.contrib.auth.models import User
from rest_framework import serializers

'''Using Model Serializer'''
class RegistratioSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={'input_type' : 'password'},write_only=True)
    
    class Meta:
        model = User
        fields = ['username','email','password','password2'] #password2 is one extra field, needs to be created

        extra_kwargs = {
            'password':{'write_only': True}
        }
        
    '''Overwriting serializer save() method'''    
    def save(self):
        password = self.validated_data['password']    #password is recieved from the request which is then validated
        password2 = self.validated_data['password2']
        
        if password != password2:
            raise serializers.ValidationError({'error':'Password do not match'})
        if User.objects.filter(username=self.validated_data['username']).exists():
            pass
        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({'error' : 'Email already exsits'})
                
        user_account = User(email=self.validated_data['email'], username=self.validated_data['username'])
        user_account.set_password(password)
        user_account.save()
        
        # print('user_account-------------------------',user_account)
        
        return user_account

'''Using Normal Serializer'''  
class UserRegisterSerializer(serializers.Serializer):
    
    password2 = serializers.CharField(style={'input_type' : 'password'},write_only=True)
    
    username = serializers.CharField(default=None)
    email = serializers.EmailField(default=None)
    password = serializers.CharField(default=None)
    password2 = serializers.CharField(default=None)
    
    extra_kwargs = {
            'password':{'write_only': True}
        }
        
    def create(self, validated_data):
        password = self.validated_data['password']    #password is recieved from the request which is then validated
        password2 = self.validated_data['password2']
        
        if password != password2:
            raise serializers.ValidationError({'error':'Password do not match'})
        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({'error' : 'Email already exsits'})
                
        user_account = User(email=self.validated_data['email'], username=self.validated_data['username'])
        user_account.set_password(password)
        
        user_account.save()
        
        return user_account
    
    def validate(self, data): # The data here is the requested data from the user.
        
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError('user already exists')
        