from django.contrib.auth import authenticate, password_validation

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token

from users.models import Account


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        """ Meta class. """

        model = Account
        fields = ('username',
                  'organization_name',
                  'email',
                  'first_name',
                  'last_name',
                  'is_staff',
                  'is_superuser',
                  'is_active')


class UserSignUpSerializer(serializers.Serializer):
    username = serializers.CharField(
        min_length=3,
        max_length=20,
        validators=[UniqueValidator(queryset=Account.objects.all())]
    )
    organization_name = serializers.CharField(min_length=2, max_length=60, required=False)
    email = serializers.EmailField(validators=[UniqueValidator(queryset=Account.objects.all())])
    password = serializers.CharField(min_length=8, max_length=64)
    password_confirmation = serializers.CharField(min_length=8, max_length=64)
    first_name = serializers.CharField(min_length=2, max_length=30)
    last_name = serializers.CharField(min_length=2, max_length=30)

    def validate(self, data):
        """Verify passwords match."""
        passwd = data['password']
        passwd_conf = data['password_confirmation']
        if passwd != passwd_conf:
            raise serializers.ValidationError("Passwords don't match.")
        password_validation.validate_password(passwd)
        return data

    def create(self, data):
        """Handle user and profile creation."""
        data.pop('password_confirmation')
        if not data.get('organization_name'):
            data['organization_name'] = f"{data['first_name']} {data['last_name']}"
        account = Account.objects.create_user(**data)

        return account


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])

        if not user:
            raise serializers.ValidationError('Incorrect credentials.')

        self.context['user'] = user
        return data

    def create(self, data):
        """ Generate/retrieve token. """
        token, created = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'], token.key
