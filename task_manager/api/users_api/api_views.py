from rest_framework import generics
from .serializers import UsersSerializer
from django.contrib.auth.views import get_user_model
from .permissions import IsCurrentUserOrReadOnly


class UsersAPIList(generics.ListCreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UsersSerializer


class UsersAPIUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UsersSerializer
    permission_classes = (IsCurrentUserOrReadOnly,)
