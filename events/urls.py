from django.urls import include, path

from rest_framework.routers import DefaultRouter

from events import views as event_views

router = DefaultRouter()
router.register(r'events', event_views.EventViewSet, basename='events')

urlpatterns = [
    path('', include(router.urls))
]
