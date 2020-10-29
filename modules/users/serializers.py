
from rest_framework import serializers
from allauth.account.adapter import get_adapter
from allauth.account import app_settings as allauth_settings
from allauth.utils import (email_address_exists,
                               get_username_max_length)
from .models import (
    User,
    ModulesApplication,
    GroupsModuls
)

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True
    )
    first_name = serializers.CharField(
        required=True, 
        write_only=True
    )
    last_name = serializers.CharField(
        required=False, 
        allow_blank=False
    )
    password1 = serializers.CharField(
        required=True, 
        write_only=True
    )
    password2 = serializers.CharField(
        required=True, 
        write_only=True
    )
    phone_office = serializers.CharField(
        required=False, 
        allow_blank=False
    )
    phone_mobile = serializers.CharField(
        required=False, 
        allow_blank=False
    )
    phone_home = serializers.CharField(
        required=False, 
        allow_blank=False
    )
    city = serializers.CharField(
        required=True, 
        write_only=True
    )
    type_document = serializers.CharField(
        required=True, 
        write_only=True
    )
    document = serializers.CharField(required=True, write_only=True)
    username = serializers.CharField(
        max_length=20,
        min_length=5,
        required=True
    )
    is_staff = serializers.BooleanField(
        default=False, 
        required=False
    )
    is_active = serializers.BooleanField(
        default=False, 
        required=False
    )
    id_group = serializers.IntegerField(
        required=False, 
        write_only=True
    )

    def validate_username(self, username):
        username = get_adapter().clean_username(username)
        return username

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    "A user is already registered with this e-mail address.")
        return email

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("The two password fields didn't match.")
        return data

    def custom_signup(self, request, user):
        pass

    def get_cleaned_data(self):
        return {
            'id': self.validated_data.get('id', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            'username': self.validated_data.get('username', ' '),
            'email': self.validated_data.get('email', ''),
            'phone_office': self.validated_data.get('phone_office', ' '),
            'is_active': self.validated_data.get('is_active', ''),
            'city': self.validated_data.get('city', ''),
            'phone_mobile': self.validated_data.get('phone_mobile', ' '),
            'phone_home': self.validated_data.get('phone_home', ' '),
            'type_document': self.validated_data.get('type_document', ' '),
            'document': self.validated_data.get('document', ' '),
            'id_group': self.validated_data.get('id_group', ' ')
        }

    def save(self, request):
        adapter = get_adapter()
        self.cleaned_data = self.get_cleaned_data()
        user = adapter.new_user(self.cleaned_data)
        adapter.save_user(self.cleaned_data, user, self)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True, 
        write_only=True
    )
    password = serializers.CharField(
        required=True, 
        write_only=True
    )

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ('password',)
        write_only_fields = ('password',)
        read_only_fields = (
            'is_staff',
            'is_superuser',
            'date_joined',
        )

class ModulSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModulesApplication
        fields = '__all__'