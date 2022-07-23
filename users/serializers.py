from rest_framework import serializers
from users.models import User



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
        fields = ('first_name', 'last_name', 'role', 'email',)
