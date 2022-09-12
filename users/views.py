from rest_framework import mixins, status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.filters import SearchFilter, OrderingFilter

from utils.permissions import IsAccountOwner
from users.serializers import UserSignUpSerializer, UserLoginSerializer, UserModelSerializer
from users.models import Account


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):

    serializer_class = UserModelSerializer
    lookup_field = 'username'

    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering_fields = ('first_name', 'last_name')

    def get_queryset(self):
        """Restrict list to active-only."""
        queryset = Account.objects.all()
        if self.action == 'list':
            return queryset.filter(is_active=True)
        return queryset

    def get_permissions(self):
        if self.action in ['signup', 'login']:
            permissions = [AllowAny]
        elif self.action in ['list']:
            permissions = [IsAdminUser]
        elif self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            permissions = [IsAuthenticated, IsAccountOwner]
        else:
            permissions = [IsAuthenticated]
        return [p() for p in permissions]

    @action(detail=False, methods=['POST'])
    def signup(self, request):
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data
        return Response(data=data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['POST'])
    def login(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': UserModelSerializer(user).data,
            'token': token
        }
        return Response(data=data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        response = super(UserViewSet, self).retrieve(request, *args, **kwargs)
        data = {
            'user': response.data,
        }
        return Response(data=data, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        """Disable user instead of deleting."""
        instance.is_active = False
        instance.save()
