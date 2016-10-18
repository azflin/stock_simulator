"""
Views for authentication to create a user, login, and logout.
"""
import json

from rest_framework import permissions, views, status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from .serializers import UserSerializer


class CreateUserView(CreateAPIView):
    """
    api/register/
        POST: Create a user. Payload must contain "username", "password", and optionally "email".
    """
    model = User
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = UserSerializer


class LoginView(views.APIView):
    """
    api/login/
        POST: Login a user. Payload must contain "username" and "password".
    """
    def post(self, request):
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
    """
    api/logout/
        POST: Logout currently authenticated user.
    """
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        logout(request)
        return Response({}, status=status.HTTP_204_NO_CONTENT)