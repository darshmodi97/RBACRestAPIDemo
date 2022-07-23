from django.shortcuts import render
from django.urls import reverse
from rest_framework.generics import (ListCreateAPIView, RetrieveAPIView, ListAPIView, UpdateAPIView)
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from users.models import User
from users.serializers import ChangePasswordSerializer, ProfileSerializer, UserSerializer, UpdateProfileSerializer
from rest_framework.response import Response
from rest_framework import status


# Create your views here.
class UserListView(ListAPIView):
    """
    This API will show users list.
    """
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
        serializer = self.serializer_class(instance=self.get_object(), context={'request': request})
        return Response(
            status=status.HTTP_200_OK,
            data=serializer.data
        )


class UpdateProfileView(UpdateAPIView):
    """
    Enter token in header and you will get allowed to update the user's data who is currently logged in.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateProfileSerializer
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        """
        This method will show user's data.
        """
        user = request.user
        serializer = self.serializer_class(user)
        return Response(
            {
                "success": "True",
                "data": serializer.data,
                "status": status.HTTP_200_OK
            }
        )

    def put(self, request, *args, **kwargs):
        """This method will update user's details."""
        user = User.objects.get(email=request.user)
        serializer = self.serializer_class(instance=user, data=request.data)
        if serializer.is_valid():
            serializer.save()

        return Response(
                {
                    "success": "True",
                    "message": "User updated successfully.",
                    "data": serializer.data,
                    "status": status.HTTP_200_OK
                }
            )


class ChangePasswordView(UpdateAPIView):
    """
    This API is responsible for changing the password of user's account.
    """
    permission_classes=[IsAuthenticated]
    serializer_class = ChangePasswordSerializer
    queryset = User.objects.all()

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(instance=request.user, data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            "success": True,
            "status": status.HTTP_200_OK,
            "message": f"Password changed successfully for user {request.user.email}"
        })
