from django.contrib.auth.models import User
from rest_framework import generics, permissions

from .serializers import UserSerializer


class UserCreateApiView(generics.CreateAPIView):
    """
    API endpoint that allows user creation
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
