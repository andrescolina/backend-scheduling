from django.shortcuts import render
from rest_auth.registration.views import RegisterView
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserSerializer
)
from .models import (
    User,
    ModulesApplication,
    GroupsModuls
)
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from itertools import chain
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import (
    login as django_login,
    logout as django_logout
)
from django.conf import settings
from django.db.models import F

class ListUser(RegisterView):

    serializer = RegisterSerializer

    def to_dicts(self, instance):
        opts = instance._meta
        data = {}
        for f in chain(opts.concrete_fields, opts.private_fields):
            data[f.name] = f.value_from_object(instance)
        for f in opts.many_to_many:
            data[f.name] = [i.id for i in f.value_from_object(instance)]
        return data

    def perform_create(self, serializer):
        user = serializer.save(self.request)
        return self.to_dicts(user)

    def create(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            values = ['password', 'last_login', 'code_conffirmation']
            for delete in values:
                try:
                    del user[delete]
                except KeyError as e:
                    pass
            return Response(user, status=201)
        else:
            return Response(serializer.errors, status=400)

class LoginUser(APIView):

    permission_classes = [AllowAny, ]

    def post(self, request):    
        serializer = AuthTokenSerializer(
             data=request.data
        )
        if serializer.is_valid():
            token, _ = Token.objects.get_or_create(
                user=serializer.validated_data['user']
            )
            try:   
                user = User.objects.get(
                            username=str(request.data['username']).lower()
                        )
                userSerializer = UserSerializer(user).data

                userSerializer['token'] = token.key
                
                modules = list(GroupsModuls.objects.filter(
                    id_group=user.id_group
                ).values(
                        name=F('id_module__name'),
                        path=F('id_module__path'),
                        icon=F('id_module__icon'),
                        nickname=F('id_module__nickname')
                    )
                )
                userSerializer['modules'] = modules
                return Response(userSerializer, status=200)
            
            except:
                return Response(status=404)
            
        else:
            return Response(serializer.errors, status=400)


class LogoutView(APIView):



    def delete(self, request, *args, **kwargs):
        return self.logout(request)

    def logout(self, request):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass
        if getattr(settings, 'REST_SESSION_LOGIN', True):
            django_logout(request)

        response = Response({"detail": "Successfully logged out."},
                            status=200)
        return response