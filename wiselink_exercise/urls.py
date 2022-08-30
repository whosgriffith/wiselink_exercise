from django.urls import include, path

from rest_framework.authtoken import views

urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token),
    path('', include(('users.urls', 'users'), namespace='users')),
    path('', include(('events.urls', 'events'), namespace='events')),
]
