from django.db import IntegrityError
from django.shortcuts import render
from django.urls import reverse
from rest_framework.generics import (GenericAPIView, ListCreateAPIView, 
                                RetrieveAPIView, ListAPIView, UpdateAPIView)
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from users.models import BlackListedToken, User
from users.serializers import ChangePasswordSerializer, ProfileSerializer, \
                                        UserSerializer, UpdateProfileSerializer
from rest_framework.response import Response
from rest_framework import status
from users.permissions import IsTokenValid
from rest_framework.views import APIView


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
    permission_classes = [IsAuthenticated, IsTokenValid]
    serializer_class = ProfileSerializer
    queryset = User.objects.all()


    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(instance=self.get_object(),
                                             context={'request': request}
                                            )
        return Response(
            status=status.HTTP_200_OK,
            data=serializer.data
        )


class UpdateProfileView(UpdateAPIView):
    """
    Enter token in header and you will get allowed to update the user's data
    who is currently logged in.
    """
    permission_classes = [IsAuthenticated, IsTokenValid]
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
    permission_classes=[IsAuthenticated, IsTokenValid]
    serializer_class = ChangePasswordSerializer
    queryset = User.objects.all()

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(instance=request.user,
                                            data=request.data,
                                            context={'request':request}
                                        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            "success": True,
            "status": status.HTTP_200_OK,
            "message": f"Password changed successfully for user \
                        {request.user.email}"
        })


class LogoutView(GenericAPIView):
    """
    This class is responsible for blacklisting token and logout the user.
    """
    permission_classes = [IsAuthenticated, IsTokenValid]

    def get(self, request, *args, **kwargs):
        try:
            BlackListedToken.objects.create(user=request.user, 
                                            jti_token=request.auth.get("jti")
                                            )
        except IntegrityError:
            return Response({
                "success": False,
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "User can't logout."
            })

        return Response(
            {
                "success": True,
                "status": status.HTTP_200_OK,
                "message": "User logged out successfully."}
        )


class DeleteView(APIView):
    """
    This class is responsible for user deletion and only admin can delete the
    users.
    """
    permission_classes = [IsAdminUser, IsTokenValid]

    def delete(self, request, *args, **kwargs):

        try:
            user = User.objects.get(pk=kwargs.get('pk'))
            user.delete()
            return Response(
                {
                    "success": "True",
                    "status": status.HTTP_204_NO_CONTENT,
                    "message": "User deleted successfully."
                }
            )
        except User.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={
                    "success": "False",
                    "message": f"User with id {kwargs.get('pk')} doesn't exist."
                }
            )
