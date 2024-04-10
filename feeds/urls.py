from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='user-registration'),
    path('login/', views.UserLoginView.as_view(), name='user-login'),
    path('channel-groups/', views.ChannelGroupListView.as_view(), name='channel-groups-list'),
    path('subscribe/', views.SubscriptionView.as_view(), name='subscribe'),
    path('token-auth/', obtain_auth_token, name='token-auth'), 
    # Add more URL patterns as needed
]

