from rest_framework import response, status, generics

from .models import User
from .serialiezrs import UserSerializer


class CreateUserViews(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

