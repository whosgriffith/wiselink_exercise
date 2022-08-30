from datetime import timedelta

from django.utils import timezone
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from events.serializers import EventModelSerializer, UpdateEventSerializer
from users.serializers import UserModelSerializer
from events.models import Event


class EventViewSet(mixins.RetrieveModelMixin,
                   mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):

    queryset = Event.objects.all()
    serializer_class = EventModelSerializer

    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['date_time', 'status']
    ordering_fields = ['date_time', 'status']

    def get_queryset(self):
        queryset = Event.objects.all()
        only_active = self.request.query_params.get('only_active') is not None

        if not self.request.user.is_staff:
            queryset = queryset.filter(status='active')
        if self.action == 'register' or (self.action == 'list' and only_active):
            valid_date = timezone.now() + timedelta(hours=1)
            queryset = queryset.filter(status='active', date_time__gte=valid_date)
        return queryset

    def get_permissions(self):
        if self.action in ['create', 'partial_update', 'destroy', 'participants']:
            permissions = [IsAuthenticated, IsAdminUser]
        else:
            permissions = [IsAuthenticated]
        return [p() for p in permissions]

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = EventModelSerializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def perfom_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        response = super(EventViewSet, self).retrieve(request, *args, **kwargs)
        data = {
            'event': response.data,
        }
        response.data = data
        return response

    def update(self, request, pk=None):
        instance = self.get_object()
        serializer = UpdateEventSerializer(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        instance = self.get_object()
        serializer = UpdateEventSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def register(self, request, *args, **kwargs):
        """ Inscription for an event """
        event = self.get_object()
        account = request.user
        event.participants.add(account)
        event.save()
        return Response({'detail': f'Inscription completed for {event.title}'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def participants(self, request, *args, **kwargs):
        event = self.get_object()
        queryset = event.participants.all()
        serializer = UserModelSerializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
