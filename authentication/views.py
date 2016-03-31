import json

from rest_framework import permissions, views, status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from .serializers import UserSerializer


class CreateUserView(CreateAPIView):

    model = User
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = UserSerializer


class LoginView(views.APIView):
    def post(self, request, format=None):

        data = json.loads(request.body)
        username = data.get('username', None)
        password = data.get('password', None)
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                serialized = UserSerializer(user)
                return Response(serialized.data)
            else:  # User is inactive
                return Response({
                    'status': 'Unauthorized',
                    'message': 'This account has been disabled.'
                }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({
                'status': 'Unauthorized',
                'message': 'Username/password combination invalid.'
            }, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        logout(request)

        return Response({}, status=status.HTTP_204_NO_CONTENT)