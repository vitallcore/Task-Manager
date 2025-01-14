from django.contrib.auth.views import get_user_model
from rest_framework import generics

from .permissions import IsCurrentUserOrReadOnly
from .serializers import UsersSerializer


class UsersAPIList(generics.ListCreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UsersSerializer


class UsersAPIUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UsersSerializer
    permission_classes = (IsCurrentUserOrReadOnly,)
