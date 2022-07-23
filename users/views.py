from django.shortcuts import render
from django.urls import reverse
from rest_framework.generics import (ListCreateAPIView, RetrieveAPIView, ListAPIView)
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from users.models import User
from users.serializers import ProfileSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework import status


# Create your views here.
class UserListView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    queryset = User.objects.all()

class SignUpView(ListCreateAPIView):
    """
    This API is for creating the new user.
    """
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer=serializer)

        return Response(
            data={
                "success": "True",
                "message": "User created successfully.",
                "status": status.HTTP_201_CREATED,
                'user list': request.build_absolute_uri('/') + \
                                reverse('users:user_list')[1:]
            }
        )


class ShowProfile(RetrieveAPIView):
    """
    This API is for showing the user detail.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer
    queryset = User.objects.all()


    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(instance=self.get_object())
        return Response(
            status=status.HTTP_200_OK,
            data=serializer.data
        )
