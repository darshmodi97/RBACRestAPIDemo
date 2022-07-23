from django.http import Http404
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from users.models import User
from django.core.exceptions import ObjectDoesNotExist


class UserSerializer(serializers.HyperlinkedModelSerializer):
    detail_url = serializers.HyperlinkedIdentityField(
        view_name='users:show_profile', read_only=True, lookup_field='pk')

    class Meta:
        model = User
        fields = ('role', 'email', 'password', 'detail_url',)
        extra_kwargs = {
            'password': {'write_only': True, 'style': {'placeholder': 'Password'}}
        }

    def create(self, validated_data):
        role = validated_data.get('role', "Solution Seeker")
        if role == "Admin":
            return User.objects.create_superuser(**validated_data)
        return User.objects.create_user(**validated_data)


class ProfileSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'role', 'email', )


class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'role')

    def update(self, instance, validated_data):


        instance.email = validated_data.get('email') if validated_data.get('email') != '' else instance.email

        instance.first_name = validated_data.get('first_name') \
            if validated_data.get('first_name') != '' else instance.first_name

        instance.last_name = validated_data.get('last_name') \
            if validated_data.get('last_name') != '' else instance.last_name

        role = validated_data.get('role')
        if role == 'Admin':
            instance.is_superuser =True
            instance.is_staff =True
        else:
            instance.is_superuser =False
            instance.is_staff =False
        if validated_data.get('password'):
            instance.set_password(validated_data.get('password'))
        instance.save()
        return instance


class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(max_length=150, write_only=True)
    new_password = serializers.CharField(max_length=150, write_only=True)
    new_password2 = serializers.CharField(max_length=150, write_only=True)

    class Meta:
        model = User
        fields = ('old_password', 'new_password', 'new_password2')

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def validate_old_password(self, value):
        instance = self._kwargs['instance']  # model object
        user = self.context['request'].user
        if user.id != instance.id:
            raise serializers.ValidationError("You don't have permission for this user.")
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError("old password is incorrect.")

        return value

    def update(self, instance, validated_data):
        user = self.context['request'].user
        if user.id != instance.id:
            raise serializers.ValidationError({"authorize": "You dont have permission for this user."})

        instance.set_password(validated_data['new_password2'])
        instance.save()
        return instance