from django.shortcuts import render
from rest_auth.registration.views import RegisterView
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserSerializer
)
from .models import (
    User
)
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from itertools import chain
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings
import jwt
from django.contrib.auth import authenticate
from rest_framework.authtoken.serializers import AuthTokenSerializer

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
        serializer = LoginSerializer(
                data=request.data
            )
        if serializer.is_valid():
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            try:   
                user = User.objects.get(
                            username=str(request.data['username']).lower()
                        )
                userSerializer = UserSerializer(user).data
            except:
                return Response(status=404)
            auth = AuthTokenSerializer(data=request.data)
            if auth.is_valid():
                payload = jwt_payload_handler(user)
                userSerializer['token'] = jwt_encode_handler(payload)
                return Response(userSerializer, status=200)
            else:
                return Response(auth.errors, status=400)
            return Response(status=201)
        else:
            return Response(serializer.errors, status=400)