from rest_framework import serializers, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework.permissions import IsAuthenticated
from .models import ChannelGroup, Subscription
from .serializers import ChannelGroupSerializer, UserSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes

#### Implement User Authentication ####


class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(**serializer.validated_data)
            return Response({'username': user.username}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({'username': user.username})
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

####### Implement Subscription Logic #######

 
class ChannelGroupListView(generics.ListAPIView):
    queryset = ChannelGroup.objects.all()
    serializer_class = ChannelGroupSerializer
    
# @permission_classes([IsAuthenticated]) 
class SubscriptionView(APIView):

    def post(self, request):
        channel_group_id = request.data.get('channel_group_id')
        channel_group = ChannelGroup.objects.get(pk=channel_group_id)
        Subscription.objects.create(user=request.user, channel_group=channel_group)
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request):
        channel_group_id = request.data.get('channel_group_id')
        Subscription.objects.filter(user=request.user, channel_group_id=channel_group_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


