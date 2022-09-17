import imp
from lib2to3.pgen2 import token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.admin import Token
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from user_app.login_api.serializers import RegistratioSerializer, UserRegisterSerializer

'''Function based view'''
@api_view(['POST',])
def registration_view(request):
    
    if request.method == 'POST':
        serializer = RegistratioSerializer(data=request.data)
        
        response = {}
        if serializer.is_valid():
            user_account = serializer.save() 
            response['message'] = 'User created successfully'
            
            response['data'] = {'username' : user_account.username}
            response['data']['email'] = user_account.email
            
            token = Token.objects.get_or_create(user=user_account)[0].key
            response['data']['token'] = token
            return Response(response)

'''class based view'''
class registrationView(APIView):
    
    def post(self,request):
        
        serializer = RegistratioSerializer(data=request.data)
        response = {}
        if serializer.is_valid():
            user_account = serializer.save() 
            response['message'] = 'User created successfully'
            
            response['data'] = {'username' : user_account.username}
            response['data']['email'] = user_account.email
            
            token = Token.objects.get_or_create(user=user_account)[0].key
            response['data']['token'] = token
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)

        
# class registrationView(APIView):
    
#     def post(self,request):
        
#         serializer = UserRegisterSerializer(data=request.data)
        
#         response = {}
#         if serializer.is_valid():
#             print('DATA--------------',serializer.data)
#             user_account = serializer.create(serializer.data) 
#             response['message'] = 'User created successfully'
            
#             response['data'] = {'username' : user_account.username}
#             response['data']['email'] = user_account.email
            
#             token = Token.objects.get_or_create(user=user_account)[0].key
#             print('Token--------------',token)
#             response['data']['token'] = token
#             return Response(response)
#         else:
#             return Response(serializer.errors)
        
        
class registrationViewUsingJwt(APIView):
    
    def post(self,request):
        
        serializer = RegistratioSerializer(data=request.data)
        response = {}
        if serializer.is_valid():
            user_account = serializer.save() 
            response['message'] = 'User created successfully'
            
            response['data'] = {'username' : user_account.username}
            response['data']['email'] = user_account.email
            
            # token = Token.objects.get_or_create(user=user_account)[0].key
            refresh = RefreshToken.for_user(user_account)
            response['data']['token'] = {
                                                'refresh': str(refresh),
                                                'access': str(refresh.access_token),
                                         }
            return Response(response, status=status.HTTP_201_CREATED)
        
class logout_view(APIView):
    
    def post(self,request):
        request.user.auth_token.delete()
        return Response({'message':'User logged out'}, status=status.HTTP_200_OK)